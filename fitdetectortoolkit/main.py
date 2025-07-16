"""
Main application for FITDetectorToolkit.

Provides a graphical interface for managing and launching detector analysis modules.
"""

import json
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Tuple

from git import Repo


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
                    "description": "Analysis tools for detector ageing studies",
                    "entry_point": "ageing_analysis.main",
                    "installed": False,
                    "version": "latest",
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


class FITDetectorToolkit:
    """Main application class for FITDetectorToolkit."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("FIT Detector Toolkit")
        self.root.geometry("800x600")
        self.root.configure(bg="#2b2b2b")

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        self.module_manager = ModuleManager()
        self.setup_ui()

    def configure_styles(self) -> None:
        """Configure custom styles for the application."""
        # Configure colors
        self.style.configure(
            "Title.TLabel",
            background="#2b2b2b",
            foreground="#ffffff",
            font=("Arial", 16, "bold"),
        )

        self.style.configure(
            "Module.TFrame", background="#3c3c3c", relief="raised", borderwidth=2
        )

        self.style.configure(
            "Module.TLabel",
            background="#3c3c3c",
            foreground="#ffffff",
            font=("Arial", 10),
        )

        self.style.configure(
            "Module.TButton",
            background="#4a90e2",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
        )

        self.style.map("Module.TButton", background=[("active", "#357abd")])

    def setup_ui(self) -> None:
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, style="Module.TFrame")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(
            main_frame, text="FIT Detector Toolkit", style="Title.TLabel"
        )
        title_label.pack(pady=(0, 20))

        # Subtitle
        subtitle_label = ttk.Label(
            main_frame, text="Available Analysis Modules", style="Module.TLabel"
        )
        subtitle_label.pack(pady=(0, 20))

        # Modules frame
        modules_frame = ttk.Frame(main_frame, style="Module.TFrame")
        modules_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create scrollable canvas for modules
        canvas = tk.Canvas(modules_frame, bg="#3c3c3c", highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            modules_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas, style="Module.TFrame")

        def configure_scroll_region(event: tk.Event) -> None:
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", configure_scroll_region)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add modules
        self.create_module_widgets(scrollable_frame)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            main_frame, textvariable=self.status_var, style="Module.TLabel"
        )
        status_bar.pack(side="bottom", fill="x", pady=(10, 0))

        # Bind mouse wheel to canvas
        def _on_mousewheel(event: tk.Event) -> None:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_module_widgets(self, parent: tk.ttk.Frame) -> None:
        """Create widgets for each available module."""
        for module_name, module_info in self.module_manager.modules.items():
            # Module container
            module_frame = ttk.Frame(parent, style="Module.TFrame")
            module_frame.pack(fill="x", padx=10, pady=5)

            # Module info frame
            info_frame = ttk.Frame(module_frame, style="Module.TFrame")
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            # Module name
            name_label = ttk.Label(info_frame, text=module_name, style="Module.TLabel")
            name_label.pack(anchor="w")

            # Module description
            desc_label = ttk.Label(
                info_frame,
                text=module_info.get("description", "No description available"),
                style="Module.TLabel",
            )
            desc_label.pack(anchor="w", pady=(5, 0))

            # Status indicator
            status_text = (
                "✓ Installed"
                if module_info.get("installed", False)
                else "✗ Not Installed"
            )
            status_color = (
                "#4CAF50" if module_info.get("installed", False) else "#f44336"
            )

            status_label = ttk.Label(
                info_frame,
                text=status_text,
                foreground=status_color,
                style="Module.TLabel",
            )
            status_label.pack(anchor="w", pady=(5, 0))

            # Buttons frame
            buttons_frame = ttk.Frame(module_frame, style="Module.TFrame")
            buttons_frame.pack(side="right", padx=10, pady=10)

            # Install button
            def install_callback() -> None:
                self.install_module(module_name)

            install_btn = ttk.Button(
                buttons_frame,
                text="Install",
                style="Module.TButton",
                command=install_callback,
            )
            install_btn.pack(side="top", pady=2)

            # Launch button
            def launch_callback() -> None:
                self.launch_module(module_name)

            launch_btn = ttk.Button(
                buttons_frame,
                text="Launch",
                style="Module.TButton",
                command=launch_callback,
            )
            launch_btn.pack(side="top", pady=2)

            # Disable launch button if not installed
            if not module_info.get("installed", False):
                launch_btn.configure(state="disabled")

    def install_module(self, module_name: str) -> None:
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

    def launch_module(self, module_name: str) -> None:
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
