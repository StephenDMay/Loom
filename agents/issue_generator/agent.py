import os
import re
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from core.llm_manager import LLMManager
    from core.context_manager import ContextManager

class IssueGeneratorAgent(BaseAgent):
    def __init__(self, config, llm_manager: 'LLMManager' = None, context_manager: 'ContextManager' = None):
        super().__init__(config, llm_manager, context_manager)
        self.output_dir = Path(self.config.get("project.root", Path.cwd())) / "generated-issues"
        self.template_directories = [
            Path(self.config.get("project.root", Path.cwd())) / d
            for d in self.config.get('templates.directories', [])
        ]

    def _find_template_path(self, template_name: str) -> Path | None:
        """Find template in configured directories."""
        for template_dir in self.template_directories:
            template_path = template_dir / template_name
            if template_path.exists():
                return template_path
        return None

    def _extract_title_from_markdown(self, content: str) -> str:
        """Extract the feature title from markdown content."""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            # Look for "# FEATURE:" pattern
            if line.startswith('# FEATURE:'):
                title = line.replace('# FEATURE:', '').strip()
                if title:
                    return title
            # Fallback to any # heading
            elif line.startswith('# '):
                title = line.replace('#', '').strip()
                if title and not title.lower().startswith('feature'):
                    return title
        return ""

    def _slugify(self, text: str) -> str:
        """Convert text to a URL-friendly slug."""
        if not text:
            return ""
        
        # Convert to lowercase and replace spaces with hyphens
        slug = text.lower()
        # Remove or replace special characters
        slug = re.sub(r'[^\w\s-]', '', slug)
        # Replace multiple spaces/hyphens with single hyphen
        slug = re.sub(r'[-\s]+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        # Limit length to reasonable size
        slug = slug[:60]
        
        return slug

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

    def execute(self, feature_description: str):
        """Execute the issue generation agent."""
        # Find template
        meta_prompt_template_path = self._find_template_path("meta-prompt-template.md")
        if not meta_prompt_template_path:
            # Fallback to the hardcoded path if not found in configured directories
            meta_prompt_template_path = Path(self.config.get("project.root", Path.cwd())) / "meta-prompt-template.md"
            if not meta_prompt_template_path.exists():
                return f"Error: Meta-prompt template not found in configured directories or at default path: {meta_prompt_template_path}"
            print(f"Warning: Meta-prompt template not found in configured directories. Using default path: {meta_prompt_template_path}")

        # Load and populate template
        with open(meta_prompt_template_path, 'r') as f:
            template = f.read()

        # Validate required config keys
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

        # Replace template placeholders
        template = template.replace('[PROJECT_CONTEXT_PLACEHOLDER]', config_values['project.context'])
        template = template.replace('[TECH_STACK_PLACEHOLDER]', config_values['project.tech_stack'])
        template = template.replace('[ARCHITECTURE_PLACEHOLDER]', config_values['project.architecture'])
        template = template.replace('[USER_BASE_PLACEHOLDER]', config_values['project.target_users'])
        template = template.replace('[CONSTRAINTS_PLACEHOLDER]', config_values['project.constraints'])
        template = template.replace('[USER_INPUT_PLACEHOLDER]', feature_description)
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Execute LLM call using LLMManager
        if not self.llm_manager:
            return "Error: LLMManager not available"
        
        try:
            raw_result = self.llm_manager.execute(template, agent_name="issue_generator")
        except Exception as e:
            return f"Error executing LLM call: {str(e)}"

        # Extract structured output
        result = self._extract_structured_output(raw_result)

        # Generate filename after content is created
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        
        # Extract title and create slug
        title = self._extract_title_from_markdown(result)
        slug = self._slugify(title)
        
        # Fallback to safe feature description if no title found
        if not slug:
            safe_feature = re.sub(r'[^\w\-_]', '_', feature_description)
            safe_feature = safe_feature[:50]
            slug = self._slugify(safe_feature.replace('_', ' '))
            if not slug:
                slug = "untitled-feature"
        
        output_file = self.output_dir / f"{timestamp}-{slug}.md"

        # Write to file
        with open(output_file, 'w') as f:
            f.write(result)
        
        print(f"Issue specification saved to: {output_file}")
        return str(output_file)