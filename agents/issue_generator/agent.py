import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from core.llm_manager import LLMManager

class IssueGeneratorAgent(BaseAgent):
    def __init__(self, config, llm_manager: 'LLMManager' = None):
        super().__init__(config, llm_manager)
        self.output_dir = Path(self.config.get("project.root", Path.cwd())) / "generated-issues"
        self.template_directories = [
            Path(self.config.get("project.root", Path.cwd())) / d
            for d in self.config.get('templates.directories', [])
        ]

    def _find_template_path(self, template_name: str) -> Path | None:
        for template_dir in self.template_directories:
            template_path = template_dir / template_name
            if template_path.exists():
                return template_path
        return None

    def _extract_structured_output(self, raw_result: str) -> str:
        """Extract structured output from LLM response, handling various formats"""
        # First, try to find the exact feature marker
        feature_marker = "# FEATURE:"
        marker_pos = raw_result.find(feature_marker)
        if marker_pos != -1:
            return raw_result[marker_pos:]
        
        # If no exact marker, look for any markdown heading that might be the feature
        lines = raw_result.split('\n')
        for i, line in enumerate(lines):
            # Look for a heading that might be a feature title
            if line.strip().startswith('# ') and any(keyword in line.lower() for keyword in ['feature', 'spec', 'implementation']):
                return '\n'.join(lines[i:])
        
        # Look for triple backticks indicating structured output
        if '```' in raw_result:
            # Find the start of the structured output block
            start_idx = raw_result.find('```')
            if start_idx != -1:
                # Find the content after the opening backticks
                content_start = raw_result.find('\n', start_idx) + 1
                end_idx = raw_result.find('```', content_start)
                if end_idx != -1:
                    return raw_result[content_start:end_idx].strip()
        
        # As a last resort, try to find any section that looks like structured output
        # Look for lines that start with ## (second-level headings)
        for i, line in enumerate(lines):
            if line.strip().startswith('## '):
                # This might be the start of structured content
                return '\n'.join(lines[i:])
        
        # If all else fails, return the original result with a warning comment
        return f"# EXTRACTED OUTPUT\n\n{raw_result}"

    def invoke_llm(self, prompt: str, agent_name: str = None) -> str:
        """Execute LLM with the given prompt using LLMManager"""
        if self.llm_manager:
            return self.llm_manager.execute(prompt, agent_name=agent_name)
        else:
            # Fallback to subprocess approach if no LLMManager available
            provider = self.config.get('llm_settings.default_provider', 'gemini')
            print(f"Executing prompt with provider: {provider}")
            
            import platform
            if platform.system() == "Windows" and provider in ["gemini"]:
                provider_cmd = f"{provider}.cmd"
            else:
                provider_cmd = provider
            
            try:
                result = subprocess.run(
                    [provider_cmd],
                    input=prompt,
                    text=True,
                    capture_output=True,
                    check=True
                )
                return result.stdout
                
            except subprocess.CalledProcessError as e:
                print(f"LLM provider execution failed with exit code {e.returncode}")
                print(f"Error details: {e.stderr}")
                sys.exit(1)
            except FileNotFoundError:
                print(f"LLM provider '{provider}' not found. Make sure it's installed and in your PATH.")
                sys.exit(1)

    def execute(self, feature_description: str):
        meta_prompt_template_path = self._find_template_path("meta-prompt-template.md")
        if not meta_prompt_template_path:
            # Fallback to the hardcoded path if not found in configured directories
            meta_prompt_template_path = Path(self.config.get("project.root", Path.cwd())) / "meta-prompt-template.md"
            if not meta_prompt_template_path.exists():
                return f"Error: Meta-prompt template not found in configured directories or at default path: {meta_prompt_template_path}"
            print(f"Warning: Meta-prompt template not found in configured directories. Using default path: {meta_prompt_template_path}")

        with open(meta_prompt_template_path, 'r') as f:
            template = f.read()

        config_values = {}
        required_keys = [
            'project.context', 'project.tech_stack', 'project.architecture',
            'project.target_users', 'project.constraints'
        ]
        for key in required_keys:
            value = self.config.get(key)
            if value is None:
                return f"Error: Missing required configuration key: '{key}'"
            config_values[key] = value

        template = template.replace('[PROJECT_CONTEXT_PLACEHOLDER]', config_values['project.context'])
        template = template.replace('[TECH_STACK_PLACEHOLDER]', config_values['project.tech_stack'])
        template = template.replace('[ARCHITECTURE_PLACEHOLDER]', config_values['project.architecture'])
        template = template.replace('[USER_BASE_PLACEHOLDER]', config_values['project.target_users'])
        template = template.replace('[CONSTRAINTS_PLACEHOLDER]', config_values['project.constraints'])
        template = template.replace('[USER_INPUT_PLACEHOLDER]', feature_description)
        
        self.output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_feature = re.sub(r'[^\w\-_]', '_', feature_description)
        safe_feature = safe_feature[:50]
        output_file = self.output_dir / f"{timestamp}_{safe_feature}.md"
        
        raw_result = self.invoke_llm(template, agent_name="issue_generator")

        # Extract the structured output from the LLM response
        result = self._extract_structured_output(raw_result)

        with open(output_file, 'w') as f:
            f.write(result)
        
        print(f"Issue specification saved to: {output_file}")
        return str(output_file)