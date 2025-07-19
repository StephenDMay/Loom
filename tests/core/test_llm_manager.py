import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Mock google.generativeai before importing LLMManager
with patch.dict('sys.modules', {'google.generativeai': MagicMock()}):
    from core.llm_manager import LLMManager
    from core.config_manager import ConfigManager

class TestLLMManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_config_manager = Mock(spec=ConfigManager)
        self.mock_config_manager.get.side_effect = self._mock_config_get
        
    def _mock_config_get(self, key, default=None):
        """Mock config values for testing."""
        config_values = {
            "llm_settings.default_provider": "gemini",
            "llm_settings.model": "gemini-pro",
            "llm_settings.temperature": 0.7,
            "llm_settings.max_tokens": 8192,
            "llm_settings.top_p": 0.8,
            "llm_settings.top_k": 40,
            "llm_settings.output_format": "structured",
            "llm_settings.research_depth": "standard"
        }
        return config_values.get(key, default)
    
    def test_llm_manager_initialization(self):
        """Test that LLMManager can be initialized with a ConfigManager."""
        with patch('core.llm_manager.LLMManager._initialize_client'):
            llm_manager = LLMManager(self.mock_config_manager)
            self.assertEqual(llm_manager.config_manager, self.mock_config_manager)
            self.assertEqual(llm_manager.provider, "gemini")
    
    def test_get_default_provider(self):
        """Test getting the default provider from configuration."""
        with patch('core.llm_manager.LLMManager._initialize_client'):
            llm_manager = LLMManager(self.mock_config_manager)
            provider = llm_manager._get_default_provider()
            self.assertEqual(provider, "gemini")
    
    def test_get_provider(self):
        """Test the get_provider method."""
        with patch('core.llm_manager.LLMManager._initialize_client'):
            llm_manager = LLMManager(self.mock_config_manager)
            self.assertEqual(llm_manager.get_provider(), "gemini")
    
    def test_get_config(self):
        """Test the get_config method returns expected configuration."""
        with patch('core.llm_manager.LLMManager._initialize_client'):
            llm_manager = LLMManager(self.mock_config_manager)
            config = llm_manager.get_config()
            
            expected_config = {
                "provider": "gemini",
                "temperature": 0.7,
                "output_format": "structured",
                "research_depth": "standard"
            }
            self.assertEqual(config, expected_config)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_api_key'})
    @patch('builtins.__import__')
    def test_initialize_gemini_client(self, mock_import):
        """Test Gemini client initialization with API key."""
        # Mock the google.generativeai module
        mock_genai = Mock()
        mock_model_instance = Mock()
        mock_genai.GenerativeModel.return_value = mock_model_instance
        
        def side_effect(name, *args, **kwargs):
            if name == 'google.generativeai':
                return mock_genai
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = side_effect
        
        llm_manager = LLMManager(self.mock_config_manager)
        
        mock_genai.configure.assert_called_once_with(api_key='test_api_key')
        mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
        self.assertEqual(llm_manager.client, mock_model_instance)
    
    def test_initialize_gemini_client_no_api_key(self):
        """Test that missing API key raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with patch('core.llm_manager.LLMManager._get_default_provider', return_value='gemini'):
                with patch('core.llm_manager.LLMManager._initialize_gemini_client', side_effect=ValueError("GEMINI_API_KEY environment variable not set")):
                    with self.assertRaises(RuntimeError) as context:
                        LLMManager(self.mock_config_manager)
                    self.assertIn("Failed to initialize LLM client", str(context.exception))
    
    @patch('core.llm_manager.LLMManager._initialize_client')
    def test_execute_llm_call_empty_prompt(self, mock_init):
        """Test that empty prompt raises ValueError."""
        llm_manager = LLMManager(self.mock_config_manager)
        
        with self.assertRaises(ValueError) as context:
            llm_manager.execute_llm_call("")
        self.assertIn("Prompt cannot be empty", str(context.exception))
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_api_key'})
    @patch('builtins.__import__')
    def test_execute_llm_call_success(self, mock_import):
        """Test successful LLM call execution."""
        # Setup mock response
        mock_response = Mock()
        mock_response.text = "Test response"
        
        # Mock the google.generativeai module
        mock_genai = Mock()
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model_instance
        
        def side_effect(name, *args, **kwargs):
            if name == 'google.generativeai':
                return mock_genai
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = side_effect
        
        llm_manager = LLMManager(self.mock_config_manager)
        result = llm_manager.execute_llm_call("Test prompt")
        
        self.assertEqual(result, "Test response")
        mock_model_instance.generate_content.assert_called_once()
    
    def test_unsupported_provider(self):
        """Test that unsupported provider raises ValueError."""
        self.mock_config_manager.get.side_effect = lambda key, default=None: "unsupported_provider" if "default_provider" in key else default
        
        with patch('core.llm_manager.LLMManager._initialize_client', side_effect=ValueError("Unsupported LLM provider: unsupported_provider")):
            with self.assertRaises(RuntimeError) as context:
                LLMManager(self.mock_config_manager)
            self.assertIn("Failed to initialize LLM client", str(context.exception))

    def test_resolve_configuration_global_defaults(self):
        """Test configuration resolution with only global defaults."""
        llm_manager = LLMManager(self.mock_config_manager)
        
        config = llm_manager._resolve_configuration()
        
        expected_config = {
            'provider': 'gemini',
            'model': 'gemini-pro',
            'temperature': 0.7,
            'max_tokens': 8192,
            'top_p': 0.8,
            'top_k': 40,
        }
        
        for key, expected_value in expected_config.items():
            self.assertEqual(config[key], expected_value)

    def test_resolve_configuration_agent_specific(self):
        """Test configuration resolution with agent-specific configuration."""
        # Mock agent config
        agent_config = {
            'llm': {
                'provider': 'claude',
                'model': 'claude-3-5-sonnet-20241022',
                'temperature': 0.3,
                'max_tokens': 2048
            }
        }
        self.mock_config_manager.get_agent_config.return_value = agent_config
        
        llm_manager = LLMManager(self.mock_config_manager)
        config = llm_manager._resolve_configuration(agent_name="test_agent")
        
        # Agent-specific values should override defaults
        self.assertEqual(config['provider'], 'claude')
        self.assertEqual(config['model'], 'claude-3-5-sonnet-20241022')
        self.assertEqual(config['temperature'], 0.3)
        self.assertEqual(config['max_tokens'], 2048)
        
        # Verify get_agent_config was called
        self.mock_config_manager.get_agent_config.assert_called_once_with("test_agent")

    def test_resolve_configuration_explicit_parameters(self):
        """Test configuration resolution with explicit parameters (highest priority)."""
        # Mock agent config
        agent_config = {
            'llm': {
                'provider': 'claude',
                'model': 'claude-3-5-sonnet-20241022',
                'temperature': 0.3
            }
        }
        self.mock_config_manager.get_agent_config.return_value = agent_config
        
        llm_manager = LLMManager(self.mock_config_manager)
        
        # Explicit parameters should override everything
        config = llm_manager._resolve_configuration(
            agent_name="test_agent",
            provider="gemini",
            temperature=0.1,
            max_tokens=1024
        )
        
        self.assertEqual(config['provider'], 'gemini')
        self.assertEqual(config['model'], 'claude-3-5-sonnet-20241022')  # From agent config
        self.assertEqual(config['temperature'], 0.1)
        self.assertEqual(config['max_tokens'], 1024)

    def test_resolve_configuration_agent_config_error(self):
        """Test configuration resolution when agent config loading fails."""
        # Mock agent config to raise exception
        self.mock_config_manager.get_agent_config.side_effect = Exception("Config not found")
        
        llm_manager = LLMManager(self.mock_config_manager)
        config = llm_manager._resolve_configuration(agent_name="test_agent")
        
        # Should fall back to global defaults
        self.assertEqual(config['provider'], 'gemini')
        self.assertEqual(config['temperature'], 0.7)

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_api_key'})
    @patch('builtins.__import__')
    def test_execute_with_agent_name(self, mock_import):
        """Test execute method with agent_name parameter."""
        # Setup mock response
        mock_response = Mock()
        mock_response.text = "Agent-specific response"
        
        # Mock the google.generativeai module
        mock_genai = Mock()
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model_instance
        
        def side_effect(name, *args, **kwargs):
            if name == 'google.generativeai':
                return mock_genai
            return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = side_effect
        
        # Mock agent config
        agent_config = {
            'llm': {
                'temperature': 0.2,
                'max_tokens': 1024
            }
        }
        self.mock_config_manager.get_agent_config.return_value = agent_config
        
        llm_manager = LLMManager(self.mock_config_manager)
        result = llm_manager.execute("Test prompt", agent_name="test_agent")
        
        self.assertEqual(result, "Agent-specific response")
        
        # Verify the call was made with agent-specific config
        call_args = mock_model_instance.generate_content.call_args
        generation_config = call_args[1]['generation_config']
        self.assertEqual(generation_config['temperature'], 0.2)
        self.assertEqual(generation_config['max_output_tokens'], 1024)

    @patch('core.llm_manager.LLMManager._initialize_client')
    def test_execute_llm_call_backward_compatibility(self, mock_init):
        """Test that legacy execute_llm_call method still works."""
        with patch('core.llm_manager.LLMManager.execute') as mock_execute:
            mock_execute.return_value = "Test response"
            
            llm_manager = LLMManager(self.mock_config_manager)
            result = llm_manager.execute_llm_call("Test prompt", temperature=0.5)
            
            self.assertEqual(result, "Test response")
            mock_execute.assert_called_once_with("Test prompt", temperature=0.5)

if __name__ == '__main__':
    unittest.main()