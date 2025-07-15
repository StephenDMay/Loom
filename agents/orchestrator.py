import os
import json
import importlib.util
from agents.base_agent import BaseAgent

class AgentOrchestrator:
    def __init__(self, agent_dir='agents'):
        self.agent_dir = agent_dir
        self.agents = {}
        self.load_agents()

    def load_agents(self):
        for agent_name in os.listdir(self.agent_dir):
            agent_path = os.path.join(self.agent_dir, agent_name)
            if os.path.isdir(agent_path):
                manifest_path = os.path.join(agent_path, 'manifest.json')
                if os.path.exists(manifest_path):
                    try:
                        with open(manifest_path, 'r') as f:
                            manifest = json.load(f)
                        
                        entry_point = manifest['entry_point']
                        class_name = manifest['class_name']
                        
                        module_path = os.path.join(agent_path, entry_point)
                        spec = importlib.util.spec_from_file_location(agent_name, module_path)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        agent_class = getattr(module, class_name)
                        if issubclass(agent_class, BaseAgent):
                            self.agents[manifest['name']] = agent_class()
                        else:
                            print(f"Error loading agent {agent_name}: {class_name} is not a subclass of BaseAgent.")
                    except Exception as e:
                        print(f"Error loading agent {agent_name}: {e}")

    def list_agents(self):
        return list(self.agents.keys())

    def get_agent(self, name):
        return self.agents.get(name)

    def execute_agent(self, name, task):
        agent = self.get_agent(name)
        if agent:
            return agent.execute(task)
        else:
            raise ValueError(f"Agent '{name}' not found.")
