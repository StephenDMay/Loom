import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING
from agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from core.llm_manager import LLMManager
    from core.context_manager import ContextManager


class PromptAssemblyAgent(BaseAgent):
    """
    An agent that dynamically constructs prompts by combining templates, context, and user input.
    """
    
    def __init__(self, config: Optional[Dict] = None, llm_manager: Optional['LLMManager'] = None, context_manager: Optional['ContextManager'] = None):
        super().__init__(config, llm_manager, context_manager)
        
        # Get templates directory from config
        self.templates_directory = self.config.get('prompt_assembly_agent', {}).get('templates_directory', 'templates')
        self.templates_path = Path(__file__).parent / self.templates_directory
        
        # Set up output directory (same as issue generator)
        self.output_dir = Path(self.config.get("project.root", Path.cwd())) / "generated-issues"

    def _load_template(self, template_name: str) -> str:
        """
        Load a template from the templates directory.
        
        Args:
            template_name: Name of the template file to load
            
        Returns:
            Template content as string
            
        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        # Add .md extension if not present
        if not template_name.endswith('.md'):
            template_name += '.md'
            
        template_file_path = self.templates_path / template_name
        
        try:
            with open(template_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            # Try to use default template if specified template not found
            default_template_path = self.templates_path / 'example_template.md'
            try:
                with open(default_template_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"Template file not found: {template_file_path} and default template not found: {default_template_path}")
        except Exception as e:
            raise Exception(f"Error loading template '{template_name}': {e}")

    def _get_context_values(self, context_keys: List[str]) -> Dict[str, str]:
        """
        Retrieve context values from the ContextManager.
        
        Args:
            context_keys: List of context keys to retrieve
            
        Returns:
            Dictionary mapping context keys to their values
        """
        context_values = {}
        
        if self.context_manager is None:
            return context_values
            
        for key in context_keys:
            value = self.context_manager.get(key)
            if value is not None:
                context_values[key] = str(value)
            else:
                # Handle missing context gracefully with empty string
                context_values[key] = ""
                
        return context_values

    def _replace_placeholders(self, template_content: str, placeholders: Dict[str, str], context_values: Dict[str, str]) -> str:
        """
        Replace placeholders in the template with provided values and context.
        
        Args:
            template_content: The raw template content
            placeholders: Dictionary of placeholder keys and their replacement values
            context_values: Dictionary of context keys and their values
            
        Returns:
            Template with placeholders replaced
        """
        result = template_content
        
        # Replace regular placeholders (format: {{ placeholder_name }})
        for key, value in placeholders.items():
            placeholder_pattern = r'\{\{\s*' + re.escape(key) + r'\s*\}\}'
            result = re.sub(placeholder_pattern, str(value), result)
        
        # Replace context placeholders (format: {{ context.key_name }})
        for key, value in context_values.items():
            context_placeholder_pattern = r'\{\{\s*context\.' + re.escape(key) + r'\s*\}\}'
            result = re.sub(context_placeholder_pattern, str(value), result)
            
        return result
    
    def _get_next_sequence_number(self) -> int:
        """Get the next sequential number for file naming."""
        if not self.output_dir.exists():
            return 1
        
        # Find all existing files with sequential numbering (format: 001-feature-name.md)
        existing_files = list(self.output_dir.glob("*.md"))
        max_number = 0
        
        for file_path in existing_files:
            # Only look for files that match our sequential numbering pattern
            match = re.match(r'^(\d{3})-', file_path.name)
            if match:
                number = int(match.group(1))
                max_number = max(max_number, number)
        
        # If no sequential files exist, start at 1
        return max_number + 1
    
    def _slugify(self, text: str) -> str:
        """Convert text to a URL-friendly slug."""
        if not text:
            return "untitled-feature"
        
        # Convert to lowercase and replace spaces with hyphens
        slug = text.lower()
        # Remove or replace special characters
        slug = re.sub(r'[^\w\s-]', '', slug)
        # Replace multiple spaces/hyphens with single hyphen
        slug = re.sub(r'[-\s]+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        # Limit length to reasonable size
        slug = slug[:50]
        
        return slug if slug else "untitled-feature"
    
    def _extract_title_from_content(self, content: str) -> str:
        """Extract a title from the generated content."""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            # Look for markdown headers
            if line.startswith('# '):
                title = line.replace('#', '').strip()
                if title and len(title) > 3:  # Avoid very short titles
                    return title
            # Look for "Development Task:" pattern
            elif 'Development Task:' in line:
                title = line.split('Development Task:')[-1].strip()
                if title:
                    return title
        return ""
    
    def _clean_llm_output(self, content: str) -> str:
        """Remove unwanted markdown code block markers from LLM output."""
        # Remove opening code block markers
        content = re.sub(r'^```\w*\n?', '', content, flags=re.MULTILINE)
        # Remove closing code block markers
        content = re.sub(r'\n?```\s*$', '', content, flags=re.MULTILINE)
        # Clean up any extra whitespace
        content = content.strip()
        return content

    def execute(self, task_description: str, *args, **kwargs) -> str:
        """
        Execute the prompt assembly process.
        
        Like other agents, this loads a template, populates it with context, and uses LLM to generate final output.
        
        Args:
            task_description: The task description to work with
            
        Returns:
            LLM-generated final prompt/output based on template and all gathered context
        """
        try:
            # Load the default template
            template_content = self._load_template('example_template.md')
            
            # Gather all available context automatically
            all_context = {}
            if self.context_manager is not None:
                for key in self.context_manager.keys():
                    value = self.context_manager.get(key)
                    if value is not None:
                        all_context[key] = str(value)
            
            # Create context section from all available context
            context_section = ""
            for key, value in all_context.items():
                readable_key = key.replace('_', ' ').title()
                context_section += f"\n## {readable_key}\n{value}\n"
            
            # Prepare the prompt with task and all context
            full_prompt = f"""
                Task: {task_description}

                Available Context:
                {context_section}

                Template Instructions:
                {template_content}

                Based on the task description and all the available context above, generate a comprehensive final output that synthesizes all the information and provides actionable guidance.
                """
                        
            # Use LLM to generate final assembled output
            if self.llm_manager:
                try:
                    raw_result = self.llm_manager.execute(
                        full_prompt, 
                        agent_name="prompt_assembly_agent"
                    )
                    
                    # Clean the output to remove code block markers
                    final_result = self._clean_llm_output(raw_result)
                    
                    # Create output directory
                    self.output_dir.mkdir(exist_ok=True)
                    
                    # Generate filename with sequential numbering
                    sequence_number = self._get_next_sequence_number()
                    title = self._extract_title_from_content(final_result)
                    
                    # Fallback to task description if no title found
                    if not title:
                        title = task_description
                    
                    slug = self._slugify(title)
                    filename = f"{sequence_number:03d}-{slug}.md"
                    output_file = self.output_dir / filename
                    
                    # Write to file
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(final_result)
                    
                    print(f"Development specification saved to: {output_file}")
                    
                    # Store the result in context manager
                    if self.context_manager is not None:
                        self.context_manager.set('assembled_prompt', final_result)
                        self.context_manager.set('output_file_path', str(output_file))
                    
                    return str(output_file)
                    
                except Exception as e:
                    error_msg = f"LLM assembly failed: {e}"
                    
                    # Fallback to basic template result but still save to file
                    basic_result = f"# Task: {task_description}\n\n## Error\nLLM assembly failed: {e}\n\n## Context Summary\n{context_section}"
                    
                    # Create output directory and save fallback result
                    self.output_dir.mkdir(exist_ok=True)
                    sequence_number = self._get_next_sequence_number()
                    slug = self._slugify(task_description)
                    filename = f"{sequence_number:03d}-{slug}-error.md"
                    output_file = self.output_dir / filename
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(basic_result)
                    
                    print(f"Fallback specification saved to: {output_file}")
                    
                    if self.context_manager is not None:
                        self.context_manager.set('assembled_prompt', basic_result)
                        self.context_manager.set('prompt_assembly_error', error_msg)
                        self.context_manager.set('output_file_path', str(output_file))
                    
                    return str(output_file)
            else:
                # No LLM available - create basic assembly but still save to file
                basic_result = f"# Task: {task_description}\n\n## Notice\nNo LLM available for detailed analysis.\n\n## Context Summary\n{context_section}"
                
                # Create output directory and save basic result
                self.output_dir.mkdir(exist_ok=True)
                sequence_number = self._get_next_sequence_number()
                slug = self._slugify(task_description)
                filename = f"{sequence_number:03d}-{slug}-basic.md"
                output_file = self.output_dir / filename
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(basic_result)
                
                print(f"Basic specification saved to: {output_file}")
                
                if self.context_manager is not None:
                    self.context_manager.set('assembled_prompt', basic_result)
                    self.context_manager.set('output_file_path', str(output_file))
                
                return str(output_file)
            
        except Exception as e:
            error_msg = f"Prompt assembly failed: {e}"
            
            if self.context_manager is not None:
                self.context_manager.set('prompt_assembly_error', error_msg)
            
            return error_msg