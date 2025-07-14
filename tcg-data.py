#!/usr/bin/env python3
"""
tcg-data.py - Data Pipeline Feature Generator for Pokemon TCG App
Usage: python tcg-data.py [feature description]
"""
import subprocess
import sys
from pathlib import Path

def main():
    """
    Wrapper script to call dev-issue.py with the 'data' template.
    """
    if len(sys.argv) < 2:
        print("Usage: python tcg-data.py 'feature description'")
        print("Example: python tcg-data.py 'optimize Limitless API sync pipeline'")
        sys.exit(1)

    feature_description = ' '.join(sys.argv[1:])
    
    script_dir = Path(__file__).parent
    dev_issue_script = script_dir / "dev-issue.py"

    command = [
        sys.executable, 
        str(dev_issue_script), 
        "--template", 
        "data", 
        feature_description
    ]

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
