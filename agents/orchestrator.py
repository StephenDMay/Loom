import os
import json
import importlib.util
import logging
import time
from agents.base_agent import BaseAgent
from core.config_manager import ConfigManager, AgentConfigManager
from core.llm_manager import LLMManager
from core.context_manager import ContextManager

class AgentOrchestrator:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.llm_manager = LLMManager(config_manager)
        self.context_manager = ContextManager()
        self.agent_dir = self.config_manager.get("agents.directory", os.path.dirname(os.path.abspath(__file__)))
        self.agents = {}
        self.execution_order = []
        
        # Set up orchestrator logger
        self.logger = logging.getLogger("orchestrator")
        
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
                    agent_config_manager = AgentConfigManager(self.config_manager, agent_name)
                    self.agents[manifest['name']] = agent_class(config=agent_config_manager, llm_manager=self.llm_manager, context_manager=self.context_manager)
                else:
                    print(f"Error loading agent {agent_name}: {class_name} is not a subclass of BaseAgent.")
            except Exception as e:
                print(f"Error loading agent {agent_name}: {e}")

    def prepare_execution_sequence(self):
        agent_order_names = self.config_manager.get_agent_execution_order()

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
        self.logger.info(f"Starting agent execution sequence with {len(self.execution_order)} agents")
        self.logger.debug(f"Initial task: {self._sanitize_for_logging(initial_task)}")
        
        current_input = initial_task
        for i, agent in enumerate(self.execution_order):
            agent_name = list(self.agents.keys())[list(self.agents.values()).index(agent)]
            
            self.logger.info(f"Executing agent {i+1}/{len(self.execution_order)}: {agent_name}")
            self.logger.debug(f"Agent {agent_name} input: {self._sanitize_for_logging(str(current_input))}")
            
            # Record start time for execution duration
            start_time = time.time()
            
            try:
                print(f"Executing agent {i+1}/{len(self.execution_order)}: {agent_name}...")
                
                # Special handling for different agent types
                if agent_name == "project-analysis-agent":
                    # Project analysis agent stores results in context, pass original task
                    output = agent.execute(initial_task)
                    # Don't update current_input - keep the original task for subsequent agents
                else:
                    # For other agents like issue_generator, use the original task
                    # They can access project analysis via context_manager if needed
                    output = agent.execute(initial_task)
                    current_input = output
                
                # Record execution duration
                execution_time = time.time() - start_time
                
                self.logger.info(f"Agent {agent_name} completed successfully in {execution_time:.2f}s")
                self.logger.debug(f"Agent {agent_name} output: {self._sanitize_for_logging(str(output))}")
                
            except Exception as e:
                execution_time = time.time() - start_time
                self.logger.error(f"Agent {agent_name} failed after {execution_time:.2f}s with error: {str(e)}")
                raise  # Re-raise the exception to maintain existing error handling behavior
                
        self.logger.info("Agent execution sequence completed successfully")
        return current_input
        
    def _sanitize_for_logging(self, data: str, max_length: int = 200) -> str:
        """
        Sanitize data for logging to prevent sensitive information exposure and limit length.
        
        Args:
            data (str): The data to sanitize
            max_length (int): Maximum length of logged data
            
        Returns:
            str: Sanitized data string
        """
        if not data:
            return ""
            
        # Truncate if too long
        if len(data) > max_length:
            data = data[:max_length] + "... [truncated]"
            
        # Basic sanitization - remove potential sensitive patterns
        # This is a simple implementation; in production, you might want more sophisticated filtering
        import re
        
        # Remove potential API keys, tokens, passwords
        patterns_to_redact = [
            r'(api[_-]?key|token|password|secret)["\']?\s*[:=]\s*["\']?[\w\-_]+',
            r'Bearer\s+[\w\-_]+',
            r'[A-Za-z0-9+/]{32,}={0,2}',  # Base64-like strings
        ]
        
        for pattern in patterns_to_redact:
            data = re.sub(pattern, '[REDACTED]', data, flags=re.IGNORECASE)
            
        return data
