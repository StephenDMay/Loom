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

    def execute(self, feature_description: str, *args, **kwargs) -> str:
        """
        Execute the feature research analysis.
        
        Args:
            feature_description: The feature description to analyze
            
        Returns:
            A string containing the populated template with the feature description
        """
        
        try:
            # Load the template
            template_content = self._load_template()
            
            # For the minimal implementation, we'll just replace the placeholder
            # with the feature description
            populated_template = template_content.replace('[USER_INPUT_PLACEHOLDER]', feature_description)
            
            # Store the result in context manager if available
            if self.context_manager is not None:
                self.context_manager.set('feature_research_result', populated_template)
            
            return populated_template
            
        except Exception as e:
            error_msg = f"Feature research failed: {e}"
            
            if self.context_manager is not None:
                self.context_manager.set('feature_research_error', error_msg)
            
            return error_msg