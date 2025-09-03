import unittest
import logging
from unittest.mock import Mock, patch, MagicMock
from agents.orchestrator import AgentOrchestrator
from agents.base_agent import BaseAgent
from core.config_manager import ConfigManager


class TestAgentForLogging(BaseAgent):
    """Test agent that tracks execution calls."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execute_calls = []
    
    def execute(self, *args, **kwargs):
        self.execute_calls.append((args, kwargs))
        return f"result_from_{self.__class__.__name__}"


class TestOrchestratorLogging(unittest.TestCase):
    
    def setUp(self):
        # Reset singleton
        ConfigManager._instance = None
        
        # Mock config manager
        self.mock_config_manager = Mock(spec=ConfigManager)
        self.mock_config_manager.get.side_effect = lambda key, default=None: {
            "agents.directory": "/mock/agents/dir"
        }.get(key, default)
        
        # Create orchestrator with mocked dependencies
        with patch('agents.orchestrator.LLMManager') as mock_llm_manager_class:
            with patch('agents.orchestrator.ContextManager') as mock_context_manager_class:
                with patch.object(AgentOrchestrator, 'load_agents'):
                    with patch.object(AgentOrchestrator, 'prepare_execution_sequence'):
                        self.orchestrator = AgentOrchestrator(self.mock_config_manager)
        
        # Set up test agents manually
        self.test_agent1 = TestAgentForLogging(config={'name': 'test_agent_1'})
        self.test_agent2 = TestAgentForLogging(config={'name': 'test_agent_2'})
        
        self.orchestrator.agents = {
            'test_agent_1': self.test_agent1,
            'test_agent_2': self.test_agent2
        }
        self.orchestrator.execution_order = [self.test_agent1, self.test_agent2]
    
    def test_orchestrator_logger_initialization(self):
        """Test that orchestrator logger is properly initialized."""
        self.assertIsInstance(self.orchestrator.logger, logging.Logger)
        self.assertEqual(self.orchestrator.logger.name, "orchestrator")
    
    def test_run_sequence_logs_execution_start(self):
        """Test that run_sequence logs the start of execution sequence."""
        initial_task = "test task"
        
        with patch.object(self.orchestrator.logger, 'info') as mock_info:
            with patch.object(self.orchestrator.logger, 'debug'):
                with patch('builtins.print'):  # Suppress print output
                    self.orchestrator.run_sequence(initial_task)
                    
                    # Check first log call for execution start
                    mock_info.assert_any_call("Starting agent execution sequence with 2 agents")
    
    def test_run_sequence_logs_execution_completion(self):
        """Test that run_sequence logs successful completion."""
        initial_task = "test task"
        
        with patch.object(self.orchestrator.logger, 'info') as mock_info:
            with patch.object(self.orchestrator.logger, 'debug'):
                with patch('builtins.print'):  # Suppress print output
                    self.orchestrator.run_sequence(initial_task)
                    
                    # Check last log call for completion
                    mock_info.assert_any_call("Agent execution sequence completed successfully")
    
    def test_run_sequence_logs_individual_agent_execution(self):
        """Test that run_sequence logs each agent's execution."""
        initial_task = "test task"
        
        with patch.object(self.orchestrator.logger, 'info') as mock_info:
            with patch.object(self.orchestrator.logger, 'debug') as mock_debug:
                with patch('builtins.print'):  # Suppress print output
                    self.orchestrator.run_sequence(initial_task)
                    
                    # Check agent execution logs
                    mock_info.assert_any_call("Executing agent 1/2: test_agent_1")
                    mock_info.assert_any_call("Executing agent 2/2: test_agent_2")
    
    def test_run_sequence_logs_execution_time(self):
        """Test that run_sequence logs execution time for each agent."""
        initial_task = "test task"
        
        with patch.object(self.orchestrator.logger, 'info') as mock_info:
            with patch.object(self.orchestrator.logger, 'debug'):
                with patch('builtins.print'):  # Suppress print output
                    with patch('time.time', side_effect=[0, 1.5, 1.5, 3.0]):  # Mock time progression
                        self.orchestrator.run_sequence(initial_task)
                        
                        # Check execution time logs (should contain timing info)
                        calls = mock_info.call_args_list
                        time_logs = [call for call in calls if 'completed successfully in' in str(call)]
                        self.assertEqual(len(time_logs), 2)  # One for each agent
    
    def test_run_sequence_logs_agent_input_output(self):
        """Test that run_sequence logs agent input and output at debug level."""
        initial_task = "test task"
        
        with patch.object(self.orchestrator.logger, 'info'):
            with patch.object(self.orchestrator.logger, 'debug') as mock_debug:
                with patch('builtins.print'):  # Suppress print output
                    self.orchestrator.run_sequence(initial_task)
                    
                    # Check debug logs for input/output
                    debug_calls = [str(call) for call in mock_debug.call_args_list]
                    input_logs = [log for log in debug_calls if 'input:' in log]
                    output_logs = [log for log in debug_calls if 'output:' in log]
                    
                    self.assertTrue(len(input_logs) >= 2)  # At least one per agent
                    self.assertTrue(len(output_logs) >= 2)  # At least one per agent
    
    def test_run_sequence_logs_agent_failure(self):
        """Test that run_sequence logs agent failures with error level."""
        initial_task = "test task"
        
        # Make the first agent raise an exception
        def failing_execute(*args, **kwargs):
            raise ValueError("Test error")
        
        self.test_agent1.execute = failing_execute
        
        with patch.object(self.orchestrator.logger, 'error') as mock_error:
            with patch.object(self.orchestrator.logger, 'info'):
                with patch.object(self.orchestrator.logger, 'debug'):
                    with patch('builtins.print'):  # Suppress print output
                        with self.assertRaises(ValueError):
                            self.orchestrator.run_sequence(initial_task)
                        
                        # Check error log
                        error_calls = mock_error.call_args_list
                        self.assertEqual(len(error_calls), 1)
                        error_message = str(error_calls[0])
                        self.assertIn("test_agent_1 failed", error_message)
                        self.assertIn("Test error", error_message)
    
    def test_sanitize_for_logging_truncates_long_data(self):
        """Test that _sanitize_for_logging truncates long data."""
        # Use a pattern that won't trigger redaction
        long_data = "This is a very long message. " * 20  # ~600 chars
        result = self.orchestrator._sanitize_for_logging(long_data, max_length=200)
        
        truncate_suffix = "... [truncated]"
        expected_length = 200 + len(truncate_suffix)
        self.assertEqual(len(result), expected_length)
        self.assertTrue(result.endswith(truncate_suffix))
        self.assertEqual(result[:200], long_data[:200])
    
    def test_sanitize_for_logging_redacts_sensitive_data(self):
        """Test that _sanitize_for_logging redacts sensitive patterns."""
        sensitive_data = "api_key=secret123 token=abc123 password=mypass Bearer xyz789"
        result = self.orchestrator._sanitize_for_logging(sensitive_data)
        
        # Should redact sensitive patterns
        self.assertNotIn("secret123", result)
        self.assertNotIn("abc123", result)
        self.assertNotIn("mypass", result)
        self.assertNotIn("xyz789", result)
        self.assertIn("[REDACTED]", result)
    
    def test_sanitize_for_logging_handles_empty_data(self):
        """Test that _sanitize_for_logging handles empty/None data."""
        self.assertEqual(self.orchestrator._sanitize_for_logging(""), "")
        self.assertEqual(self.orchestrator._sanitize_for_logging(None), "")
    
    def test_sanitize_for_logging_preserves_safe_data(self):
        """Test that _sanitize_for_logging preserves safe data unchanged."""
        safe_data = "This is safe data with numbers 123 and symbols !@#"
        result = self.orchestrator._sanitize_for_logging(safe_data)
        self.assertEqual(result, safe_data)


if __name__ == '__main__':
    unittest.main()