#!/usr/bin/env python3
"""
dev-issue.py - Universal Development Issue Runner
Usage: python dev-issue.py "feature description"
"""

import argparse
import sys
from pathlib import Path

from core.config_manager import ConfigManager
from agents.orchestrator import AgentOrchestrator

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

    def run(self, feature_description: str):
        """
        Initializes the AgentOrchestrator and runs the agent sequence.
        """
        print("Initializing agent orchestrator...")
        orchestrator = AgentOrchestrator(self.config_manager)
        
        print("Executing agent sequence...")
        final_output = orchestrator.run_sequence(feature_description)
        
        print("\nAgent sequence finished.")
        print("Final output:")
        print(final_output)

def main():
    parser = argparse.ArgumentParser(description='Universal Development Issue Runner')
    
    parser.add_argument('feature_description', nargs='*', help='The feature description to be processed by the agent pipeline.')
    
    args = parser.parse_args()
    
    if not args.feature_description:
        parser.print_help()
        sys.exit(1)
    
    feature_description = ' '.join(args.feature_description)
    runner = DevIssueRunner()
    runner.run(feature_description)

if __name__ == '__main__':
    main()
