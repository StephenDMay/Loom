import unittest
import logging
from unittest.mock import Mock, patch
from agents.base_agent import BaseAgent
from core.config_manager import ConfigManager


class TestAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing."""
    
    def execute(self, *args, **kwargs):
        return "test_result"


class TestBaseAgentLogging(unittest.TestCase):
    
    def setUp(self):
        # Reset singleton instance
        ConfigManager._instance = None
        
        # Create test agent instance
        self.config = {'log_level': 'debug'}
        self.llm_manager = Mock()
        self.context_manager = Mock()
        self.agent = TestAgent(
            config=self.config, 
            llm_manager=self.llm_manager, 
            context_manager=self.context_manager
        )
    
    def test_agent_logger_initialization(self):
        """Test that agent logger is properly initialized."""
        self.assertIsInstance(self.agent.logger, logging.Logger)
        self.assertEqual(self.agent.logger.name, "agents.TestAgent")
    
    def test_log_method_with_valid_levels(self):
        """Test log method with all valid log levels."""
        test_message = "Test message"
        
        with patch.object(self.agent.logger, 'log') as mock_log:
            # Test all valid log levels
            levels = ['debug', 'info', 'warning', 'error', 'critical']
            for level in levels:
                self.agent.log(test_message, level)
                expected_level = getattr(logging, level.upper())
                mock_log.assert_called_with(expected_level, test_message)
    
    def test_log_method_with_invalid_level(self):
        """Test log method with invalid log level falls back to info."""
        test_message = "Test message"
        invalid_level = "invalid_level"
        
        with patch.object(self.agent.logger, 'info') as mock_info:
            self.agent.log(test_message, invalid_level)
            mock_info.assert_called_with(f"[INVALID_LEVEL:{invalid_level}] {test_message}")
    
    def test_log_method_default_level(self):
        """Test log method defaults to info level when no level specified."""
        test_message = "Test message"
        
        with patch.object(self.agent.logger, 'log') as mock_log:
            self.agent.log(test_message)  # No level specified
            mock_log.assert_called_with(logging.INFO, test_message)
    
    def test_log_error_method(self):
        """Test that _log_error method uses the new logging system."""
        test_message = "Error message"
        
        with patch.object(self.agent, 'log') as mock_log:
            self.agent._log_error(test_message)
            mock_log.assert_called_with(test_message, "error")
    
    def test_agent_specific_log_level_configuration(self):
        """Test agent-specific log level configuration."""
        config_with_log_level = {'log_level': 'warning'}
        
        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger
            
            agent = TestAgent(config=config_with_log_level)
            
            # Verify logger level is set
            mock_logger.setLevel.assert_called_with(logging.WARNING)
    
    def test_agent_invalid_log_level_configuration(self):
        """Test agent handles invalid log level gracefully."""
        config_with_invalid_level = {'log_level': 'invalid'}
        
        # Should not raise an exception
        try:
            agent = TestAgent(config=config_with_invalid_level)
            self.assertIsNotNone(agent.logger)
        except Exception as e:
            self.fail(f"Agent creation failed with invalid log level: {e}")
    
    def test_agent_without_log_level_configuration(self):
        """Test agent without log level configuration."""
        config_without_log_level = {}
        
        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger
            
            agent = TestAgent(config=config_without_log_level)
            
            # Should not call setLevel since no log_level in config
            mock_logger.setLevel.assert_not_called()


if __name__ == '__main__':
    unittest.main()