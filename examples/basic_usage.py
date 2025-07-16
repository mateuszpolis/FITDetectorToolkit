#!/usr/bin/env python3
"""
Basic usage example for FITDetectorToolkit.

This script demonstrates how to use the toolkit programmatically
without the GUI interface.
"""

import sys
from pathlib import Path

# Add the parent directory to the path to import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from fitdetectortoolkit.main import ModuleManager


def main():
    """Demonstrate basic usage of the ModuleManager."""
    print("FITDetectorToolkit - Basic Usage Example")
    print("=" * 50)
    
    # Initialize the module manager
    manager = ModuleManager()
    
    # List available modules
    print("\nAvailable modules:")
    for module_name, module_info in manager.modules.items():
        status = "✓ Installed" if module_info.get('installed', False) else "✗ Not Installed"
        print(f"  - {module_name}: {status}")
        print(f"    Description: {module_info.get('description', 'No description')}")
        print(f"    Repository: {module_info.get('url', 'No URL')}")
        print()
    
    # Example: Install a module (commented out to avoid actual installation)
    # print("Installing AgeingAnalysis module...")
    # success = manager.install_module("AgeingAnalysis")
    # if success:
    #     print("✓ AgeingAnalysis installed successfully!")
    # else:
    #     print("✗ Failed to install AgeingAnalysis")
    
    # Example: Launch a module (commented out to avoid actual launch)
    # if manager.is_module_installed("AgeingAnalysis"):
    #     print("Launching AgeingAnalysis...")
    #     success, message = manager.launch_module("AgeingAnalysis")
    #     if success:
    #         print("✓ AgeingAnalysis launched successfully!")
    #     else:
    #         print(f"✗ Failed to launch AgeingAnalysis: {message}")
    # else:
    #     print("AgeingAnalysis is not installed. Install it first.")
    
    print("\nTo run the GUI version, use:")
    print("  python -m fitdetectortoolkit.main")
    print("  or")
    print("  fitdetectortoolkit")


if __name__ == "__main__":
    main() 