import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

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
            "llm_settings.temperature": 0.7,
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
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_initialize_gemini_client(self, mock_model, mock_configure):
        """Test Gemini client initialization with API key."""
        mock_model_instance = Mock()
        mock_model.return_value = mock_model_instance
        
        llm_manager = LLMManager(self.mock_config_manager)
        
        mock_configure.assert_called_once_with(api_key='test_api_key')
        mock_model.assert_called_once_with('gemini-pro')
        self.assertEqual(llm_manager.client, mock_model_instance)
    
    def test_initialize_gemini_client_no_api_key(self):
        """Test that missing API key raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                LLMManager(self.mock_config_manager)
            self.assertIn("GEMINI_API_KEY environment variable not set", str(context.exception))
    
    @patch('core.llm_manager.LLMManager._initialize_client')
    def test_execute_llm_call_empty_prompt(self, mock_init):
        """Test that empty prompt raises ValueError."""
        llm_manager = LLMManager(self.mock_config_manager)
        
        with self.assertRaises(ValueError) as context:
            llm_manager.execute_llm_call("")
        self.assertIn("Prompt cannot be empty", str(context.exception))
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_api_key'})
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_execute_llm_call_success(self, mock_model, mock_configure):
        """Test successful LLM call execution."""
        # Setup mock response
        mock_response = Mock()
        mock_response.text = "Test response"
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        llm_manager = LLMManager(self.mock_config_manager)
        result = llm_manager.execute_llm_call("Test prompt")
        
        self.assertEqual(result, "Test response")
        mock_model_instance.generate_content.assert_called_once()
    
    def test_unsupported_provider(self):
        """Test that unsupported provider raises ValueError."""
        self.mock_config_manager.get.side_effect = lambda key, default=None: "unsupported_provider" if "default_provider" in key else default
        
        with self.assertRaises(ValueError) as context:
            LLMManager(self.mock_config_manager)
        self.assertIn("Unsupported LLM provider: unsupported_provider", str(context.exception))

if __name__ == '__main__':
    unittest.main()