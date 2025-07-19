import os
import platform
import subprocess
from typing import Optional, Dict, Any
from core.config_manager import ConfigManager

class LLMManager:
    """
    Centralized manager for Large Language Model interactions using CLI-first approach.
    """
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.execution_mode = config_manager.get("llm_settings.execution_mode", "cli")
        
        # Provider CLI mapping
        self.provider_commands = {
            "gemini": "gemini",
            "claude": "claude"
        }
    
    def execute(self, prompt: str, agent_name: str = None, provider: str = None, 
                temperature: float = None, **kwargs) -> str:
        """
        Execute an LLM call with the given prompt and optional agent-specific configuration.
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        
        resolved_config = self._resolve_configuration(agent_name, provider, temperature, **kwargs)
        
        if self.execution_mode == "api":
            return self._execute_api_call(prompt, resolved_config)
        else:
            return self._execute_cli_call(prompt, resolved_config)

    def _execute_cli_call(self, prompt: str, config: Dict[str, Any]) -> str:
        """Execute LLM call using CLI tools."""
        provider = config['provider']
        
        if provider not in self.provider_commands:
            available = ", ".join(self.provider_commands.keys())
            raise ValueError(f"Unsupported provider '{provider}'. Available: {available}")
        
        # Claude doesn't support simple stdin/stdout like Gemini, so use API mode
        if provider == "claude":
            print("Note: Claude CLI doesn't support simple prompt mode, using API...")
            return self._execute_api_call(prompt, config)
        
        cmd = self.provider_commands[provider]
        
        # Handle Windows .cmd extension for npm-installed tools
        if platform.system() == "Windows" and provider == "gemini":
            cmd += ".cmd"
        
        try:
            # Check if provider is available
            if not self._validate_provider_availability(provider):
                self._prompt_user_for_missing_provider(provider)
                raise RuntimeError(f"Provider '{provider}' is not available")
            
            print(f"Executing LLM call with provider: {provider}")
            
            result = subprocess.run(
                [cmd],
                input=prompt,
                text=True,
                capture_output=True,
                check=True,
                timeout=300  # 5 minute timeout
            )
            
            return result.stdout.strip()
            
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"LLM call timed out after 5 minutes")
        except subprocess.CalledProcessError as e:
            error_msg = f"LLM provider '{provider}' failed with exit code {e.returncode}"
            if e.stderr:
                error_msg += f"\nError details: {e.stderr}"
            raise RuntimeError(error_msg)
        except FileNotFoundError:
            self._prompt_user_for_missing_provider(provider)
            raise RuntimeError(f"LLM provider '{provider}' not found in PATH")

    def _execute_api_call(self, prompt: str, config: Dict[str, Any]) -> str:
        """Execute LLM call using API (future implementation)."""
        provider = config['provider']
        
        if provider == "gemini":
            return self._execute_gemini_api(prompt, config)
        elif provider == "claude":
            return self._execute_claude_api(prompt, config)
        else:
            raise NotImplementedError(f"API mode not yet implemented for provider: {provider}")

    def _execute_claude_api(self, prompt: str, config: Dict[str, Any]) -> str:
        """Execute Claude API call."""
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic")

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        client = anthropic.Anthropic(api_key=api_key)
        
        model_name = config.get('model', 'claude-3-5-sonnet-20241022')
        temperature = config.get('temperature', 0.7)
        max_tokens = config.get('max_tokens', 8192)
        
        # Claude temperature is 0-1, so clamp if necessary
        temperature = min(max(temperature, 0.0), 1.0)
        
        response = client.messages.create(
            model=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text

    def _execute_gemini_api(self, prompt: str, config: Dict[str, Any]) -> str:
        """Execute Gemini API call (existing implementation)."""
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
        
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text

    def _validate_provider_availability(self, provider: str) -> bool:
        """Check if provider CLI tool is available."""
        cmd = self.provider_commands.get(provider)
        if not cmd:
            return False
        
        if platform.system() == "Windows" and provider == "gemini":
            cmd += ".cmd"
        
        try:
            # Try a simple command to check availability
            subprocess.run([cmd, "--help"], capture_output=True, check=True, timeout=10)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _prompt_user_for_missing_provider(self, provider: str):
        """Provide helpful error message for missing provider."""
        install_instructions = {
            "gemini": "Install with: npm install -g @google-ai/generativelanguage-cli",
            "claude": "Install with: npm install -g @anthropic-ai/claude-code"
        }
        
        instruction = install_instructions.get(provider, f"Install {provider} CLI tool")
        
        print(f"\n❌ Error: {provider} CLI tool not found")
        print(f"📦 {instruction}")
        print(f"🔧 Make sure the tool is installed and available in your PATH")
        print(f"💡 You can also switch providers in your dev-automation.config.json")

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
            provider: self._validate_provider_availability(provider)
            for provider in self.provider_commands.keys()
        }

    def validate_config(self) -> Dict[str, Any]:
        """Validate current configuration and provider availability."""
        default_provider = self.config_manager.get("llm_settings.default_provider", "gemini")
        provider_status = self.get_available_providers()
        
        return {
            "default_provider": default_provider,
            "execution_mode": self.execution_mode,
            "available_providers": provider_status,
            "default_provider_available": provider_status.get(default_provider, False)
        }