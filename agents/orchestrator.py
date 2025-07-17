import os
import json
import importlib.util
from agents.base_agent import BaseAgent
from core.config_manager import ConfigManager

class AgentOrchestrator:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.agent_dir = self.config_manager.get("agents.directory", os.path.dirname(os.path.abspath(__file__)))
        self.agents = {}
        self.execution_order = []
        self.load_agents()
        self.prepare_execution_sequence()

    def load_agents(self):
        for agent_name in os.listdir(self.agent_dir):
            agent_path = os.path.join(self.agent_dir, agent_name)
            
            if not os.path.isdir(agent_path):
                continue

            manifest_path = os.path.join(agent_path, 'manifest.json')
            if not os.path.exists(manifest_path):
                continue

            try:
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                
                entry_point = manifest['entry_point']
                class_name = manifest['class_name']
                
                agent_config_path = os.path.join(agent_path, 'config.json')
                module_path = os.path.join(agent_path, entry_point)
                spec = importlib.util.spec_from_file_location(agent_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                agent_class = getattr(module, class_name)
                if issubclass(agent_class, BaseAgent):
                    self.agents[manifest['name']] = agent_class(config=self.config_manager)
                else:
                    print(f"Error loading agent {agent_name}: {class_name} is not a subclass of BaseAgent.")
            except Exception as e:
                print(f"Error loading agent {agent_name}: {e}")

    def prepare_execution_sequence(self):
        agent_order_names = self.config_manager.get('agent_execution_order')

        if not agent_order_names:
            print("Warning: 'agent_execution_order' not found in config. Executing all loaded agents in arbitrary order.")
            self.execution_order = list(self.agents.values())
            return

        for agent_name in agent_order_names:
            agent = self.agents.get(agent_name)
            if not agent:
                raise ValueError(f"Agent '{agent_name}' from execution order not found.")
            self.execution_order.append(agent)

    def get_execution_sequence(self):
        return self.execution_order

    def list_agents(self):
        return list(self.agents.keys())

    def get_agent(self, name):
        return self.agents.get(name)

    def run_sequence(self, initial_task: str):
        current_input = initial_task
        for i, agent in enumerate(self.execution_order):
            agent_name = list(self.agents.keys())[list(self.agents.values()).index(agent)]
            print(f"Executing agent {i+1}/{len(self.execution_order)}: {agent_name}...")
            output = agent.execute(current_input)
            current_input = output
        return current_input
