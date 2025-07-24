import os
from pathlib import Path
from typing import Dict, Optional, TYPE_CHECKING
from agents.base_agent import BaseAgent

if TYPE_CHECKING:
    from core.llm_manager import LLMManager
    from core.context_manager import ContextManager


class FeatureResearchAgent(BaseAgent):
    """
    An agent that analyzes feature requests and generates comprehensive research and implementation specifications.
    """
    
    def __init__(self, config: Optional[Dict] = None, llm_manager: Optional['LLMManager'] = None, context_manager: Optional['ContextManager'] = None):
        super().__init__(config, llm_manager, context_manager)
        
        # Get template path from config
        self.template_path = self.config.get('feature_research_agent', {}).get('template_path', 'templates/feature_research_template.md')

    def _load_template(self) -> str:
        """Load the feature research template from file."""
        template_file_path = Path(__file__).parent / self.template_path
        
        try:
            with open(template_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {template_file_path}")
        except Exception as e:
            raise Exception(f"Error loading template: {e}")
    
    def _discover_available_context(self) -> Dict[str, str]:
        """Discover and gather available context from the ContextManager.
        
        Returns:
            Dict containing available context data with descriptive keys
        """
        context_data = {}
        
        if self.context_manager is None:
            return context_data
        
        # Dynamically discover all available context keys using the keys() method
        all_context_keys = list(self.context_manager.keys())
        
        for key in all_context_keys:
            value = self.context_manager.get(key)
            if value is not None and str(value).strip():  # Only include non-empty values
                # Create a more readable key name for the template
                readable_key = key.replace('_', ' ').title()
                context_data[readable_key] = str(value)
        
        return context_data
    
    def _render_template(self, template_content: str, feature_request: str, available_context: Dict[str, str]) -> str:
        """Render the template with feature request and context data.
        
        Args:
            template_content: The raw template content
            feature_request: The feature description 
            available_context: Dictionary of context data
            
        Returns:
            Rendered template as string
        """
        # Replace the feature request placeholder
        rendered = template_content.replace('{{ feature_request }}', feature_request)
        
        # Handle the context loop - this is a simple implementation
        context_section = ""
        if available_context:
            for key, value in available_context.items():
                if value and value.strip():  # Only include non-empty values
                    context_section += f"\n### {key}\n{value}\n"
        
        # Replace the context loop with the generated context section
        # Look for the pattern between {% for key, value in available_context.items() %} and {% endfor %}
        import re
        context_pattern = r'{%\s*for\s+key,\s*value\s+in\s+available_context\.items\(\)\s*%}.*?{%\s*endfor\s*%}'
        rendered = re.sub(context_pattern, context_section, rendered, flags=re.DOTALL)
        
        return rendered

    def execute(self, feature_description: str, *args, **kwargs) -> str:
        """
        Execute the feature research analysis.
        
        Args:
            feature_description: The feature description to analyze
            
        Returns:
            A string containing the populated template with the feature description and context
        """
        
        try:
            # Load the template
            template_content = self._load_template()
            
            # Discover available context
            available_context = self._discover_available_context()
            
            # Render template with simple string replacement approach
            populated_template = self._render_template(template_content, feature_description, available_context)
            
            # Store the result in context manager if available
            if self.context_manager is not None:
                self.context_manager.set('feature_research_result', populated_template)
            
            return populated_template
            
        except Exception as e:
            error_msg = f"Feature research failed: {e}"
            
            if self.context_manager is not None:
                self.context_manager.set('feature_research_error', error_msg)
            
            return error_msg