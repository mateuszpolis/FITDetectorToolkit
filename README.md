# FIT Detector Toolkit

A modular Python toolkit for detector analysis that automatically manages and launches analysis modules from GitHub repositories.

## Features

- **Modular Design**: Easily add and manage analysis modules from GitHub repositories
- **Automatic Installation**: One-click installation of modules with dependency management
- **Beautiful GUI**: Modern, intuitive tkinter-based interface
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Extensible**: Simple configuration to add new modules

## Installation

### Prerequisites

- Python 3.8 or higher
- Git

### Install FITDetectorToolkit

```bash
# Clone the repository
git clone https://github.com/mateuszpolis/FITDetectorToolkit.git
cd FITDetectorToolkit

# Install in development mode
pip install -e .
```

## Usage

### Launch the Application

```bash
# Run the main application
python -m fitdetectortoolkit.main

# Or use the command-line entry point
fitdetectortoolkit
```

### Using the GUI

1. **Launch the Application**: Start the FITDetectorToolkit application
2. **Install Modules**: Click the "Install" button next to any module you want to use
3. **Launch Modules**: Once installed, click "Launch" to run the analysis module
4. **Monitor Status**: Check the status bar at the bottom for installation and launch progress

## Available Modules

### AgeingAnalysis
- **Repository**: https://github.com/mateuszpolis/AgeingAnalysis
- **Description**: Analysis tools for detector ageing studies
- **Entry Point**: `ageing_analysis.main`

## Adding New Modules

To add a new module to the toolkit:

1. **Edit the Configuration**: Modify the `modules` dictionary in `ModuleManager.load_modules_config()`
2. **Module Configuration**:
   ```python
   "ModuleName": {
       "url": "https://github.com/username/repository.git",
       "branch": "main",
       "description": "Description of the module",
       "entry_point": "module.package.main",
       "installed": False,
       "version": "latest"
   }
   ```

### Module Requirements

- Must have a `pyproject.toml` or `setup.py` for installation
- Should have a main entry point function
- Repository should be publicly accessible

## Development

### Project Structure

```
FITDetectorToolkit/
├── fitdetectortoolkit/
│   ├── __init__.py          # Package initialization
│   └── main.py              # Main application
├── tests/                   # Test files
├── pyproject.toml          # Project configuration
├── setup.py                # Setup script
└── README.md               # This file
```

### Running Tests

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run with coverage
pytest --cov=fitdetectortoolkit
```

### Code Style

The project uses:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

```bash
# Format code
black .

# Check linting
flake8

# Type checking
mypy fitdetectortoolkit/
```

## Configuration

The toolkit stores module configurations in:
- **Location**: `~/.fitdetectortoolkit/modules/modules.json`
- **Format**: JSON configuration file
- **Auto-generated**: Created on first run

## Troubleshooting

### Common Issues

1. **Module Installation Fails**
   - Check internet connection
   - Verify repository URL is correct
   - Ensure repository is publicly accessible

2. **Module Launch Fails**
   - Verify module is properly installed
   - Check entry point configuration
   - Review module's main function

3. **Permission Errors**
   - Ensure write permissions to `~/.fitdetectortoolkit/`
   - Run with appropriate user permissions

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
export FITDETECTOR_DEBUG=1
python -m fitdetectortoolkit.main
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- **Mateusz Polis** - *Initial work* - [mateuszpolis](https://github.com/mateuszpolis)

## Acknowledgments

- CERN for the detector analysis context
- The Python community for excellent tools and libraries 