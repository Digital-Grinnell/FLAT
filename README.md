# FLAT - Flet Layout Application Template

FLAT is a template for building desktop applications with [Flet](https://flet.dev). It provides a clean starting point with essential features like persistent settings, logging, function management, and help documentation built-in.

## Features

### Core Template Features
- **Persistent Settings**: Automatic saving/loading of window position and user preferences
- **Logging System**: Organized log files with timestamps in `~/FLAT-data/logfiles/`
- **Function Management**: Dropdown-based function selection with usage tracking
- **Help Mode**: Built-in markdown help system for each function
- **Directory Pickers**: Input and output directory selection with state persistence
- **Status Bar**: User-friendly status messages at bottom of window
- **Clean UI Layout**: Professional desktop application appearance

### Example Functions Included
- **Function 1**: List all files in a directory
- **Function 2**: Count files by extension type
- **Function 3**: Display system information

These examples demonstrate the function pattern and can be replaced with your own functionality.

## Quick Start

### Running from Source

1. **Clone or copy this template**
   ```bash
   cd /path/to/your/projects
   cp -r FLAT my-new-app
   cd my-new-app
   ```

2. **Run the application**
   ```bash
   # macOS/Linux
   ./run.sh
   
   # Windows
   run.bat
   ```

The run scripts automatically:
- Create a Python virtual environment
- Install dependencies
- Launch the application

## Requirements

- **Python 3.8+**
- **Flet 0.25.2** (installed automatically by run scripts)

No other dependencies required for the base template.

## Project Structure

```
FLAT/
├── app.py                      # Main application file
├── run.sh                      # macOS/Linux launcher
├── run.bat                     # Windows launcher
├── python_requirements.txt     # Python dependencies
├── .gitignore                  # Git exclusions
├── FUNCTION_1_LIST_FILES.md    # Help documentation for Function 1
├── FUNCTION_2_COUNT_FILES.md   # Help documentation for Function 2
├── FUNCTION_3_SYSTEM_INFO.md   # Help documentation for Function 3
└── README.md                   # This file
```

### Runtime Files
When you run the application, these are created automatically:
```
~/FLAT-data/
├── logfiles/                   # Application logs
│   └── flat_YYYYMMDD_HHMMSS.log
└── persistent.json             # Saved settings and state
```

## Customizing FLAT for Your Application

### 1. Rename the Application

Update these items throughout the codebase:
- `page.title` in `app.py`
- Data directory name (`FLAT-data` → `YourApp-data`)
- Window title and header text
- Script headers in `run.sh` and `run.bat`
- README title and descriptions

### 2. Add Your Own Functions

To add a new function:

**a) Create the function handler in `app.py`:**

```python
def on_function_4_your_feature():
    """Your Function 4: Description."""
    storage.record_function_usage("Function 4")
    
    # Your implementation here
    if not input_dir_text.value:
        show_status("Error: Please select an input directory first", is_error=True)
        return
    
    # ... do work ...
    
    show_status("Your feature completed successfully")
    logger.info("Function 4: Completed")
```

**b) Add to the function dropdown:**

```python
function_options = [
    # ... existing options ...
    ft.dropdown.Option("4", "4: Your New Feature"),
]
```

**c) Register in the function map:**

```python
function_map = {
    "1": on_function_1_list_files,
    "2": on_function_2_count_files,
    "3": on_function_3_system_info,
    "4": on_function_4_your_feature,  # Add this
}
```

**d) Create help documentation:**

Create `FUNCTION_4_YOUR_FEATURE.md` with documentation, then add it to the help files mapping:

```python
help_files = {
    "1": "FUNCTION_1_LIST_FILES.md",
    "2": "FUNCTION_2_COUNT_FILES.md",
    "3": "FUNCTION_3_SYSTEM_INFO.md",
    "4": "FUNCTION_4_YOUR_FEATURE.md",  # Add this
}
```

### 3. Add Dependencies

If your functions need additional Python packages:

1. Add them to `python_requirements.txt`:
   ```
   flet==0.25.2
   flet-desktop==0.25.2
   your-package>=1.0.0
   ```

2. Import them in `app.py`:
   ```python
   try:
       import your_package
       YOUR_PACKAGE_AVAILABLE = True
   except ImportError:
       YOUR_PACKAGE_AVAILABLE = False
   ```

3. Check availability before use:
   ```python
   if not YOUR_PACKAGE_AVAILABLE:
       show_status("Error: your-package not installed", is_error=True)
       return
   ```

### 4. Modify UI Layout

The layout is defined in the `page.add()` section at the bottom of `app.py`. The structure uses Flet containers and rows:

```python
page.add(
    ft.Container(
        content=ft.Column([
            # Your UI components here
        ]),
        padding=30,
    )
)
```

Add your own UI elements:
- `ft.TextField()` - Text input fields
- `ft.Dropdown()` - Dropdown menus
- `ft.Checkbox()` - Checkboxes
- `ft.ElevatedButton()` - Buttons
- `ft.Text()` - Labels and text
- `ft.Row()` and `ft.Column()` - Layout containers

See [Flet documentation](https://flet.dev/docs/) for all available controls.

### 5. Persistent Settings

To save additional settings:

```python
# Save a custom setting
storage.set_ui_state("my_custom_field", "value")

# Load a custom setting
value = storage.get_ui_state("my_custom_field", default="default_value")
```

All settings are automatically saved to `~/FLAT-data/persistent.json`.

### 6. Remove Example Functions

Once you've built your own functions, remove the examples:

1. Delete functions from `app.py`: `on_function_1_list_files`, etc.
2. Delete help files: `FUNCTION_1_LIST_FILES.md`, etc.
3. Update `function_options` and `function_map` in `app.py`

## Building Standalone Packages

### macOS DMG

Create a distributable DMG file:

```bash
bash build_dmg.sh 1.0
```

This creates `YourApp_v1.0.dmg` with:
- Self-contained app bundle
- Automatic dependency installation on first launch
- No code signing (users must right-click → Open on first launch)

### Windows ZIP

Create a distributable ZIP package:

```bash
bash build_windows_zip.sh 1.0
```

This creates `YourApp_v1.0_Windows.zip` with:
- All source files
- `run.bat` launcher
- Automatic dependency installation on first launch

Recipients need Python 3 installed (one-time setup).

## Logging

All application activity is logged to:
```
~/FLAT-data/logfiles/flat_YYYYMMDD_HHMMSS.log
```

Use the logger in your functions:
```python
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
logger.debug("Debug message")
```

Console output shows only errors; all levels are written to log files.

## Help Documentation

Help files use GitHub Flavored Markdown and support:
- Headers (`#`, `##`, `###`)
- Lists (ordered and unordered)
- Code blocks with syntax highlighting
- Tables
- Links
- **Bold** and *italic* text

Create help documentation for each function to guide users.

## Examples of Apps Built with This Template

- **OHM - Oral History Manager**: Audio processing workflow for digital archives
- *(Add your own app here!)*

## Tips for Development

### Testing Your Changes

After modifying `app.py`, just rerun:
```bash
./run.sh  # or run.bat on Windows
```

The virtual environment and dependencies are cached, so subsequent runs are fast.

### Debugging

- Check log files in `~/FLAT-data/logfiles/` for errors
- Console shows error-level messages immediately
- Use `logger.debug()` for detailed troubleshooting

### Version Control

Initialize a git repository for your new app:
```bash
git init
git add .
git commit -m "Initial commit based on FLAT template"
```

The included `.gitignore` excludes:
- Virtual environments (`.venv/`)
- Python cache (`__pycache__/`)
- Log files
- Build artifacts

## Flet Resources

- **Documentation**: https://flet.dev/docs/
- **Controls Gallery**: https://flet.dev/docs/controls
- **GitHub**: https://github.com/flet-dev/flet
- **Discord**: https://discord.gg/dzWXP8SHG8

## License

This template is provided as-is for building your own applications. Modify freely.

## About

FLAT was created to provide a solid starting point for Flet desktop applications without the overhead of reinventing common patterns like settings persistence, logging, and help systems.

Built with ❤️ using [Flet](https://flet.dev)
