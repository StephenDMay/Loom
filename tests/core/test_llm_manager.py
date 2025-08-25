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
        self.mock_config_manager.get_agent_config.return_value = {}
        
    def _mock_config_get(self, key, default=None):
        """Mock config values for testing."""
        config_values = {
            "llm_settings.default_provider": "gemini",
            "llm_settings.model": "gemini-2.0-flash-exp",
            "llm_settings.temperature": 0.7,
            "llm_settings.max_tokens": 8192,
            "llm_settings.top_p": 0.8,
            "llm_settings.top_k": 40,
        }
        return config_values.get(key, default)
    
    def test_llm_manager_initialization(self):
        """Test that LLMManager can be initialized with a ConfigManager."""
        llm_manager = LLMManager(self.mock_config_manager)
        self.assertEqual(llm_manager.config_manager, self.mock_config_manager)
    
    def test_execute_empty_prompt(self):
        """Test that empty prompt raises ValueError."""
        llm_manager = LLMManager(self.mock_config_manager)
        
        with self.assertRaises(ValueError) as context:
            llm_manager.execute("")
        
        self.assertIn("Prompt cannot be empty", str(context.exception))
    
    def test_execute_none_prompt(self):
        """Test that None prompt raises ValueError."""
        llm_manager = LLMManager(self.mock_config_manager)
        
        with self.assertRaises(ValueError) as context:
            llm_manager.execute(None)
        
        self.assertIn("Prompt cannot be empty", str(context.exception))
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_api_key'})
    @patch('google.generativeai', new_callable=MagicMock)
    def test_execute_gemini_success(self, mock_genai):
        """Test successful Gemini API call execution."""
        # Set up mock response
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "Test response"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        llm_manager = LLMManager(self.mock_config_manager)
        result = llm_manager.execute("Test prompt")
        
        self.assertEqual(result, "Test response")
        mock_genai.configure.assert_called_once_with(api_key='test_api_key')
        mock_genai.GenerativeModel.assert_called_once_with('gemini-2.0-flash-exp')
        mock_model.generate_content.assert_called_once()
    
    def test_execute_unsupported_provider(self):
        """Test that unsupported provider raises ValueError."""
        llm_manager = LLMManager(self.mock_config_manager)
        
        with self.assertRaises(ValueError) as context:
            llm_manager.execute("Test prompt", provider="unsupported")
        
        self.assertIn("Unsupported provider: unsupported", str(context.exception))
    
    @patch.dict(os.environ, {}, clear=True)
    def test_execute_no_api_key(self):
        """Test that missing API key raises ValueError."""
        llm_manager = LLMManager(self.mock_config_manager)
        
        with self.assertRaises(ValueError) as context:
            llm_manager.execute("Test prompt")
        
        self.assertIn("GEMINI_API_KEY environment variable not set", str(context.exception))
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_api_key'})
    @patch('google.generativeai', new_callable=MagicMock)
    def test_execute_with_custom_temperature(self, mock_genai):
        """Test execute with custom temperature parameter."""
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "Test response"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        llm_manager = LLMManager(self.mock_config_manager)
        result = llm_manager.execute("Test prompt", temperature=0.5)
        
        # Verify the generation config includes custom temperature
        call_args = mock_model.generate_content.call_args
        generation_config = call_args[1]['generation_config']
        self.assertEqual(generation_config['temperature'], 0.5)
    
    def test_resolve_configuration_defaults(self):
        """Test configuration resolution with defaults."""
        llm_manager = LLMManager(self.mock_config_manager)
        config = llm_manager._resolve_configuration()
        
        expected_config = {
            'provider': 'gemini',
            'model': 'gemini-2.0-flash-exp',
            'temperature': 0.7,
            'max_tokens': 8192,
            'top_p': 0.8,
            'top_k': 40,
        }
        self.assertEqual(config, expected_config)
    
    def test_resolve_configuration_with_overrides(self):
        """Test configuration resolution with parameter overrides."""
        llm_manager = LLMManager(self.mock_config_manager)
        config = llm_manager._resolve_configuration(
            provider="gemini",
            temperature=0.9,
            custom_param="value"
        )
        
        self.assertEqual(config['temperature'], 0.9)
        self.assertEqual(config['custom_param'], "value")
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_api_key'})
    @patch('google.generativeai', new_callable=MagicMock)
    def test_validate_gemini_availability_success(self, mock_genai):
        """Test successful Gemini availability validation."""
        mock_genai.list_models.return_value = [Mock()]
        
        llm_manager = LLMManager(self.mock_config_manager)
        available = llm_manager._validate_gemini_availability()
        
        self.assertTrue(available)
        mock_genai.configure.assert_called_once_with(api_key='test_api_key')
    
    @patch.dict(os.environ, {}, clear=True)
    def test_validate_gemini_availability_no_key(self):
        """Test Gemini availability validation without API key."""
        llm_manager = LLMManager(self.mock_config_manager)
        available = llm_manager._validate_gemini_availability()
        
        self.assertFalse(available)
    
    def test_get_available_providers(self):
        """Test getting available providers."""
        llm_manager = LLMManager(self.mock_config_manager)
        
        with patch.object(llm_manager, '_validate_gemini_availability', return_value=True):
            providers = llm_manager.get_available_providers()
        
        self.assertEqual(providers, {"gemini": True})
    
    def test_validate_config(self):
        """Test configuration validation."""
        llm_manager = LLMManager(self.mock_config_manager)
        
        with patch.object(llm_manager, 'get_available_providers', return_value={"gemini": True}):
            config = llm_manager.validate_config()
        
        expected = {
            "default_provider": "gemini",
            "available_providers": {"gemini": True},
            "default_provider_available": True
        }
        self.assertEqual(config, expected)

if __name__ == '__main__':
    unittest.main()