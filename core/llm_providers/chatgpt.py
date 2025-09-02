import os
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from .base import LLMProvider


class ChatGPTProvider(LLMProvider):
    """
    OpenAI ChatGPT provider implementation.
    """
    
    def __init__(self, api_key: str, **kwargs):
        self.default_model = kwargs.get('model', 'gpt-3.5-turbo')
        super().__init__(api_key, **kwargs)
    
    def authenticate(self) -> None:
        """
        Authenticate with OpenAI API.
        """
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
            # Test the connection by listing models
            list(self.client.models.list())
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")
        except Exception as e:
            raise ValueError(f"Failed to authenticate with OpenAI: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,))
    )
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate a response using OpenAI's ChatGPT API.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters like model, temperature, max_tokens, etc.
            
        Returns:
            The generated response text
        """
        try:
            # Extract parameters with defaults
            model = kwargs.get('model', self.default_model)
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 4096)
            top_p = kwargs.get('top_p', 1.0)
            
            # Prepare the messages
            messages = [{"role": "user", "content": prompt}]
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating response from ChatGPT: {e}")
            raise RuntimeError(f"ChatGPT API call failed: {str(e)}")
    
    def get_model_name(self) -> str:
        """
        Get the default model name for ChatGPT.
        
        Returns:
            The default model name
        """
        return self.default_model
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate ChatGPT-specific configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if valid, False otherwise
        """
        # Check for valid model names
        valid_models = [
            'gpt-3.5-turbo',
            'gpt-3.5-turbo-16k',
            'gpt-4',
            'gpt-4-32k',
            'gpt-4-turbo-preview',
            'gpt-4-vision-preview'
        ]
        
        model = config.get('model', self.default_model)
        if model not in valid_models:
            return False
        
        # Validate temperature range
        temperature = config.get('temperature', 0.7)
        if not (0.0 <= temperature <= 2.0):
            return False
        
        # Validate max_tokens
        max_tokens = config.get('max_tokens', 4096)
        if not isinstance(max_tokens, int) or max_tokens < 1:
            return False
            
        return True