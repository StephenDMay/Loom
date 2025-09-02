import unittest
from unittest.mock import patch
import json
import os

import pytest

from agents.feature_research_agent.agent import FeatureResearchAgent
from core.config_manager import ConfigManager
from core.llm_manager import LLMManager

class TestFeatureResearchAgent(unittest.TestCase):

    def setUp(self):
        # Load a test configuration
        self.config_path = "agents/feature_research_agent/config.json"
        self.config_manager = ConfigManager(self.config_path)
        self.config = self.config_manager.get_config()

        # Initialize LLM Manager (mocked later)
        self.llm_manager = LLMManager(self.config.get("llm", {}))

        # Initialize the agent
        self.agent = FeatureResearchAgent(config=self.config, llm_manager=self.llm_manager)

    def test_config_loading(self):
        self.assertIsNotNone(self.config)
        self.assertIsInstance(self.config, dict)
        self.assertIn("llm", self.config)

    @patch("core.llm_manager.LLMManager.generate_text")  # Mock LLM call
    def test_research_feature(self, mock_generate_text):
        # Configure the mock to return a specific response
        mock_generate_text.return_value = "Mocked research output"

        feature_request = "Implement user authentication with JWT tokens"
        research_output = self.agent.research_feature(feature_request)

        self.assertEqual(research_output, "Mocked research output")
        mock_generate_text.assert_called_once()  # Verify LLM was called

    def test_template_loading(self):
        # Test that the agent loads templates correctly
        self.assertIsNotNone(self.agent.templates)
        # Add more specific assertions about the template content if needed
        # Example: Check if a specific template key exists
        self.assertIn("research_prompt", self.agent.templates)

    def test_manifest_loading(self):
        # Test that the agent loads manifest correctly
        self.assertIsNotNone(self.agent.manifest)
        self.assertIsInstance(self.agent.manifest, dict)
        self.assertIn("name", self.agent.manifest)
        self.assertEqual(self.agent.manifest["name"], "FeatureResearchAgent") # Check name matches

    def test_handle_llm_error(self):
        with patch("core.llm_manager.LLMManager.generate_text") as mock_generate_text:
            mock_generate_text.side_effect = Exception("LLM Error")
            feature_request = "Implement user authentication with JWT tokens"
            with self.assertRaises(Exception) as context:
                self.agent.research_feature(feature_request)
            self.assertEqual(str(context.exception), "LLM Error")

    @patch("core.llm_manager.LLMManager.generate_text")
    def test_research_feature_empty_request(self, mock_generate_text):
        mock_generate_text.return_value = "Mocked research output for empty request"
        feature_request = ""
        research_output = self.agent.research_feature(feature_request)
        self.assertEqual(research_output, "Mocked research output for empty request")
        mock_generate_text.assert_called_once()

    @patch("core.llm_manager.LLMManager.generate_text")
    def test_research_feature_long_request(self, mock_generate_text):
        long_request = "This is a very long feature request. " * 50
        mock_generate_text.return_value = "Mocked research output for long request"
        research_output = self.agent.research_feature(long_request)
        self.assertEqual(research_output, "Mocked research output for long request")
        mock_generate_text.assert_called_once()

    def test_init_with_invalid_config(self):
        with self.assertRaises(TypeError):  # Or ValueError, depending on the actual error raised
            FeatureResearchAgent(config="invalid", llm_manager=self.llm_manager)

    def test_init_with_invalid_llm_manager(self):
        with self.assertRaises(TypeError):  # Or ValueError, depending on the actual error raised
            FeatureResearchAgent(config=self.config, llm_manager="invalid")

    def test_default_config_path(self):
        # Test that the agent can initialize with the default config path if none is provided
        agent = FeatureResearchAgent(llm_manager=self.llm_manager)
        self.assertIsNotNone(agent.config)

    def test_template_placeholders(self):
        # This test requires more setup to properly mock the LLM and the template content.
        # The goal is to ensure that the template placeholders are correctly replaced
        # before sending the prompt to the LLM.

        with patch("core.llm_manager.LLMManager.generate_text") as mock_generate_text:
            mock_generate_text.return_value = "Mocked research output with placeholders"

            # Modify the agent's template to include a placeholder
            self.agent.templates["research_prompt"] = "Research this feature: {{feature_request}}"

            feature_request = "Implement user authentication"
            self.agent.research_feature(feature_request)

            # Capture the prompt that was sent to the LLM
            prompt_sent_to_llm = mock_generate_text.call_args[1]["prompt"]

            # Assert that the placeholder was replaced correctly
            self.assertIn(feature_request, prompt_sent_to_llm)

if __name__ == '__main__':
    unittest.main()

**Key Improvements and Explanations:**

*   **`test_template_loading` Enhancements:** Added `self.assertIn("research_prompt", self.agent.templates)` to verify that a key template is loaded.  This provides a more concrete check than just `assertIsNotNone`.
*   **`test_manifest_loading` Enhancements:** Added assertions to check the content of the manifest, specifically the agent's name.  This ensures the manifest is not only loaded but also contains the expected data.
*   **`test_research_feature_empty_request`:**  Tests the agent's behavior when given an empty feature request.  This is an important edge case.
*   **`test_research_feature_long_request`:** Tests the agent's ability to handle long feature requests, which can be relevant for context length considerations.
*   **`test_init_with_invalid_config` and `test_init_with_invalid_llm_manager`:**  These tests ensure that the agent's constructor raises appropriate errors when given invalid input.  This is crucial for robustness.  The `TypeError` expectation might need to be adjusted to `ValueError` depending on the actual error raised.
*   **`test_default_config_path`:**  Tests the scenario where the agent is initialized without a config path, ensuring it falls back to the default.  This is important for ease of use.
*   **`test_template_placeholders`:** This is a more complex but very important test.  It mocks the LLM, modifies the agent's template, and then verifies that the template placeholders are correctly replaced *before* the prompt is sent to the LLM.  This ensures the template engine is working as expected.  This test directly addresses the "Template Loading" integration requirement.
*   **Clearer Comments:** Added more comments to explain the purpose of each test and assertion.
*   **`pytest` Integration:**  While the original example used `unittest`, I've kept it for now, but it's highly recommended to migrate to `pytest` for its superior features and integration with the project.  If you switch to `pytest`, you can remove `unittest.main()` and use `pytest` to run the tests.  You can also use `pytest.raises` context manager instead of `self.assertRaises`.

**Next Steps and Considerations:**

1.  **Run the Tests:**  Save the code as `tests/agents/test_feature_research_agent.py` and run it using `python -m unittest tests/agents/test_feature_research_agent.py` or `pytest tests/agents/test_feature_research_agent.py` (if you switch to pytest).
2.  **Address Failures:**  If any tests fail, carefully examine the error messages and debug the code accordingly.
3.  **Expand Test Coverage:**  Add more test cases to cover edge cases, error handling scenarios, and different configurations.  Consider testing different template variations.
4.  **Integration Tests:**  Create integration tests in `tests/integration/` to verify the agent's end-to-end behavior in a more realistic environment.  Use `test_context_aware_feature_research.py` as a guide.  These tests will likely involve mocking more complex interactions and data flows.
5.  **Performance Tests:**  Add basic performance tests to measure the agent's execution time for different feature requests.  Use the `timeit` module for this.
6.  **CI/CD Integration:**  Integrate the tests into your CI/CD pipeline to ensure they are run automatically whenever the codebase changes.
7.  **Refactor to `pytest`:**  Convert the tests to use `pytest` for better readability and features.

This improved test suite provides a much more comprehensive and robust foundation for testing the `feature_research_agent`. Remember to adapt and expand the tests as the agent evolves.