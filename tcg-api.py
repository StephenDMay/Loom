#!/usr/bin/env python3
"""
tcg-api.py - API Feature Generator for Pokemon TCG App
Usage: python tcg-api.py [feature description]
"""
import subprocess
import sys
from pathlib import Path

def main():
    """
    Wrapper script to call dev-issue.py with the 'api' template.
    """
    if len(sys.argv) < 2:
        print("Usage: python tcg-api.py 'feature description'")
        print("Example: python tcg-api.py 'implement tournament bracket API endpoints'")
        sys.exit(1)

    feature_description = ' '.join(sys.argv[1:])
    
    # Construct the path to the main dev-issue.py script
    script_dir = Path(__file__).parent
    dev_issue_script = script_dir / "dev-issue.py"

    # Build the command to execute
    command = [
        sys.executable, 
        str(dev_issue_script), 
        "--template", 
        "api", 
        feature_description
    ]

    # Execute the main script
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing dev-issue.py: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Main script not found at {dev_issue_script}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
