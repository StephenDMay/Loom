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
        self._client_initialized = False
    
    def _get_default_provider(self) -> str:
        """Get the default LLM provider from configuration."""
        return self.config_manager.get("llm_settings.default_provider", "gemini")
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client based on the provider."""
        if self.provider == "gemini":
            self._initialize_gemini_client()
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
        except ImportError:
            raise ImportError("google-generativeai package not installed. Install with: pip install google-generativeai")
    
    def _ensure_client_initialized(self):
        """Lazy initialization of the LLM client."""
        if not self._client_initialized:
            try:
                self._initialize_client()
                self._client_initialized = True
            except (ImportError, ValueError) as e:
                raise RuntimeError(f"Failed to initialize LLM client: {str(e)}")

    def execute(self, prompt: str, agent_name: str = None, provider: str = None, 
                model: str = None, temperature: float = None, max_tokens: int = None, **kwargs) -> str:
        """
        Execute an LLM call with the given prompt and optional agent-specific configuration.
        
        Args:
            prompt: The input prompt for the LLM
            agent_name: Optional agent name to load agent-specific LLM configuration
            provider: Optional provider override
            model: Optional model override
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            **kwargs: Additional parameters for the LLM call
            
        Returns:
            The LLM's response as a string
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        
        # Resolve configuration in order of precedence:
        # 1. Explicit parameters (highest priority)
        # 2. Agent-specific configuration
        # 3. Global default configuration (lowest priority)
        resolved_config = self._resolve_configuration(agent_name, provider, model, temperature, max_tokens, **kwargs)
        
        # Set provider for this call
        call_provider = resolved_config.get('provider', self.provider)
        
        # Ensure client is initialized before making calls
        self._ensure_client_initialized()
        
        try:
            if call_provider == "gemini":
                return self._execute_gemini_call(prompt, resolved_config)
            else:
                raise ValueError(f"Unsupported provider: {call_provider}")
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}")

    def execute_llm_call(self, prompt: str, temperature: Optional[float] = None) -> str:
        """
        Legacy method for backward compatibility.
        
        Args:
            prompt: The input prompt for the LLM
            temperature: Optional temperature override for this call
            
        Returns:
            The LLM's response as a string
        """
        return self.execute(prompt, temperature=temperature)
    
    def _resolve_configuration(self, agent_name: str = None, provider: str = None, 
                              model: str = None, temperature: float = None, 
                              max_tokens: int = None, **kwargs) -> Dict[str, Any]:
        """
        Resolve LLM configuration in order of precedence:
        1. Explicit parameters (highest priority)
        2. Agent-specific configuration
        3. Global default configuration (lowest priority)
        """
        # Start with global defaults
        config = {
            'provider': self.config_manager.get("llm_settings.default_provider", "gemini"),
            'model': self.config_manager.get("llm_settings.model", "gemini-2.5-pro"),
            'temperature': self.config_manager.get("llm_settings.temperature", 0.7),
            'max_tokens': self.config_manager.get("llm_settings.max_tokens", 8192),
            'top_p': self.config_manager.get("llm_settings.top_p", 0.8),
            'top_k': self.config_manager.get("llm_settings.top_k", 40),
        }
        
        # Override with agent-specific configuration if agent_name is provided
        if agent_name:
            try:
                agent_config = self.config_manager.get_agent_config(agent_name)
                if 'llm' in agent_config:
                    llm_config = agent_config['llm']
                    for key in ['provider', 'model', 'temperature', 'max_tokens', 'top_p', 'top_k']:
                        if key in llm_config:
                            config[key] = llm_config[key]
            except Exception:
                # If agent config can't be loaded, fall back to global defaults
                pass
        
        # Override with explicit parameters (highest priority)
        if provider is not None:
            config['provider'] = provider
        if model is not None:
            config['model'] = model
        if temperature is not None:
            config['temperature'] = temperature
        if max_tokens is not None:
            config['max_tokens'] = max_tokens
        
        # Add any additional kwargs
        config.update(kwargs)
        
        return config

    def _execute_gemini_call(self, prompt: str, config: Dict[str, Any]) -> str:
        """Execute a call to Gemini with the resolved configuration."""
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("google-generativeai package not installed. Install with: pip install google-generativeai")

        generation_config = {
            'temperature': config.get('temperature', 0.7),
            'top_p': config.get('top_p', 0.8),
            'top_k': config.get('top_k', 40),
            'max_output_tokens': config.get('max_tokens', 8192),
        }
        
        model_name = config.get('model', 'gemini-1.0-pro')
        model = genai.GenerativeModel(model_name)
        
        response = model.generate_content(
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

llm_manager = LLMManager(ConfigManager())
