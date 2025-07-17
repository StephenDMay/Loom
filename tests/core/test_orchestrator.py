import unittest
import json
import os
import shutil
from core.config_manager import ConfigManager
from agents.orchestrator import AgentOrchestrator
from agents.base_agent import BaseAgent

class MockAgent(BaseAgent):
    def __init__(self, config, name):
        super().__init__(config)
        self.name = name
        self.executed = False
        self.input_task = None

    def execute(self, task: str):
        self.executed = True
        self.input_task = task
        return f"processed by {self.name}"

class TestAgentOrchestrator(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'tests/core/temp_test_agents'
        self.agents_dir = os.path.join(self.test_dir, 'agents')
        os.makedirs(self.agents_dir, exist_ok=True)

        # Create mock agents
        self.create_mock_agent('agent_a', 'AgentA')
        self.create_mock_agent('agent_b', 'AgentB')
        self.create_mock_agent('agent_c', 'AgentC')

        # Config Manager
        ConfigManager._instance = None
        self.config_manager = ConfigManager()
        self.config_path = os.path.join(self.test_dir, 'config.json')

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        ConfigManager._instance = None

    def create_mock_agent(self, name, class_name):
        agent_path = os.path.join(self.agents_dir, name)
        os.makedirs(agent_path, exist_ok=True)

        # Manifest
        manifest = {
            "name": name,
            "entry_point": "agent.py",
            "class_name": class_name
        }
        with open(os.path.join(agent_path, 'manifest.json'), 'w') as f:
            json.dump(manifest, f)

        # Agent script
        script_content = f"""
from agents.base_agent import BaseAgent
class {class_name}(BaseAgent):
    def execute(self, task: str):
        return f"output from {name}: {{task}}"
"""
        with open(os.path.join(agent_path, 'agent.py'), 'w') as f:
            f.write(script_content)

    def test_execution_order_respected(self):
        config_data = {
            "agents": {"directory": self.agents_dir},
            "agent_execution_order": ["agent_c", "agent_a", "agent_b"]
        }
        with open(self.config_path, 'w') as f:
            json.dump(config_data, f)
        self.config_manager.load_config(self.config_path)

        orchestrator = AgentOrchestrator(self.config_manager)
        orchestrator.run_sequence("initial_task")

        execution_sequence = [agent.__class__.__name__ for agent in orchestrator.get_execution_sequence()]
        self.assertEqual(execution_sequence, ['AgentC', 'AgentA', 'AgentB'])

    def test_missing_execution_order_executes_all(self):
        config_data = {"agents": {"directory": self.agents_dir}}
        with open(self.config_path, 'w') as f:
            json.dump(config_data, f)
        self.config_manager.load_config(self.config_path)

        orchestrator = AgentOrchestrator(self.config_manager)
        self.assertEqual(len(orchestrator.get_execution_sequence()), 3)

    def test_agent_not_found_raises_error(self):
        config_data = {
            "agents": {"directory": self.agents_dir},
            "agent_execution_order": ["agent_a", "agent_dne"]
        }
        with open(self.config_path, 'w') as f:
            json.dump(config_data, f)
        self.config_manager.load_config(self.config_path)

        with self.assertRaises(ValueError):
            AgentOrchestrator(self.config_manager)

    def test_data_passing_between_agents(self):
        config_data = {
            "agents": {"directory": self.agents_dir},
            "agent_execution_order": ["agent_a", "agent_b"]
        }
        with open(self.config_path, 'w') as f:
            json.dump(config_data, f)
        self.config_manager.load_config(self.config_path)

        orchestrator = AgentOrchestrator(self.config_manager)
        final_output = orchestrator.run_sequence("start")
        
        self.assertEqual(final_output, "output from agent_b: output from agent_a: start")

if __name__ == '__main__':
    unittest.main()
