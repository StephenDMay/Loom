#!/usr/bin/env python3
"""
loom.py - Universal Development Issue Runner
Usage: python loom.py "feature description"
"""

import argparse
import sys
from pathlib import Path

from core.config_manager import ConfigManager
from core.llm_manager import LLMManager
from agents.orchestrator import AgentOrchestrator

def validate_configuration(config_manager: ConfigManager, llm_manager: LLMManager):
    """Validate configuration and provider availability."""
    print("🔍 Validating configuration...")
    
    # Check LLM configuration
    validation_result = llm_manager.validate_config()
    
    print(f"📝 Default provider: {validation_result['default_provider']}")
    print(f"⚙️  Execution mode: {validation_result['execution_mode']}")
    print()
    
    print("🔧 Provider availability:")
    all_available = True
    for provider, available in validation_result['available_providers'].items():
        status = "✅" if available else "❌"
        print(f"  {status} {provider}")
        if not available:
            all_available = False
    
    print()
    
    if not validation_result['default_provider_available']:
        print(f"⚠️  WARNING: Default provider '{validation_result['default_provider']}' is not available!")
        print("   Consider installing the CLI tool or changing the default provider.")
        return False
    
    if all_available:
        print("✅ All configured providers are available!")
    else:
        print("⚠️  Some providers are unavailable. This may limit your flexibility.")
    
    return validation_result['default_provider_available']

class DevIssueRunner:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.config_file = self.project_dir / "dev-automation.config.json"
        
        # Initialize ConfigManager
        self.config_manager = ConfigManager()
        try:
            self.config_manager.load_config(str(self.config_file))
            self.config_manager.set("project.root", str(self.project_dir))
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
            print(f"Please ensure '{self.config_file}' exists and is valid.")
            # For now, we'll let it continue and rely on default configs,
            # but a stricter implementation might exit here.
            # sys.exit(1) 

        # Initialize LLMManager
        self.llm_manager = LLMManager(self.config_manager)
        
        # Initialize orchestrator
        self.orchestrator = None

    def _ensure_orchestrator(self):
        """Lazy initialization of orchestrator."""
        if self.orchestrator is None:
            self.orchestrator = AgentOrchestrator(self.config_manager)

    def run(self, feature_description: str):
        """
        Initializes the AgentOrchestrator and runs the agent sequence.
        """
        print("Initializing agent orchestrator...")
        self._ensure_orchestrator()
        
        print("Executing agent sequence...")
        final_output = self.orchestrator.run_sequence(feature_description)
        
        print("\nAgent sequence finished.")
        print("Final output:")
        print(final_output)

    def validate_config(self):
        """Validate configuration and provider availability."""
        return validate_configuration(self.config_manager, self.llm_manager)

def main():
    parser = argparse.ArgumentParser(description='Universal Development Issue Runner')
    
    parser.add_argument('feature_description', nargs='*', help='The feature description to be processed by the agent pipeline.')
    parser.add_argument('--validate-config', action='store_true', help='Validate configuration and provider availability')
    
    args = parser.parse_args()
    
    runner = DevIssueRunner()
    
    if args.validate_config:
        is_valid = runner.validate_config()
        sys.exit(0 if is_valid else 1)
    
    if not args.feature_description:
        parser.print_help()
        sys.exit(1)
    
    feature_description = ' '.join(args.feature_description)
    runner.run(feature_description)

if __name__ == '__main__':
    main()