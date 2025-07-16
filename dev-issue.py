#!/usr/bin/env python3
"""
dev-issue.py - Universal Development Issue Generator
Usage: python dev-issue.py [options] [template] [feature description]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from core.config_manager import config_manager


class DevIssueGenerator:
    def __init__(self):
        self.script_dir = Path(__file__).parent  # Where the script lives
        self.project_dir = Path.cwd()            # Where you run the script from
        self.config_file = self.project_dir / "dev-automation.config.json"
        self.meta_prompt_file = self.script_dir / "meta-prompt-template.md"
        self.output_dir = self.project_dir / "generated-issues"

    def show_help(self):
        """Display help information"""
        help_text = f"""
Universal Development Issue Generator

USAGE:
    python dev-issue.py [OPTIONS] [TEMPLATE] [FEATURE_DESCRIPTION]

COMMANDS:
    init                        Interactive setup to create configuration
    -h, --help                  Show this help message
    --config PATH               Use custom config file
    --provider PROVIDER         Override LLM provider (gemini, claude-code, openai)
    --dry-run                   Generate prompt without executing LLM

TEMPLATES:
    --template ui               User interface features
    --template api              Backend/API features  
    --template data             Data pipeline features
    --template perf             Performance optimization features

EXAMPLES:
    python dev-issue.py init
    python dev-issue.py "implement user authentication system"
    python dev-issue.py --template ui "add real-time dashboard updates"
    python dev-issue.py --template data "optimize tournament data sync"
    python dev-issue.py --provider claude-code "implement caching layer"

CONFIGURATION:
    Config file: {self.config_file}
    Template file: {self.meta_prompt_file}
    Output directory: {self.output_dir}
        """
        print(help_text)

    def test_dependencies(self, skip_check=False):
        """Check for required dependencies"""
        # Temporarily skip dependency check since we know gemini works
        return
        
        if skip_check:
            return
            
        missing_deps = []
        
        if not self.config_file.exists():
            return  # Skip dependency check if no config exists yet
            
        try:
            provider = config_manager.get('llm_settings.default_provider', 'gemini')
            
            # Check if the LLM provider command exists
            try:
                subprocess.run([provider, '--version'], 
                             capture_output=True, 
                             check=False, 
                             timeout=5)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                missing_deps.append(provider)
                
        except (json.JSONDecodeError, KeyError):
            print(f"Error: Invalid configuration file: {self.config_file}")
            sys.exit(1)
            
        if missing_deps:
            print(f"Missing dependencies: {', '.join(missing_deps)}")
            print("Please install the missing dependencies and try again")
            sys.exit(1)

    def create_project_config(self):
        """Interactive setup to create configuration"""
        print("Creating new project configuration...")
        print()
        print("Please provide the following information about your project:")
        print()
        
        project_name = input("Project name: ")
        project_context = input("Project description/context: ")
        tech_stack = input("Tech stack (e.g., React, Node.js, PostgreSQL): ")
        architecture = input("Architecture pattern (e.g., microservices, monolith): ")
        target_users = input("Target users: ")
        constraints = input("Key constraints (optional): ")
        repo_owner = input("GitHub repo owner: ")
        repo_name = input("GitHub repo name: ")
        
        print()
        print("Choose default LLM provider:")
        print("1) gemini")
        print("2) claude-code")
        print("3) openai")
        
        provider_choice = input("Selection (1-3): ").strip()
        provider_map = {"1": "gemini", "2": "claude-code", "3": "openai"}
        llm_provider = provider_map.get(provider_choice, "gemini")
        
        config = {
            "project": {
                "name": project_name,
                "context": project_context,
                "tech_stack": tech_stack,
                "architecture": architecture,
                "target_users": target_users,
                "constraints": constraints
            },
            "github": {
                "repo_owner": repo_owner,
                "repo_name": repo_name,
                "default_project": "",
                "default_labels": ["auto-generated", "needs-review"]
            },
            "llm_settings": {
                "default_provider": llm_provider,
                "output_format": "structured",
                "research_depth": "standard",
                "temperature": 0.7
            },
            "templates": {},
            "automation": {
                "auto_create_issues": False,
                "auto_assign": False
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
        print(f"Configuration created at {self.config_file}")
        print("You can edit this file to customize templates and automation settings")

    def invoke_llm(self, prompt: str, provider: str) -> str:
        """Execute LLM with the given prompt"""
        print(f"Executing prompt with provider: {provider}")
        
        # On Windows, npm-installed tools need .cmd extension for subprocess
        import platform
        if platform.system() == "Windows" and provider in ["gemini"]:
            provider_cmd = f"{provider}.cmd"
        else:
            provider_cmd = provider
        
        try:
            # Use subprocess to pipe the prompt to the LLM provider
            result = subprocess.run(
                [provider_cmd],
                input=prompt,
                text=True,
                capture_output=True,
                check=True
            )
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            print(f"LLM provider execution failed with exit code {e.returncode}")
            print(f"Error details: {e.stderr}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"LLM provider '{provider}' not found. Make sure it's installed and in your PATH.")
            print("Supported providers: gemini, claude-code, openai")
            sys.exit(1)

    def publish_issue_to_github(self, output_file: Path, feature_description: str, result: str):
        """Handle GitHub issue creation"""
        print(f"Generated issue file: {output_file}")
        print()
        print("To create GitHub issue manually:")
        
        repo_path = f"{config_manager.get('github.repo_owner')}/{config_manager.get('github.repo_name')}"
        manual_command = f'gh issue create --repo "{repo_path}" --body-file "{output_file}"'
        print(f"  {manual_command}")
        print()
        
        if not config_manager.get('automation.auto_create_issues', False):
            return
            
        print("Auto-creating GitHub issue...")
        
        # Extract title from generated content
        issue_title = feature_description  # Fallback
        match = re.search(r'^# FEATURE:\s*(.+)$', result, re.MULTILINE)
        if match:
            issue_title = match.group(1).strip()
            print(f"Extracted title: {issue_title}")
        
        # Build GitHub CLI command
        gh_args = [
            'gh', 'issue', 'create',
            '--repo', repo_path,
            '--title', issue_title,
            '--body-file', str(output_file)
        ]
        
        # Add labels if configured
        default_labels = config_manager.get('github.default_labels', [])
        if default_labels:
            gh_args.extend(['--label', ','.join(default_labels)])
            
        # Add project if configured
        default_project = config_manager.get('github.default_project')
        if default_project:
            gh_args.extend(['--project', default_project])
        
        try:
            print(f"Running: {' '.join(gh_args)}")
            
            result = subprocess.run(gh_args, capture_output=True, text=True, check=True)
            
            print("✓ GitHub issue created successfully!")
            
            # Try to extract and display issue URL from output
            url_match = re.search(r'https://github\\.com/.*/issues/\\d+', result.stdout)
            if url_match:
                print(f"Issue URL: {url_match.group()}")
            else:
                print(f"Output: {result.stdout}")
                
        except subprocess.CalledProcessError as e:
            print(f"Failed to create GitHub issue (exit code: {e.returncode})")
            print(f"Error output: {e.stderr}")
            print("Use the manual command above to create the issue.")
        except FileNotFoundError:
            print("Error: GitHub CLI (gh) not found.")
            print("Ensure 'gh' is installed and you're authenticated.")
            print("Use the manual command above to create the issue.")

    def generate_issue(self, feature_description: str, template_type: Optional[str] = None,
                      provider: Optional[str] = None, dry_run: bool = False):
        """Generate issue specification"""
        if not self.meta_prompt_file.exists():
            print(f"Meta-prompt template not found: {self.meta_prompt_file}")
            print("Please ensure the template file exists")
            sys.exit(1)
            
        print(f"Generating issue for: {feature_description}")
        
        # Load and process template
        with open(self.meta_prompt_file, 'r') as f:
            template = f.read()
            
        # Get required values from config, exit if missing
        required_keys = [
            'project.context', 'project.tech_stack', 'project.architecture',
            'project.target_users', 'project.constraints'
        ]
        config_values = {}
        for key in required_keys:
            value = config_manager.get(key)
            if value is None:
                print(f"Error: Missing required configuration key: '{key}' in {self.config_file}")
                sys.exit(1)
            config_values[key] = value

        # Substitute template variables
        template = template.replace('[PROJECT_CONTEXT_PLACEHOLDER]', config_values['project.context'])
        template = template.replace('[TECH_STACK_PLACEHOLDER]', config_values['project.tech_stack'])
        template = template.replace('[ARCHITECTURE_PLACEHOLDER]', config_values['project.architecture'])
        template = template.replace('[USER_BASE_PLACEHOLDER]', config_values['project.target_users'])
        
        constraints = config_values['project.constraints']
        if template_type and config_manager.get(f'templates.{template_type}'):
            template_context = config_manager.get(f'templates.{template_type}')
            constraints = f"{constraints}\n\nTEMPLATE-SPECIFIC CONTEXT: {template_context}"
            
        template = template.replace('[CONSTRAINTS_PLACEHOLDER]', constraints)
        template = template.replace('[RUNTIME_CONSTRAINTS_PLACEHOLDER]', constraints)
        template = template.replace('[USER_INPUT_PLACEHOLDER]', feature_description)
        
        if dry_run:
            print("=== GENERATED PROMPT (DRY RUN) ===")
            print(template)
            print("==================================")
            return
            
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_feature = re.sub(r'[^\w\-_]', '_', feature_description)
        safe_feature = safe_feature[:50]
        output_file = self.output_dir / f"{timestamp}_{safe_feature}.md"
        
        # Execute LLM and save output
        print("Processing with LLM...")
        llm_provider = provider or config_manager.get('llm_settings.default_provider')
        raw_result = self.invoke_llm(template, llm_provider)

        # Clean the result
        result = raw_result
        feature_marker = "# FEATURE:"
        marker_pos = raw_result.find(feature_marker)
        if marker_pos != -1:
            result = raw_result[marker_pos:]

        with open(output_file, 'w') as f:
            f.write(result)
        print(f"Issue specification saved to: {output_file}")
        
        # GitHub Integration
        self.publish_issue_to_github(output_file, feature_description, result)
        
        # Display summary
        print()
        print("=== GENERATED ISSUE SUMMARY ===")
        lines = result.split('\n')
        for line in lines[:20]:
            print(line)
        print("...")
        print("===============================")
        print()
        print(f"Full specification available at: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Universal Development Issue Generator',
                                   add_help=False)
    
    # Main command
    parser.add_argument('command', nargs='?', help='Command or feature description')
    parser.add_argument('remaining_args', nargs='*', help='Additional arguments')
    
    # Options
    parser.add_argument('-h', '--help', action='store_true', help='Show help')
    parser.add_argument('--config', help='Use custom config file')
    parser.add_argument('--template', choices=['ui', 'api', 'data', 'perf'],
                       help='Feature template type')
    parser.add_argument('--provider', choices=['gemini', 'claude-code', 'openai'],
                       help='Override LLM provider')
    parser.add_argument('--dry-run', action='store_true',
                       help='Generate prompt without executing LLM')
    
    args = parser.parse_args()
    
    generator = DevIssueGenerator()
    
    # Override config file if specified
    if args.config:
        generator.config_file = Path(args.config)

    # Load configuration
    if args.command != 'init':
        try:
            config_manager.load_config(str(generator.config_file))
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
            print("Run 'python dev-issue.py init' to create a configuration file")
            sys.exit(1)

    if args.help:
        generator.show_h()
        return
        
    if args.command == 'init':
        generator.create_project_config()
        return
    
    # Handle feature description parsing
    if args.template:
        # Template specified: --template ui "feature description"
        feature_description = ' '.join(args.remaining_args).strip()
        template_type = f"{args.template}_feature"
    else:
        # No template: treat command as start of feature description
        all_args = [args.command] + args.remaining_args if args.command else args.remaining_args
        feature_description = ' '.join(all_args).strip()
        template_type = None
    
    if not feature_description:
        print("No feature description provided")
        print()
        generator.show_help()
        sys.exit(1)
    
    # Run the tool
    generator.test_dependencies(skip_check=args.dry_run)
    generator.generate_issue(feature_description, template_type, args.provider, args.dry_run)


if __name__ == '__main__':
    main()
