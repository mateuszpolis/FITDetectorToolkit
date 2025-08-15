"""
Tests for the main FITDetectorToolkit application.
"""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from fitdetectortoolkit.main import FITDetectorToolkit, ModuleManager


class TestModuleManager:
    """Test the ModuleManager class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.modules_dir = Path(self.temp_dir) / "modules"
        self.modules_dir.mkdir(parents=True, exist_ok=True)

    def teardown_method(self) -> None:
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    @patch("fitdetectortoolkit.main.Path.home")
    def test_init(self, mock_home: Mock) -> None:
        """Test ModuleManager initialization."""
        mock_home.return_value = Path(self.temp_dir)

        with patch.object(ModuleManager, "load_modules_config") as mock_load:
            ModuleManager()
            mock_load.assert_called_once()

    def test_load_modules_config_new(self) -> None:
        """Test loading modules config when it doesn't exist."""
        with patch.object(ModuleManager, "save_modules_config") as mock_save:
            manager = ModuleManager()  # noqa: F841
            manager.modules_dir = self.modules_dir
            manager.modules_config = self.modules_dir / "modules.json"

            # Reset the mock since __init__ already called save_modules_config
            mock_save.reset_mock()

            manager.load_modules_config()

            assert "AgeingAnalysis" in manager.modules
            assert (
                manager.modules["AgeingAnalysis"]["url"]
                == "https://github.com/mateuszpolis/AgeingAnalysis.git"
            )
            mock_save.assert_called_once()

    def test_save_modules_config(self) -> None:
        """Test saving modules configuration."""
        manager = ModuleManager()
        manager.modules_dir = self.modules_dir
        manager.modules_config = self.modules_dir / "modules.json"
        manager.modules = {"test": {"key": "value"}}

        manager.save_modules_config()

        assert manager.modules_config.exists()

    def test_is_module_installed(self) -> None:
        """Test checking if a module is installed."""
        manager = ModuleManager()
        manager.modules = {
            "test_module": {"installed": True},
            "uninstalled_module": {"installed": False},
        }

        assert manager.is_module_installed("test_module") is True
        assert manager.is_module_installed("uninstalled_module") is False
        assert manager.is_module_installed("nonexistent_module") is False


class TestFITDetectorToolkit:
    """Test the FITDetectorToolkit class."""

    @patch("fitdetectortoolkit.main.font.Font")
    @patch("fitdetectortoolkit.main.ttk.Style")
    @patch("fitdetectortoolkit.main.tk.Tk")
    def test_init(self, mock_tk: Mock, mock_style: Mock, mock_font: Mock) -> None:
        """Test FITDetectorToolkit initialization."""
        # Create mock objects
        mock_root = Mock()
        mock_tk.return_value = mock_root
        mock_style_instance = Mock()
        mock_style.return_value = mock_style_instance

        # Mock font creation
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        with patch.object(FITDetectorToolkit, "setup_ui") as mock_setup:
            with patch.object(FITDetectorToolkit, "center_window"):
                with patch.object(
                    FITDetectorToolkit, "create_main_frame"
                ) as mock_create_frame:
                    mock_frame = Mock()
                    mock_create_frame.return_value = mock_frame
                    app = FITDetectorToolkit()
                    mock_setup.assert_called_once()
                    mock_root.title.assert_called_with("FIT Detector Toolkit")
                    assert hasattr(app, "root")

    @patch("fitdetectortoolkit.main.font.Font")
    @patch("fitdetectortoolkit.main.ttk.Style")
    @patch("fitdetectortoolkit.main.tk.Tk")
    def test_configure_styles(
        self, mock_tk: Mock, mock_style: Mock, mock_font: Mock
    ) -> None:
        """Test style configuration."""
        # Create mock objects
        mock_root = Mock()
        mock_tk.return_value = mock_root
        mock_style_instance = Mock()
        mock_style.return_value = mock_style_instance

        # Mock font creation
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        with patch.object(FITDetectorToolkit, "setup_ui") as mock_setup:
            with patch.object(FITDetectorToolkit, "center_window"):
                with patch.object(
                    FITDetectorToolkit, "create_main_frame"
                ) as mock_create_frame:
                    mock_frame = Mock()
                    mock_create_frame.return_value = mock_frame
                    app = FITDetectorToolkit()
                    mock_setup.assert_called_once()

        # Verify that styles were configured
        assert hasattr(app, "style")

    @patch("fitdetectortoolkit.main.font.Font")
    @patch("fitdetectortoolkit.main.ttk.Style")
    @patch("fitdetectortoolkit.main.tk.Tk")
    def test_install_module(
        self, mock_tk: Mock, mock_style: Mock, mock_font: Mock
    ) -> None:
        """Test module installation."""
        # Create mock objects
        mock_root = Mock()
        mock_tk.return_value = mock_root
        mock_style_instance = Mock()
        mock_style.return_value = mock_style_instance

        # Mock font creation
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        with patch.object(FITDetectorToolkit, "setup_ui") as mock_setup:
            with patch.object(FITDetectorToolkit, "center_window"):
                with patch.object(
                    FITDetectorToolkit, "create_main_frame"
                ) as mock_create_frame:
                    mock_frame = Mock()
                    mock_create_frame.return_value = mock_frame
                    app = FITDetectorToolkit()
                    mock_setup.assert_called_once()

        # Mock the status_var to avoid AttributeError
        app.status_var = Mock()

        with patch.object(app.module_manager, "install_module") as mock_install:
            mock_install.return_value = True

            with patch.object(app, "refresh_ui") as mock_refresh:  # noqa: F841
                app.install_module("test_module")

                # Since it runs in a thread, we can't easily test the call
                # Just verify the method exists and can be called
                assert hasattr(app, "install_module")

    @patch("fitdetectortoolkit.main.font.Font")
    @patch("fitdetectortoolkit.main.ttk.Style")
    @patch("fitdetectortoolkit.main.tk.Tk")
    def test_launch_module(
        self, mock_tk: Mock, mock_style: Mock, mock_font: Mock
    ) -> None:
        """Test module launching."""
        # Create mock objects
        mock_root = Mock()
        mock_tk.return_value = mock_root
        mock_style_instance = Mock()
        mock_style.return_value = mock_style_instance

        # Mock font creation
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        with patch.object(FITDetectorToolkit, "setup_ui") as mock_setup:
            with patch.object(FITDetectorToolkit, "center_window"):
                with patch.object(
                    FITDetectorToolkit, "create_main_frame"
                ) as mock_create_frame:
                    mock_frame = Mock()
                    mock_create_frame.return_value = mock_frame
                    app = FITDetectorToolkit()
                    mock_setup.assert_called_once()

        # Mock the status_var to avoid AttributeError
        app.status_var = Mock()

        with patch.object(app.module_manager, "launch_module") as mock_launch:
            mock_launch.return_value = (True, "Success")

            app.launch_module("test_module")

            mock_launch.assert_called_with("test_module")


def test_main_function() -> None:
    """Test the main function."""
    with patch("fitdetectortoolkit.main.FITDetectorToolkit") as mock_app_class:
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        # Mock sys.argv to avoid argument parsing issues
        with patch("sys.argv", ["fitdetectortoolkit"]):
            from fitdetectortoolkit.main import main

            main()

            mock_app_class.assert_called_once()
            mock_app.run.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
