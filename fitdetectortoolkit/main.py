"""
Main application for FITDetectorToolkit.

Provides a graphical interface for managing and launching detector analysis modules.
"""

import json
import os
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import font, messagebox, ttk
from typing import Tuple, Union

from git import Repo


class BaseGUI:
    """Base class for GUI components with common styling and utilities."""

    def __init__(self, root: Union[tk.Tk, None] = None) -> None:
        """Initialize the base GUI with common styles and utilities.

        Args:
            root (tk.Tk, optional): The root Tkinter window. If None, a new one is
                created.
        """
        self.root = root if root else tk.Tk()

        # Set application icon if available
        self._set_application_icon()

        # Create custom fonts
        self.header_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)
        self.button_font = font.Font(family="Helvetica", size=10, weight="bold")
        self.monospace_font = font.Font(family="Courier New", size=10)

        # Create a style for ttk widgets
        self.style = ttk.Style()
        self.style.configure("TButton", font=self.button_font)
        self.style.configure("TLabel", font=self.normal_font)
        self.style.configure("Header.TLabel", font=self.header_font)
        self.style.configure("Title.TLabel", font=self.title_font)

        # Configure progress bar style
        self.style.configure(
            "Analysis.Horizontal.TProgressbar",
            troughcolor="#E0E0E0",
            background="#4CAF50",
            thickness=20,
        )

        # Configure button styles
        self.style.configure(
            "Primary.TButton", background="#4CAF50", foreground="white"
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", "#45a049"), ("pressed", "#3d8b40")],
        )

        self.style.configure(
            "Secondary.TButton", background="#2196F3", foreground="white"
        )
        self.style.map(
            "Secondary.TButton",
            background=[("active", "#0b7dda"), ("pressed", "#0a69b7")],
        )

    def _set_application_icon(self) -> None:
        """Set the application icon if available."""
        try:
            # Use a path relative to the script location,
            # not the current working directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(
                os.path.dirname(script_dir)
            )  # Go up two levels

            # Try different methods based on platform
            if sys.platform == "win32":
                icon_path = os.path.join(project_root, "assets", "icon.ico")
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
            else:
                # For macOS and Linux
                try:
                    from PIL import Image, ImageTk

                    icon_path = os.path.join(project_root, "assets", "icon.png")
                    if os.path.exists(icon_path):
                        icon = ImageTk.PhotoImage(Image.open(icon_path))
                        self.root.iconphoto(True, icon)
                except Exception:  # nosec B110 - Silent fallback is intentional
                    pass  # Silently fail if PIL is not available or other errors occur
        except Exception:  # nosec B110 - Silent fallback is intentional
            pass  # Silently fail if icon setting fails

    def create_main_frame(self, padding: str = "20 20 20 20") -> ttk.Frame:
        """Create a main frame with padding.

        Args:
            padding (str, optional): Padding specification. Defaults to "20 20 20 20".

        Returns:
            ttk.Frame: The created main frame.
        """
        main_frame = ttk.Frame(self.root, padding=padding)
        main_frame.pack(fill=tk.BOTH, expand=True)
        return main_frame

    def create_status_bar(
        self, parent_frame: ttk.Frame
    ) -> Tuple[ttk.Frame, tk.StringVar]:
        """Create a status bar at the bottom of the parent frame.

        Args:
            parent_frame (ttk.Frame): The parent frame to add the status bar to.

        Returns:
            Tuple[ttk.Frame, tk.StringVar]: The status frame and status text variable.
        """
        # Create a frame for the status bar
        status_frame = ttk.Frame(parent_frame, relief=tk.SUNKEN)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a string variable to hold the status message
        status_var = tk.StringVar()

        # Create a label to display the status message
        status_label = ttk.Label(status_frame, textvariable=status_var, anchor=tk.W)
        status_label.pack(fill=tk.X, padx=5, pady=2)

        return status_frame, status_var

    def set_window_properties(
        self,
        title: str,
        geometry: str = "900x700",
        min_size: Tuple[int, int] = (800, 600),
    ) -> None:
        """Set window properties for the application.

        Args:
            title (str): The window title.
            geometry (str, optional): The window geometry. Defaults to "900x700".
            min_size (tuple, optional): The minimum window size. Defaults to (800, 600).
        """
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.minsize(min_size[0], min_size[1])
        # Center window on screen
        self.center_window()

    def center_window(self) -> None:
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_separator(
        self, parent_frame: ttk.Frame, padding: Tuple[int, int] = (5, 10)
    ) -> ttk.Separator:
        """Create a horizontal separator in the parent frame.

        Args:
            parent_frame (ttk.Frame): The parent frame to add the separator to.
            padding (tuple, optional): Padding for the separator. Defaults to (5, 10).

        Returns:
            ttk.Separator: The created separator.
        """
        separator = ttk.Separator(parent_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=padding[0], pady=padding[1])
        return separator


class ModuleManager:
    """Manages the installation and execution of external modules."""

    def __init__(self) -> None:
        self.modules_dir = Path.home() / ".fitdetectortoolkit" / "modules"
        self.modules_dir.mkdir(parents=True, exist_ok=True)
        self.modules_config = self.modules_dir / "modules.json"
        self.load_modules_config()

    def load_modules_config(self) -> None:
        """Load the modules configuration file."""
        if self.modules_config.exists():
            with open(self.modules_config, "r") as f:
                self.modules = json.load(f)
        else:
            self.modules = {
                "AgeingAnalysis": {
                    "url": "https://github.com/mateuszpolis/AgeingAnalysis.git",
                    "branch": "main",
                    "description": "Analyze and visualize ageing factors in the FIT "
                    "detector.",
                    "entry_point": "ageing_analysis.main",
                    "installed": False,
                    "version": "latest",
                    "icon": "📊",
                }
            }
            self.save_modules_config()

    def save_modules_config(self) -> None:
        """Save the modules configuration file."""
        with open(self.modules_config, "w") as f:
            json.dump(self.modules, f, indent=2)

    def install_module(self, module_name: str) -> bool:
        """Install a module from GitHub."""
        try:
            module_info = self.modules[module_name]
            module_path = self.modules_dir / module_name

            if module_path.exists():
                shutil.rmtree(module_path)

            # Clone the repository
            Repo.clone_from(
                module_info["url"], module_path, branch=module_info["branch"]
            )

            # Check for pyproject.toml (preferred) or setup.py
            pyproject_toml = module_path / "pyproject.toml"
            setup_py = module_path / "setup.py"

            if not pyproject_toml.exists() and not setup_py.exists():
                raise FileNotFoundError(
                    f"Neither pyproject.toml nor setup.py found in {module_name}"
                )

            # Prefer pyproject.toml over setup.py
            if pyproject_toml.exists():
                print(f"Installing {module_name} using pyproject.toml...")
                # Install the module using pyproject.toml
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-e", str(module_path)],
                    check=True,
                    capture_output=True,
                )
            else:
                print(
                    f"Warning: {module_name} uses setup.py (pyproject.toml preferred)"
                )
                # Fallback to setup.py if pyproject.toml doesn't exist
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-e", str(module_path)],
                    check=True,
                    capture_output=True,
                )

            module_info["installed"] = True
            self.save_modules_config()
            return True

        except Exception as e:
            print(f"Error installing {module_name}: {e}")
            return False

    def is_module_installed(self, module_name: str) -> bool:
        """Check if a module is installed."""
        module = self.modules.get(module_name, {})
        installed = module.get("installed", False)
        return bool(installed)

    def launch_module(self, module_name: str) -> Tuple[bool, str]:
        """Launch a module."""
        try:
            module_info = self.modules[module_name]
            module_path = self.modules_dir / module_name

            if not module_info["installed"]:
                return False, "Module not installed"

            # Always use subprocess to avoid threading issues with GUI modules
            if "entry_point" in module_info:
                # Try to run the module using python -m
                try:
                    # First try to run as a module
                    subprocess.Popen([sys.executable, "-m", module_info["entry_point"]])
                    return True, "Module launched successfully"
                except Exception:
                    # If that fails, try to run the main function directly
                    try:
                        import importlib

                        module = importlib.import_module(module_info["entry_point"])
                        if hasattr(module, "main"):
                            # Run in a separate process to avoid threading issues
                            cmd = f"import {module_info['entry_point']};"
                            cmd += f" {module_info['entry_point']}.main()"
                            subprocess.Popen([sys.executable, "-c", cmd])
                            return True, "Module launched successfully"
                        else:
                            return False, "No main function found in module"
                    except Exception as e:
                        return False, f"Error importing module: {e}"
            else:
                # Try to run the module directory directly
                subprocess.Popen([sys.executable, str(module_path)])
                return True, "Module launched successfully"

        except Exception as e:
            return False, f"Error launching module: {e}"


class FITDetectorToolkit(BaseGUI):
    """Main application class for FITDetectorToolkit."""

    def __init__(self, root: Union[tk.Tk, None] = None) -> None:
        """Initialize the FIT Detector Toolkit application.

        Args:
            root (tk.Tk, optional): The root Tkinter window. If None, a new one is
                created.
        """
        super().__init__(root)
        self.set_window_properties("FIT Detector Toolkit", geometry="1200x800")

        # Create main frame with padding
        self.main_frame = self.create_main_frame()

        self.module_manager = ModuleManager()
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        # Create the UI elements
        self._create_header_section()
        self._create_app_launcher_section()
        self._create_footer_section()

    def _create_header_section(self) -> None:
        """Create the header section with title and description."""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        # Title
        title_label = ttk.Label(
            header_frame, text="FIT Detector Toolkit", style="Title.TLabel"
        )
        title_label.pack(pady=(0, 10))

        # Description
        description_text = (
            "Welcome to the FIT Detector Toolkit. This application provides "
            "a suite of tools for working with the FIT detector system."
        )
        description_label = ttk.Label(
            header_frame, text=description_text, wraplength=700
        )
        description_label.pack(pady=(0, 15))

        # Separator
        self.create_separator(header_frame)

    def _create_app_launcher_section(self) -> None:
        """Create the application launcher section with cards for each tool."""
        launcher_frame = ttk.Frame(self.main_frame)
        launcher_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Create a frame for tool cards
        tools_frame = ttk.Frame(launcher_frame)
        tools_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Get tools from module manager
        tools = []
        for module_name, module_info in self.module_manager.modules.items():
            tools.append(
                {
                    "name": module_name,
                    "description": module_info.get(
                        "description", "No description available"
                    ),
                    "icon": module_info.get("icon", "🔧"),
                    "installed": module_info.get("installed", False),
                    "module_name": module_name,
                }
            )

        # Create a card for each tool
        for i, tool in enumerate(tools):
            self._create_tool_card(tools_frame, tool, i)

    def _create_tool_card(self, parent: ttk.Frame, tool: dict, index: int) -> None:
        """Create a card for a tool in the launcher.

        Args:
            parent (ttk.Frame): The parent frame to add the card to.
            tool (dict): Dictionary with tool information.
            index (int): The index of the tool for determining its position.
        """
        card_frame = ttk.Frame(parent, borderwidth=2, relief=tk.GROOVE)

        # Calculate position (2 cards per row)
        row = index // 2
        col = index % 2

        # Place the card in a grid layout
        card_frame.grid(
            row=row, column=col, padx=20, pady=20, sticky="nsew", ipadx=20, ipady=20
        )

        # Configure grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

        # Icon
        icon_label = ttk.Label(card_frame, text=tool["icon"], font=("Helvetica", 36))
        icon_label.pack(pady=(15, 10))

        # Tool name
        name_label = ttk.Label(card_frame, text=tool["name"], style="Header.TLabel")
        name_label.pack(pady=(0, 10))

        # Tool description
        desc_label = ttk.Label(
            card_frame, text=tool["description"], wraplength=250, justify=tk.CENTER
        )
        desc_label.pack(pady=(0, 15))

        # Status indicator
        status_text = "✓ Installed" if tool["installed"] else "✗ Not Installed"
        status_color = "#27ae60" if tool["installed"] else "#e74c3c"

        status_label = ttk.Label(
            card_frame,
            text=status_text,
            foreground=status_color,
            font=("Arial", 10),
        )
        status_label.pack(pady=(0, 15))

        # Buttons frame
        buttons_frame = ttk.Frame(card_frame)
        buttons_frame.pack(pady=(0, 15))

        # Install button
        install_button = ttk.Button(
            buttons_frame,
            text="Install",
            command=lambda: self.install_module(tool["module_name"]),
            style="Primary.TButton",
            width=12,
        )
        install_button.pack(side=tk.LEFT, padx=(0, 5))

        # Launch button
        launch_button = ttk.Button(
            buttons_frame,
            text="Launch",
            command=lambda: self.launch_module(tool["module_name"]),
            style="Primary.TButton",
            width=12,
        )
        launch_button.pack(side=tk.LEFT, padx=(5, 0))

        # Disable launch button if not installed
        if not tool["installed"]:
            launch_button.configure(state="disabled")

    def _create_footer_section(self) -> None:
        """Create the footer section with status bar and version information."""
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(15, 0))

        # Version information
        version = "0.1.0"
        version_label = ttk.Label(footer_frame, text=f"Version {version}")
        version_label.pack(side=tk.RIGHT, padx=(0, 10))

        # Separator
        self.create_separator(footer_frame, padding=(0, 10))

        # Create status bar
        _, self.status_var = self.create_status_bar(footer_frame)
        self.status_var.set("Ready")

    def install_module(self, module_name: str) -> None:  # noqa: C901
        """Install a module in a separate thread."""

        def install_thread() -> None:
            try:
                self.status_var.set(f"Installing {module_name}...")
                success = self.module_manager.install_module(module_name)

                if success:
                    self.status_var.set(f"{module_name} installed successfully!")
                    try:
                        messagebox.showinfo(
                            "Success", f"{module_name} has been installed successfully!"
                        )
                    except tk.TclError:
                        # Window was closed, just update status
                        pass
                    # Refresh the UI
                    self.refresh_ui()
                else:
                    self.status_var.set(f"Failed to install {module_name}")
                    try:
                        messagebox.showerror(
                            "Error", f"Failed to install {module_name}"
                        )
                    except tk.TclError:
                        # Window was closed, just update status
                        pass
            except Exception as e:
                self.status_var.set(f"Error during installation: {e}")

        threading.Thread(target=install_thread, daemon=True).start()

    def launch_module(self, module_name: str) -> None:  # noqa: C901
        """Launch a module."""

        def launch_thread() -> None:
            try:
                self.status_var.set(f"Launching {module_name}...")
                success, message = self.module_manager.launch_module(module_name)

                if success:
                    self.status_var.set(f"{module_name} launched successfully!")
                else:
                    self.status_var.set(f"Failed to launch {module_name}")
                    try:
                        messagebox.showerror(
                            "Error", f"Failed to launch {module_name}: {message}"
                        )
                    except tk.TclError:
                        # Window was closed, just update status
                        pass
            except Exception as e:
                self.status_var.set(f"Error during launch: {e}")

        # For GUI modules, we need to run in the main thread
        # For now, let's use subprocess to avoid threading issues
        try:
            self.status_var.set(f"Launching {module_name}...")
            success, message = self.module_manager.launch_module(module_name)

            if success:
                self.status_var.set(f"{module_name} launched successfully!")
            else:
                self.status_var.set(f"Failed to launch {module_name}")
                try:
                    messagebox.showerror(
                        "Error", f"Failed to launch {module_name}: {message}"
                    )
                except tk.TclError:
                    # Window was closed, just update status
                    pass
        except Exception as e:
            self.status_var.set(f"Error during launch: {e}")
            try:
                messagebox.showerror("Error", f"Error launching {module_name}: {e}")
            except tk.TclError:
                pass

    def refresh_ui(self) -> None:
        """Refresh the user interface."""
        # Clear and recreate the modules section
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()

    def run(self) -> None:
        """Run the application."""
        self.root.mainloop()


def main() -> None:
    """Main entry point for the application."""
    import argparse

    parser = argparse.ArgumentParser(
        description="FIT Detector Toolkit - A modular toolkit for detector analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fitdetectortoolkit                    # Launch the GUI
  fitdetectortoolkit --list-modules     # List available modules
  fitdetectortoolkit --install AgeingAnalysis  # Install a module
        """,
    )

    parser.add_argument(
        "--list-modules",
        action="store_true",
        help="List all available modules and their status",
    )

    parser.add_argument("--install", metavar="MODULE", help="Install a specific module")

    parser.add_argument("--launch", metavar="MODULE", help="Launch a specific module")

    parser.add_argument(
        "--version", action="version", version="FITDetectorToolkit 0.1.0"
    )

    args = parser.parse_args()

    # Handle command-line operations
    if args.list_modules:
        manager = ModuleManager()
        print("Available modules:")
        print("=" * 50)
        for module_name, module_info in manager.modules.items():
            status = (
                "✓ Installed"
                if module_info.get("installed", False)
                else "✗ Not Installed"
            )
            print(f"{module_name}: {status}")
            print(f"  Description: {module_info.get('description', 'No description')}")
            print(f"  Repository: {module_info.get('url', 'No URL')}")
            print()
        return

    if args.install:
        manager = ModuleManager()
        print(f"Installing {args.install}...")
        success = manager.install_module(args.install)
        if success:
            print(f"✓ {args.install} installed successfully!")
        else:
            print(f"✗ Failed to install {args.install}")
        return

    if args.launch:
        manager = ModuleManager()
        if not manager.is_module_installed(args.launch):
            print(f"✗ {args.launch} is not installed. Install it first.")
            return

        print(f"Launching {args.launch}...")
        success, message = manager.launch_module(args.launch)
        if success:
            print(f"✓ {args.launch} launched successfully!")
        else:
            print(f"✗ Failed to launch {args.launch}: {message}")
        return

    # Default: launch GUI
    app = FITDetectorToolkit()
    app.run()


if __name__ == "__main__":
    main()
