# FLAT Changelog

All notable changes to the FLAT (Flet Layout Application Template) project are documented in this file.

---

## [1.0.0] - 2026-05-04

### Initial Release

FLAT is a template for building desktop applications with Flet. It was created by extracting and generalizing the core framework from the OHM (Oral History Manager) application.

### Features

- **Persistent Settings System**
  - Automatic save/restore of window position
  - User preferences storage in JSON format
  - Function usage tracking with timestamps and counts
  - Stored in `~/FLAT-data/persistent.json`

- **Logging System**
  - Timestamped log files in `~/FLAT-data/logfiles/`
  - Separate file and console handlers
  - Configurable log levels
  - Reduced verbosity for Flet internal logging

- **UI Framework**
  - Input and output directory pickers with persistence
  - Function dropdown with numeric ordering
  - Help mode for viewing documentation
  - Status bar for user feedback
  - Professional desktop application layout

- **Example Functions**
  - Function 1: List all files in a directory
  - Function 2: Count files by extension type
  - Function 3: Display system information
  - Each function includes markdown help documentation

- **Distribution Tools**
  - `build_dmg.sh`: Create macOS DMG installers
  - `build_windows_zip.sh`: Create Windows ZIP packages
  - Both include automatic dependency installation on first launch

- **Development Tools**
  - `run.sh`: macOS/Linux launcher with venv management
  - `run.bat`: Windows launcher with venv management
  - `.gitignore`: Sensible exclusions for Python/Flet projects
  - `python_requirements.txt`: Minimal Flet dependencies

### Documentation

- Comprehensive README with:
  - Quick start guide
  - Customization instructions
  - How to add new functions
  - How to modify UI layout
  - Building standalone packages
  - Flet resources and tips

- Function-specific help documentation:
  - `FUNCTION_1_LIST_FILES.md`
  - `FUNCTION_2_COUNT_FILES.md`
  - `FUNCTION_3_SYSTEM_INFO.md`

### Technical Details

- Built with Flet 0.25.2
- Python 3.8+ required
- No external dependencies beyond Flet
- Cross-platform: macOS, Windows, Linux

---

## Future Development

FLAT is a starting template. When you create your own application from FLAT:

1. Update the changelog with your app's version history
2. Replace example functions with your own
3. Customize the UI to match your needs
4. Add any additional dependencies required

---

## Credits

FLAT was derived from the OHM (Oral History Manager) project, which demonstrated effective patterns for Flet desktop applications including persistent settings, logging, function management, and help documentation.

Built with [Flet](https://flet.dev) - a Python framework for building desktop applications.
