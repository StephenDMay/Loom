import os
from pathlib import Path
from typing import Dict, Optional, TYPE_CHECKING, Set
from agents.base_agent import BaseAgent
import re

if TYPE_CHECKING:
    from core.llm_manager import LLMManager
    from core.context_manager import ContextManager


class ProjectAnalysisAgent(BaseAgent):
    """
    An agent that analyzes the project structure and generates a comprehensive summary.
    Stores the analysis in the ContextManager for other agents to use.
    """
    
    def __init__(self, config: Optional[Dict] = None, llm_manager: Optional['LLMManager'] = None, context_manager: Optional['ContextManager'] = None):
        super().__init__(config, llm_manager, context_manager)
        
        # Default ignore patterns
        self.default_ignore_patterns = {
            '__pycache__', '.git', '.gitignore', 'node_modules', '.venv', 'venv',
            '.env', '.pytest_cache', '.mypy_cache', '.tox', 'dist', 'build',
            '*.pyc', '*.pyo', '*.egg-info', '.DS_Store', 'Thumbs.db'
        }
        
        # Get ignore patterns from config or use defaults
        ignore_patterns = self.config.get('ignore_patterns', [])
        self.ignore_patterns = self.default_ignore_patterns.union(set(ignore_patterns))
        
        # Get project root from config or use current directory
        self.project_root = Path(self.config.get('project_root', os.getcwd()))

    def _should_ignore(self, path: Path) -> bool:
        """Check if a path should be ignored based on ignore patterns."""
        path_str = str(path)
        path_name = path.name
        
        for pattern in self.ignore_patterns:
            if pattern in path_str or path_name == pattern:
                return True
            # Check for wildcard patterns
            if pattern.startswith('*.') and path_name.endswith(pattern[1:]):
                return True
        return False

    def _analyze_directory_structure(self, root_path: Path, max_depth: int = 3, current_depth: int = 0) -> str:
        """
        Generate a text representation of the project directory structure.
        
        Args:
            root_path: The root directory to analyze
            max_depth: Maximum depth to traverse
            current_depth: Current traversal depth
            
        Returns:
            A string representation of the directory structure
        """
        structure = []
        
        if current_depth >= max_depth:
            return ""
            
        try:
            items = sorted(root_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            
            for item in items:
                if self._should_ignore(item):
                    continue
                    
                indent = "  " * current_depth
                
                if item.is_dir():
                    structure.append(f"{indent}{item.name}/")
                    # Recursively analyze subdirectories
                    sub_structure = self._analyze_directory_structure(
                        item, max_depth, current_depth + 1
                    )
                    if sub_structure:
                        structure.append(sub_structure)
                else:
                    # Add file with size info for important files
                    try:
                        size = item.stat().st_size
                        size_str = f" ({size} bytes)" if size < 1024 else f" ({size//1024}KB)"
                        structure.append(f"{indent}{item.name}{size_str}")
                    except (OSError, PermissionError):
                        structure.append(f"{indent}{item.name}")
                        
        except (OSError, PermissionError) as e:
            structure.append(f"{indent}[Permission denied: {e}]")
            
        return "\n".join(structure)

    def _get_key_files_content(self) -> str:
        """
        Read and summarize content from key project files.
        
        Returns:
            A string containing content from key files
        """
        key_files = ['README.md', 'requirements.txt', 'package.json', 'setup.py', 'pyproject.toml']
        content = []
        
        for filename in key_files:
            file_path = self.project_root / filename
            if file_path.exists() and not self._should_ignore(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        # Limit content size to avoid overwhelming the LLM
                        if len(file_content) > 2000:
                            file_content = file_content[:2000] + "\n... [truncated]"
                        content.append(f"=== {filename} ===\n{file_content}\n")
                except (OSError, UnicodeDecodeError) as e:
                    content.append(f"=== {filename} ===\n[Error reading file: {e}]\n")
                    
        return "\n".join(content)

    def _load_and_prepare_template(self, template_path: Path, context: Dict) -> str:
        """
        Load and process a markdown template file, replacing placeholders with dynamic content.
        
        Args:
            template_path: Path to the template file
            context: Dictionary containing placeholder values
            
        Returns:
            Processed template with placeholders replaced
            
        Raises:
            FileNotFoundError: If template file doesn't exist
            Exception: For other template processing errors
        """
        try:
            if not template_path.exists():
                raise FileNotFoundError(f"Template file not found: {template_path}")
                
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Replace placeholders in the format {{ placeholder_name }}
            def replace_placeholder(match):
                placeholder_name = match.group(1).strip()
                return str(context.get(placeholder_name, f"{{{{ {placeholder_name} }}}}"))
            
            processed_content = re.sub(r'\{\{\s*([^}]+)\s*\}\}', replace_placeholder, template_content)
            
            return processed_content
            
        except FileNotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Error processing template {template_path}: {e}")

    def execute(self, *args, **kwargs) -> str:
        """
        Execute the project analysis.
        
        Returns:
            A string containing the analysis summary
        """
        
        try:
            # Generate directory structure
            directory_structure = self._analyze_directory_structure(self.project_root)
            
            # Get key files content
            key_files_content = self._get_key_files_content()
            
            # Prepare template context
            template_context = {
                'project_name': self.project_root.name,
                'tech_stack': 'To be analyzed',
                'architecture': 'To be analyzed',
                'project_root': str(self.project_root),
                'feature_request': kwargs.get('feature_request', 'General project analysis'),
                'directory_structure': directory_structure,
                'key_files_content': key_files_content
            }
            
            # Try to load and use template
            template_path = Path(__file__).parent / "templates" / "project_analysis_template.md"
            
            try:
                analysis_prompt = self._load_and_prepare_template(template_path, template_context)
            except (FileNotFoundError, Exception) as template_error:
                # Fall back to hardcoded prompt if template fails
                self._log_error(f"Template loading failed: {template_error}. Using fallback prompt.")
                analysis_prompt = f"""
Please analyze the following project structure and provide a comprehensive summary.

PROJECT DIRECTORY STRUCTURE:
{directory_structure}

KEY FILES CONTENT:
{key_files_content}

Please provide:
1. Project type/technology stack identification
2. Main components and their purposes
3. Project architecture overview
4. Key dependencies and technologies used
5. Development setup requirements
6. Any notable patterns or conventions observed

Keep the analysis concise but comprehensive, focusing on information that would be useful for other development agents working on this project.
"""

            # Use LLM to generate analysis if available
            if self.llm_manager:
                try:
                    analysis_result = self.llm_manager.execute(
                        analysis_prompt, 
                        agent_name="project_analysis_agent"
                    )
                    
                    # Store the analysis in context manager
                    if self.context_manager is not None:
                        self.context_manager.set(
                            "project_analysis_summary", 
                            analysis_result
                        )
                        self.context_manager.set(
                            "project_structure", 
                            directory_structure
                        )
                    
                    return f"Project analysis completed successfully. Analysis stored in context manager.\n\nSummary:\n{analysis_result}"
                    
                except Exception as e:
                    error_msg = f"LLM analysis failed: {e}"
                    
                    # Still store basic structure info even if LLM fails
                    if self.context_manager is not None:
                        self.context_manager.set(
                            "project_structure", 
                            directory_structure
                        )
                        self.context_manager.set(
                            "project_analysis_error", 
                            error_msg
                        )
                    
                    return f"Project structure mapped, but LLM analysis failed: {e}\n\nDirectory structure stored in context manager."
            else:
                # Store basic structure info when no LLM available
                if self.context_manager is not None:
                    self.context_manager.set(
                        "project_structure", 
                        directory_structure
                    )
                
                return f"Project structure analysis completed (no LLM available for detailed analysis).\n\nStructure:\n{directory_structure}"
                
        except Exception as e:
            error_msg = f"Project analysis failed: {e}"
            
            if self.context_manager is not None:
                self.context_manager.set("project_analysis_error", error_msg)
            
            return error_msg