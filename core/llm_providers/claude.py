import os
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from .base import LLMProvider


class ClaudeProvider(LLMProvider):
    """
    Anthropic Claude provider implementation.
    """
    
    def __init__(self, api_key: str, **kwargs):
        self.default_model = kwargs.get('model', 'claude-3-opus-20240229')
        super().__init__(api_key, **kwargs)
    
    def authenticate(self) -> None:
        """
        Authenticate with Anthropic API.
        """
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
            # Test the connection by making a minimal request
            self.client.messages.create(
                model=self.default_model,
                max_tokens=1,
                messages=[{"role": "user", "content": "test"}]
            )
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic")
        except Exception as e:
            raise ValueError(f"Failed to authenticate with Anthropic: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,))
    )
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate a response using Anthropic's Claude API.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters like model, max_tokens, temperature, etc.
            
        Returns:
            The generated response text
        """
        try:
            # Extract parameters with defaults
            model = kwargs.get('model', self.default_model)
            max_tokens = kwargs.get('max_tokens', 4096)
            temperature = kwargs.get('temperature', 0.7)
            
            # Make the API call
            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
            
        except Exception as e:
            print(f"Error generating response from Claude: {e}")
            raise RuntimeError(f"Claude API call failed: {str(e)}")
    
    def get_model_name(self) -> str:
        """
        Get the default model name for Claude.
        
        Returns:
            The default model name
        """
        return self.default_model
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate Claude-specific configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if valid, False otherwise
        """
        # Check for valid model names
        valid_models = [
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229', 
            'claude-3-haiku-20240307',
            'claude-2.1',
            'claude-2.0',
            'claude-instant-1.2'
        ]
        
        model = config.get('model', self.default_model)
        if model not in valid_models:
            return False
        
        # Validate temperature range
        temperature = config.get('temperature', 0.7)
        if not (0.0 <= temperature <= 1.0):
            return False
        
        # Validate max_tokens
        max_tokens = config.get('max_tokens', 4096)
        if not isinstance(max_tokens, int) or max_tokens < 1:
            return False
            
        return True