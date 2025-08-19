import os
import re
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
            raise FileNotFoundError(f"Template file not found: {template_file_path}")
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

    def execute(self, template_name: str, placeholders: Optional[Dict[str, str]] = None, context_keys: Optional[List[str]] = None, *args, **kwargs) -> str:
        """
        Execute the prompt assembly process.
        
        Args:
            template_name: Name of the template to load
            placeholders: Dictionary of placeholder keys and their replacement values
            context_keys: List of context keys to retrieve and inject
            
        Returns:
            Fully assembled prompt as a string
            
        Raises:
            FileNotFoundError: If template doesn't exist
            Exception: If assembly process fails
        """
        try:
            # Set defaults
            placeholders = placeholders or {}
            context_keys = context_keys or []
            
            # Load the template
            template_content = self._load_template(template_name)
            
            # Get context values
            context_values = self._get_context_values(context_keys)
            
            # Replace placeholders and context
            assembled_prompt = self._replace_placeholders(template_content, placeholders, context_values)
            
            # Store the result in context manager if available
            if self.context_manager is not None:
                self.context_manager.set('assembled_prompt', assembled_prompt)
                self.context_manager.set('last_template_used', template_name)
            
            return assembled_prompt
            
        except Exception as e:
            error_msg = f"Prompt assembly failed: {e}"
            
            if self.context_manager is not None:
                self.context_manager.set('prompt_assembly_error', error_msg)
            
            raise Exception(error_msg)