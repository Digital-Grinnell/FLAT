"""
FLAT - Flet Layout Application Template
A template Flet desktop application with persistent settings, logging,
function management, and help documentation system.
"""

import flet as ft
import os
import getpass
import logging
import json
import platform
import socket
from datetime import datetime
from pathlib import Path

# Configure logging
DATA_DIR = Path.home() / "FLAT-data"
os.makedirs(DATA_DIR / "logfiles", exist_ok=True)
log_filename = DATA_DIR / "logfiles" / f"flat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])
logger = logging.getLogger(__name__)

# Reduce Flet's logging verbosity
logging.getLogger("flet").setLevel(logging.WARNING)
logging.getLogger("flet_core").setLevel(logging.WARNING)
logging.getLogger("flet_desktop").setLevel(logging.WARNING)

# Persistent storage file
PERSISTENCE_FILE = DATA_DIR / "persistent.json"


class PersistentStorage:
    """Handle persistent storage of UI state and function usage."""

    def __init__(self):
        self.data = self.load()

    def load(self) -> dict:
        """Load persistent data from file."""
        try:
            if os.path.exists(PERSISTENCE_FILE):
                with open(PERSISTENCE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logger.info(f"Loaded persistent data from {PERSISTENCE_FILE}")
                return data
        except Exception as e:
            logger.warning(f"Could not load persistent data: {str(e)}")

        return {
            "ui_state": {
                "last_input_dir": "",
                "last_output_dir": "",
                "window_left": None,
                "window_top": None,
            },
            "function_usage": {},
        }

    def save(self):
        """Save persistent data to file."""
        try:
            with open(PERSISTENCE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved persistent data to {PERSISTENCE_FILE}")
        except Exception as e:
            logger.error(f"Could not save persistent data: {str(e)}")

    def set_ui_state(self, field: str, value: str):
        """Update UI state field."""
        self.data["ui_state"][field] = value
        self.save()

    def get_ui_state(self, field: str, default: str = "") -> str:
        """Get UI state field."""
        return self.data["ui_state"].get(field, default)

    def record_function_usage(self, function_name: str):
        """Record that a function was used."""
        if function_name not in self.data["function_usage"]:
            self.data["function_usage"][function_name] = {"count": 0}

        self.data["function_usage"][function_name]["last_used"] = datetime.now().isoformat()
        self.data["function_usage"][function_name]["count"] = (
            self.data["function_usage"][function_name].get("count", 0) + 1
        )
        self.save()

    def get_function_usage(self, function_name: str) -> dict:
        """Get usage stats for a function."""
        return self.data["function_usage"].get(
            function_name, {"last_used": None, "count": 0}
        )

    def get_all_function_usage(self) -> dict:
        """Get all function usage stats."""
        return self.data["function_usage"]


def load_help_document(filename: str) -> str:
    """Load help documentation from markdown file."""
    try:
        help_path = Path(__file__).parent / filename
        if help_path.exists():
            return help_path.read_text(encoding="utf-8")
        else:
            return f"# Help Documentation Not Found\n\nCould not find {filename}"
    except Exception as e:
        logger.error(f"Error loading help document {filename}: {e}")
        return f"# Error Loading Help\n\n{str(e)}"


def main(page: ft.Page):
    page.title = "FLAT - Flet Layout Application Template"
    page.window.width = 800
    page.window.height = 600
    
    # Initialize persistent storage
    storage = PersistentStorage()
    
    # Restore window position if saved
    saved_left = storage.get_ui_state("window_left")
    saved_top = storage.get_ui_state("window_top")
    if saved_left is not None and saved_top is not None:
        page.window.left = saved_left
        page.window.top = saved_top
    
    # Status text at bottom
    status_text = ft.Text("Ready", size=12, color=ft.colors.GREY_700)
    
    def show_status(message: str, is_error: bool = False):
        """Display a status message."""
        status_text.value = message
        status_text.color = ft.colors.RED_700 if is_error else ft.colors.GREY_700
        page.update()
        logger.info(f"Status: {message}")
    
    # Input directory
    input_dir_text = ft.TextField(
        label="Input Directory",
        value=storage.get_ui_state("last_input_dir"),
        expand=True,
        read_only=True,
    )
    
    def on_input_dir_picked(e: ft.FilePickerResultEvent):
        if e.path:
            input_dir_text.value = e.path
            storage.set_ui_state("last_input_dir", e.path)
            show_status(f"Input directory set: {e.path}")
            page.update()
    
    input_dir_picker = ft.FilePicker(on_result=on_input_dir_picked)
    page.overlay.append(input_dir_picker)
    
    def on_browse_input_clicked(e):
        input_dir_picker.get_directory_path(dialog_title="Select Input Directory")
    
    browse_input_button = ft.ElevatedButton(
        "Browse...",
        on_click=on_browse_input_clicked,
        icon=ft.icons.FOLDER_OPEN,
    )
    
    # Output directory
    output_dir_text = ft.TextField(
        label="Output Directory",
        value=storage.get_ui_state("last_output_dir"),
        expand=True,
        read_only=True,
    )
    
    def on_output_dir_picked(e: ft.FilePickerResultEvent):
        if e.path:
            output_dir_text.value = e.path
            storage.set_ui_state("last_output_dir", e.path)
            show_status(f"Output directory set: {e.path}")
            page.update()
    
    output_dir_picker = ft.FilePicker(on_result=on_output_dir_picked)
    page.overlay.append(output_dir_picker)
    
    def on_browse_output_clicked(e):
        output_dir_picker.get_directory_path(dialog_title="Select Output Directory")
    
    browse_output_button = ft.ElevatedButton(
        "Browse...",
        on_click=on_browse_output_clicked,
        icon=ft.icons.FOLDER_OPEN,
    )
    
    # Help mode checkbox
    help_mode_checkbox = ft.Checkbox(
        label="Help Mode",
        value=False,
        tooltip="Enable to view help documentation instead of running functions",
    )
    
    # Function dropdown
    function_options = [
        ft.dropdown.Option("1", "1: Example Function - List Files"),
        ft.dropdown.Option("2", "2: Example Function - Count Files"),
        ft.dropdown.Option("3", "3: Example Function - System Info"),
    ]
    
    function_dropdown = ft.Dropdown(
        label="Select Function",
        hint_text="Choose a function to execute",
        options=function_options,
        width=400,
    )
    
    # ==================== FUNCTION IMPLEMENTATIONS ====================
    
    def on_function_1_list_files():
        """Example Function 1: List all files in input directory."""
        storage.record_function_usage("Function 1")
        
        if not input_dir_text.value:
            show_status("Error: Please select an input directory first", is_error=True)
            return
        
        input_path = Path(input_dir_text.value)
        if not input_path.exists():
            show_status(f"Error: Directory does not exist: {input_path}", is_error=True)
            return
        
        # Count files
        files = list(input_path.glob("*"))
        file_list = [f.name for f in files if f.is_file()]
        
        # Create result dialog
        result_text = f"Found {len(file_list)} file(s) in {input_path.name}:\n\n"
        result_text += "\n".join(f"• {name}" for name in sorted(file_list)) if file_list else "(No files found)"
        
        def close_dialog(e):
            dialog.open = False
            page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Function 1: List Files"),
            content=ft.Text(result_text, selectable=True),
            actions=[ft.TextButton("Close", on_click=close_dialog)],
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        
        show_status(f"Listed {len(file_list)} file(s)")
        logger.info(f"Function 1: Listed {len(file_list)} files from {input_path}")
    
    def on_function_2_count_files():
        """Example Function 2: Count files by extension."""
        storage.record_function_usage("Function 2")
        
        if not input_dir_text.value:
            show_status("Error: Please select an input directory first", is_error=True)
            return
        
        input_path = Path(input_dir_text.value)
        if not input_path.exists():
            show_status(f"Error: Directory does not exist: {input_path}", is_error=True)
            return
        
        # Count by extension
        ext_counts = {}
        for file_path in input_path.glob("*"):
            if file_path.is_file():
                ext = file_path.suffix.lower() or "(no extension)"
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
        
        # Create result dialog
        result_text = f"File count by extension in {input_path.name}:\n\n"
        if ext_counts:
            for ext, count in sorted(ext_counts.items(), key=lambda x: x[1], reverse=True):
                result_text += f"• {ext}: {count}\n"
        else:
            result_text += "(No files found)"
        
        def close_dialog(e):
            dialog.open = False
            page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Function 2: Count Files by Extension"),
            content=ft.Text(result_text, selectable=True),
            actions=[ft.TextButton("Close", on_click=close_dialog)],
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        
        total = sum(ext_counts.values())
        show_status(f"Counted {total} file(s) across {len(ext_counts)} extension(s)")
        logger.info(f"Function 2: Counted files by extension in {input_path}")
    
    def on_function_3_system_info():
        """Example Function 3: Display system information."""
        storage.record_function_usage("Function 3")
        
        # Gather system info
        info_lines = [
            f"Hostname: {socket.gethostname()}",
            f"OS: {platform.system()} {platform.release()}",
            f"Machine: {platform.machine()}",
            f"Python: {platform.python_version()}",
            f"User: {getpass.getuser()}",
            f"Data Directory: {DATA_DIR}",
        ]
        
        result_text = "System Information:\n\n" + "\n".join(f"• {line}" for line in info_lines)
        
        def close_dialog(e):
            dialog.open = False
            page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Function 3: System Info"),
            content=ft.Text(result_text, selectable=True),
            actions=[ft.TextButton("Close", on_click=close_dialog)],
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        
        show_status("Displayed system information")
        logger.info("Function 3: Displayed system information")
    
    def show_help_dialog(function_num: str):
        """Display help documentation for a function."""
        help_files = {
            "1": "FUNCTION_1_LIST_FILES.md",
            "2": "FUNCTION_2_COUNT_FILES.md",
            "3": "FUNCTION_3_SYSTEM_INFO.md",
        }
        
        help_filename = help_files.get(function_num, "")
        if not help_filename:
            show_status(f"No help available for function {function_num}", is_error=True)
            return
        
        help_content = load_help_document(help_filename)
        
        def close_help(e):
            help_dialog.open = False
            page.update()
        
        help_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Help: Function {function_num}"),
            content=ft.Container(
                content=ft.Markdown(
                    help_content,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                ),
                width=700,
                height=500,
            ),
            actions=[ft.TextButton("Close", on_click=close_help)],
        )
        
        page.overlay.append(help_dialog)
        help_dialog.open = True
        page.update()
        
        logger.info(f"Displayed help for Function {function_num}")
    
    def on_function_selected(e):
        """Handle function selection and execution."""
        if not function_dropdown.value:
            return
        
        function_num = function_dropdown.value
        
        # Show help if help mode is enabled
        if help_mode_checkbox.value:
            show_help_dialog(function_num)
            return
        
        # Execute the selected function
        function_map = {
            "1": on_function_1_list_files,
            "2": on_function_2_count_files,
            "3": on_function_3_system_info,
        }
        
        function = function_map.get(function_num)
        if function:
            logger.info(f"Executing Function {function_num}")
            function()
        else:
            show_status(f"Function {function_num} not implemented", is_error=True)
    
    execute_button = ft.ElevatedButton(
        "Execute Function",
        on_click=on_function_selected,
        icon=ft.icons.PLAY_ARROW,
    )
    
    # ==================== LAYOUT ====================
    
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    # Header
                    ft.Container(
                        content=ft.Text(
                            "FLAT - Flet Layout Application Template",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
                        padding=ft.padding.only(bottom=20),
                    ),
                    
                    # Input/Output Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Directories", size=16, weight=ft.FontWeight.BOLD),
                            ft.Row([input_dir_text, browse_input_button]),
                            ft.Row([output_dir_text, browse_output_button]),
                        ]),
                        padding=ft.padding.only(bottom=20),
                    ),
                    
                    # Functions Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Functions", size=16, weight=ft.FontWeight.BOLD),
                            ft.Row([help_mode_checkbox]),
                            ft.Row([function_dropdown, execute_button]),
                        ]),
                        padding=ft.padding.only(bottom=20),
                    ),
                    
                    # Status bar
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.INFO_OUTLINE, size=16, color=ft.colors.GREY_700),
                            status_text,
                        ]),
                        padding=ft.padding.only(top=20),
                        border=ft.border.only(top=ft.border.BorderSide(1, ft.colors.GREY_300)),
                    ),
                ],
                spacing=10,
            ),
            padding=30,
        )
    )
    
    # Save window position on close
    def on_window_event(e):
        if e.data == "close":
            storage.set_ui_state("window_left", page.window.left)
            storage.set_ui_state("window_top", page.window.top)
    
    page.window.on_event = on_window_event
    
    show_status("Application ready")
    logger.info("FLAT application started")


if __name__ == "__main__":
    ft.app(target=main)
