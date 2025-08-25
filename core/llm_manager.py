import os
from typing import Optional, Dict, Any
from core.config_manager import ConfigManager

class LLMManager:
    """
    Centralized manager for Large Language Model interactions using API-only approach.
    """
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def execute(self, prompt: str, agent_name: str = None, provider: str = None, 
                temperature: float = None, **kwargs) -> str:
        """
        Execute an LLM call with the given prompt and optional agent-specific configuration.
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        
        resolved_config = self._resolve_configuration(agent_name, provider, temperature, **kwargs)
        
        return self._execute_api_call(prompt, resolved_config)

    def _execute_api_call(self, prompt: str, config: Dict[str, Any]) -> str:
        """Execute LLM call using API."""
        provider = config['provider']
        
        if provider == "gemini":
            return self._execute_gemini_api(prompt, config)
        else:
            raise ValueError(f"Unsupported provider: {provider}. Only 'gemini' is supported.")

    def _execute_gemini_api(self, prompt: str, config: Dict[str, Any]) -> str:
        """Execute Gemini API call."""
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("google-generativeai package not installed. Install with: pip install google-generativeai")

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        
        generation_config = {
            'temperature': config.get('temperature', 0.7),
            'top_p': config.get('top_p', 0.8),
            'top_k': config.get('top_k', 40),
            'max_output_tokens': config.get('max_tokens', 8192),
        }
        
        model_name = config.get('model', 'gemini-2.0-flash-exp')
        model = genai.GenerativeModel(model_name)
        
        print(f"Executing LLM call with Gemini model: {model_name}")
        
        try:
            response = model.generate_content(prompt, generation_config=generation_config)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {str(e)}")

    def _resolve_configuration(self, agent_name: str = None, provider: str = None, 
                              temperature: float = None, **kwargs) -> Dict[str, Any]:
        """
        Resolve LLM configuration with proper precedence:
        1. Hardcoded defaults (lowest priority)
        2. Global LLM settings from dev-automation.config.json
        3. Agent-specific configuration from agent's config.json
        4. Explicit parameters passed to execute method (highest priority)
        """
        # 1. Start with hardcoded defaults
        config = {
            'provider': "gemini",
            'model': "gemini-2.0-flash-exp", 
            'temperature': 0.7,
            'max_tokens': 8192,
        }
        
        # 2. Apply global LLM settings from dev-automation.config.json
        global_llm_config = {
            'provider': self.config_manager.get("llm_settings.default_provider"),
            'model': self.config_manager.get("llm_settings.model"),
            'temperature': self.config_manager.get("llm_settings.temperature"),
            'max_tokens': self.config_manager.get("llm_settings.max_tokens"),
            'top_p': self.config_manager.get("llm_settings.top_p"),
            'top_k': self.config_manager.get("llm_settings.top_k"),
        }
        # Only update with non-None values from global config
        for key, value in global_llm_config.items():
            if value is not None:
                config[key] = value
        
        # 3. Apply agent-specific configuration
        if agent_name:
            try:
                agent_config = self.config_manager.get_agent_config(agent_name)
                agent_llm_config = agent_config.get('llm', {})
                config.update(agent_llm_config)
            except Exception:
                # If agent config can't be loaded, fall back to current config
                pass
        
        # 4. Apply explicit parameters (highest priority)
        if provider is not None:
            config['provider'] = provider
        if temperature is not None:
            config['temperature'] = temperature
        
        # Apply any additional keyword arguments
        config.update(kwargs)
        return config

    def get_available_providers(self) -> Dict[str, bool]:
        """Get list of providers and their availability status."""
        return {
            "gemini": self._validate_gemini_availability()
        }

    def _validate_gemini_availability(self) -> bool:
        """Check if Gemini API is available."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return False
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            # Try to list models to validate API key works
            list(genai.list_models())
            return True
        except Exception:
            return False

    def validate_config(self) -> Dict[str, Any]:
        """Validate current configuration and provider availability."""
        default_provider = self.config_manager.get("llm_settings.default_provider", "gemini")
        provider_status = self.get_available_providers()
        
        return {
            "default_provider": default_provider,
            "available_providers": provider_status,
            "default_provider_available": provider_status.get(default_provider, False)
        }