from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    Defines the common interface that all LLM providers must implement.
    """
    
    def __init__(self, api_key: str, **kwargs):
        """
        Initialize the LLM provider with API key and configuration.
        
        Args:
            api_key: The API key for the LLM provider
            **kwargs: Additional configuration parameters
        """
        self.api_key = api_key
        self.config = kwargs
        self.authenticate()
    
    @abstractmethod
    def authenticate(self) -> None:
        """
        Authenticate with the LLM provider using the API key.
        Should raise an exception if authentication fails.
        """
        pass
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the LLM provider.
        
        Args:
            prompt: The input prompt to send to the LLM
            **kwargs: Additional generation parameters (model, temperature, etc.)
            
        Returns:
            The generated response as a string
            
        Raises:
            Exception: If the API call fails or returns an error
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """
        Get the default model name for this provider.
        
        Returns:
            The model name as a string
        """
        pass
    
    def handle_rate_limit(self) -> None:
        """
        Handle rate limiting for API calls.
        Base implementation does nothing - providers can override if needed.
        """
        pass
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate the configuration parameters for this provider.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            True if configuration is valid, False otherwise
        """
        return True