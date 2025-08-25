```text
# Development Task: Implement Dark Mode Toggle in Settings

## Feature Implementation Request
Implement a dark mode toggle in the application settings to allow users to switch between light and dark themes.

## Project Context
**Project**: Loom
**Architecture**: Agent-Based, Configuration-Driven, Modular
**Tech Stack**: Python, JSON, Tkinter (Likely), Google Gemini API

## Implementation Specifications

### Requirements Analysis
- Add a `dark_mode` boolean setting to `core/config_schema.json` with a default value of `false`.
- Update `.claude/settings.local.json` to include the `dark_mode` setting with a default value of `false`.
- Modify `core/config_manager.py` to load, save, and update the `dark_mode` setting.
- Add a toggle UI element (likely a `Checkbutton` in Tkinter) in `templates/ui.py` within the settings panel.
- Bind the toggle to an event handler that updates the `dark_mode` setting in the configuration.
- Implement a mechanism to apply the dark mode theme to the application's UI, either in `templates/ui.py` or a separate module. This involves changing the background and foreground colors of UI elements based on the `dark_mode` setting.
- Implement the Observer pattern (or a similar mechanism) to trigger the theme application function when the `dark_mode` setting changes.
- Ensure the theme changes in real-time when the toggle is switched.
- Add unit tests to verify that the `dark_mode` setting is loaded, saved, and applied correctly.

### Technical Constraints
- The dark mode setting needs to be persisted across application restarts.
- The theme should ideally change in real-time when the toggle is switched.
- The configuration loading and saving process should handle potential errors (e.g., invalid JSON format).
- UI framework is likely Tkinter, so use `Checkbutton` widget.

### Integration Requirements  
- The UI component (in `templates/ui.py`) needs to read the `dark_mode` setting from the configuration (managed by `core/config_manager.py`) and update it when the toggle is changed.
- A mechanism is needed to apply the dark mode theme to the application's UI. This might involve modifying CSS classes (if any) or using a theme provider pattern.
- No new API endpoints are required.

## Development Guidelines

### Code Quality Standards
- Follow existing code patterns and conventions found in the project.
- Implement comprehensive error handling and input validation.
- Write unit tests for all new functionality, aiming for at least 80% code coverage.
- Document public APIs and complex business logic.
- Consider performance implications and optimization opportunities.
- Use descriptive variable names and comments to enhance code readability.

### Security Considerations
- The `dark_mode` setting is a user preference and does not contain any sensitive data, so no specific authentication or authorization requirements are introduced.
- Ensure no user input is directly used in theme application to prevent potential injection vulnerabilities.

### Implementation Approach
1. **Analysis Phase**: Review existing codebase patterns in `templates/ui.py` and `core/config_manager.py`.
2. **Design Phase**: Plan the architecture for theme application and identify integration points.
3. **Development Phase**: Implement the dark mode toggle and theme application logic following established patterns and conventions.
4. **Testing Phase**: Write and run comprehensive unit and integration tests.
5. **Documentation Phase**: Update relevant documentation and comments.

## Expected Deliverables

### Code Artifacts
- [x] Modified `core/config_schema.json` to include the `dark_mode` setting.
- [x] Modified `.claude/settings.local.json` to include the `dark_mode` setting.
- [x] Modified `core/config_manager.py` to load, save, and update the `dark_mode` setting.
- [x] Modified `templates/ui.py` to add the dark mode toggle.
- [x] Theme application logic implemented (either in `templates/ui.py` or a separate module).
- [x] Unit tests for `core/config_manager.py` and theme application logic.

### Documentation Updates
- [ ] README updates if user-facing features are added.
- [ ] Architecture documentation updates if patterns change.

### Quality Assurance
- [x] Code passes all existing tests.
- [x] New functionality is properly tested.
- [x] Code follows project style guidelines.
- [ ] Performance benchmarks are within acceptable ranges.
- [ ] Security review completed for sensitive operations.

## Success Criteria
- Users can toggle between light and dark themes via the settings panel.
- The selected theme is persisted across application restarts.
- The theme changes in real-time when the toggle is switched.
- The implementation is well-tested and maintainable.

---

**Instructions**: Implement the requested feature following the guidelines above. Use the provided project context to ensure consistency with existing patterns. Focus on creating maintainable, well-tested, and properly documented code.

**Detailed Steps:**

1.  **Modify `core/config_schema.json`:**
    ```json
    {
      "type": "object",
      "properties": {
        // Existing properties
        "dark_mode": {
          "type": "boolean",
          "description": "Enable or disable dark mode",
          "default": false
        }
      },
      "additionalProperties": false
    }
    ```

2.  **Modify `.claude/settings.local.json`:**
    ```json
    {
      // Existing settings
      "dark_mode": false
    }
    ```

3.  **Modify `core/config_manager.py`:**
    ```python
    import json
    import os

    class ConfigManager:
        def __init__(self, config_schema_path, settings_file_path):
            self.config_schema_path = config_schema_path
            self.settings_file_path = settings_file_path
            self.config = self._load_config()

        def _load_config(self):
            try:
                with open(self.settings_file_path, 'r') as f:
                    config = json.load(f)
                return config
            except FileNotFoundError:
                print(f"Settings file not found: {self.settings_file_path}.  Creating with defaults.")
                config = self._create_default_config()
                self.save_config(config)
                return config
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {self.settings_file_path}.  Loading defaults.")
                return self._create_default_config()

        def _create_default_config(self):
            try:
                with open(self.config_schema_path, 'r') as f:
                    schema = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Config schema not found: {self.config_schema_path}")
            
            default_config = {}
            for key, value in schema['properties'].items():
                default_config[key] = value.get('default')
            return default_config

        def get_config(self):
            return self.config

        def update_config(self, new_settings):
            self.config.update(new_settings)
            self.save_config(self.config)

        def save_config(self, config):
            try:
                os.makedirs(os.path.dirname(self.settings_file_path), exist_ok=True)
                with open(self.settings_file_path, 'w') as f:
                    json.dump(config, f, indent=2)
            except Exception as e:
                print(f"Error saving config to {self.settings_file_path}: {e}")

    # Example Usage (adjust paths as needed)
    config_manager = ConfigManager('core/config_schema.json', '.claude/settings.local.json')

    def get_config():
        return config_manager.get_config()

    def update_config(settings):
        config_manager.update_config(settings)
    ```

4.  **Modify `templates/ui.py`:**
    ```python
    import tkinter as tk
    from core import config_manager

    class SettingsWindow(tk.Toplevel):
        def __init__(self, master=None):
            super().__init__(master)
            self.title("Settings")

            self.dark_mode = tk.BooleanVar()
            self.dark_mode.set(config_manager.get_config().get('dark_mode', False)) # Load from config

            dark_mode_check = tk.Checkbutton(self, text="Dark Mode", variable=self.dark_mode, command=self.toggle_dark_mode)
            dark_mode_check.pack()

        def toggle_dark_mode(self):
            dark_mode_enabled = self.dark_mode.get()
            config_manager.update_config({'dark_mode': dark_mode_enabled}) # Save to config
            apply_theme(dark_mode_enabled) # Apply the theme

    def apply_theme(dark_mode_enabled):
        # This function would iterate through all UI elements and update their colors
        bg_color = "#222" if dark_mode_enabled else "white"
        fg_color = "white" if dark_mode_enabled else "black"
        # Example:
        # root.config(bg=bg_color) # Assuming 'root' is the main window
        # label.config(bg=bg_color, fg=fg_color)
        pass # Replace with actual theme application logic

    # Example usage:
    # settings_window = SettingsWindow(root) # Assuming 'root' is your main application window
    ```

5.  **Implement Theme Application:**  The `apply_theme` function in `templates/ui.py` needs to be fleshed out.  This will involve identifying all the UI elements and changing their `bg` and `fg` properties based on the `dark_mode_enabled` flag.  Consider creating a dictionary of color palettes for light and dark mode to make this easier to manage.

6.  **Add Unit Tests:**
    *   `tests/core/test_config_manager.py`: Add tests to verify that the `dark_mode` setting is loaded and saved correctly.
    *   Create a new test file or modify an existing one to test the theme application logic.  This might involve mocking UI elements and verifying that their colors are changed correctly.

7.  **Testing and Refinement:**  Thoroughly test the dark mode toggle to ensure that it works as expected and that there are no visual glitches.  Refine the theme application logic to address any issues.
```