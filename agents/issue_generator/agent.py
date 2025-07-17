import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from agents.base_agent import BaseAgent

class IssueGeneratorAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
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

    def invoke_llm(self, prompt: str, provider: str) -> str:
        """Execute LLM with the given prompt"""
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
        
        llm_provider = self.config.get('llm_settings.default_provider', 'gemini')
        raw_result = self.invoke_llm(template, llm_provider)

        result = raw_result
        feature_marker = "# FEATURE:"
        marker_pos = raw_result.find(feature_marker)
        if marker_pos != -1:
            result = raw_result[marker_pos:]

        with open(output_file, 'w') as f:
            f.write(result)
        
        print(f"Issue specification saved to: {output_file}")
        return str(output_file)