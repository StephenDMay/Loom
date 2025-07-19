import os
from typing import Optional, Dict, Any
from core.config_manager import ConfigManager

class LLMManager:
    """
    Centralized manager for all Large Language Model interactions.
    Provides a unified interface for different LLM providers.
    """
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the LLMManager with configuration.
        
        Args:
            config_manager: ConfigManager instance for accessing LLM settings
        """
        self.config_manager = config_manager
        self.provider = self._get_default_provider()
        self.client = None
        self._client_initialized = False
    
    def _get_default_provider(self) -> str:
        """Get the default LLM provider from configuration."""
        return self.config_manager.get("llm_settings.default_provider", "gemini")
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client based on the provider."""
        if self.provider == "gemini":
            return self._initialize_gemini_client()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _initialize_gemini_client(self):
        """Initialize Gemini client."""
        try:
            import google.generativeai as genai
            
            # Get API key from environment variable
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set")
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            return model
        except ImportError:
            raise ImportError("google-generativeai package not installed. Install with: pip install google-generativeai")
    
    def _ensure_client_initialized(self):
        """Lazy initialization of the LLM client."""
        if not self._client_initialized:
            try:
                self.client = self._initialize_client()
                self._client_initialized = True
            except (ImportError, ValueError) as e:
                raise RuntimeError(f"Failed to initialize LLM client: {str(e)}")

    def execute_llm_call(self, prompt: str, temperature: Optional[float] = None) -> str:
        """
        Execute an LLM call with the given prompt.
        
        Args:
            prompt: The input prompt for the LLM
            temperature: Optional temperature override for this call
            
        Returns:
            The LLM's response as a string
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        
        # Ensure client is initialized before making calls
        self._ensure_client_initialized()
        
        # Use provided temperature or fall back to config default
        if temperature is None:
            temperature = self.config_manager.get("llm_settings.temperature", 0.7)
        
        try:
            if self.provider == "gemini":
                return self._execute_gemini_call(prompt, temperature)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}")
    
    def _execute_gemini_call(self, prompt: str, temperature: float) -> str:
        """Execute a call to Gemini."""
        generation_config = {
            'temperature': temperature,
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 8192,
        }
        
        response = self.client.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return response.text
    
    def get_provider(self) -> str:
        """Get the current LLM provider."""
        return self.provider
    
    def get_config(self) -> Dict[str, Any]:
        """Get current LLM configuration."""
        return {
            "provider": self.provider,
            "temperature": self.config_manager.get("llm_settings.temperature", 0.7),
            "output_format": self.config_manager.get("llm_settings.output_format", "structured"),
            "research_depth": self.config_manager.get("llm_settings.research_depth", "standard")
        }