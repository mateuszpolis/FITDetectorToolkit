# FIT Detector Toolkit

A modular Python toolkit for **offline analysis related to the FIT detector** that automatically manages and launches analysis modules from GitHub repositories.

## Overview

The FIT Detector Toolkit is designed specifically for researchers and engineers working with the FIT detector system. It provides a centralized platform to discover, install, and launch various analysis tools and modules that help with detector calibration, data analysis, ageing studies, and other offline analysis tasks.

## Features

- **FIT Detector Focus**: Specifically designed for FIT detector offline analysis
- **Modular Design**: Easily add and manage analysis modules from GitHub repositories
- **Automatic Installation**: One-click installation of modules with dependency management
- **Beautiful GUI**: Modern, card-based tkinter interface with professional styling
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Extensible**: Simple configuration to add new modules
- **Quality Assurance**: Integrated CI/CD pipeline ensures code quality and security

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
2. **Browse Modules**: View available analysis modules in the card-based interface
3. **Install Modules**: Click the "Install" button next to any module you want to use
4. **Launch Modules**: Once installed, click "Launch" to run the analysis module
5. **Monitor Status**: Check the status bar at the bottom for installation and launch progress

### Command Line Usage

```bash
# List available modules
fitdetectortoolkit --list-modules

# Install a specific module
fitdetectortoolkit --install AgeingAnalysis

# Launch a specific module
fitdetectortoolkit --launch AgeingAnalysis
```

## Available Modules

### AgeingAnalysis
- **Repository**: https://github.com/mateuszpolis/AgeingAnalysis
- **Description**: Analysis tools for detector ageing studies and visualization
- **Entry Point**: `ageing_analysis.main`
- **Icon**: 📊

## Adding New Modules

### For End Users

To add a new module to the toolkit, you need to:

1. **Fork the repository** to your GitHub account
2. **Create a feature branch** for your changes
3. **Add module configuration** to the toolkit
4. **Submit a Pull Request** for review and merging

**⚠️ IMPORTANT: You cannot push directly to the main branch. All changes must go through Pull Requests.**

### Module Configuration

To add a new module, edit the `modules` dictionary in `ModuleManager.load_modules_config()`:

```python
"YourNewModule": {
    "url": "https://github.com/yourusername/your-module.git",
    "branch": "main",
    "description": "Brief description of what your module does for FIT detector analysis.",
    "entry_point": "your_module.main",
    "installed": False,
    "version": "latest",
    "icon": "🔬",  # Choose an appropriate emoji icon
}
```

### Module Requirements

Your module must meet these requirements to be compatible:

- **Repository Structure**: Must have `pyproject.toml` (preferred) or `setup.py`
- **Entry Point**: Must have a `main()` function that serves as the entry point
- **Installation**: Must be installable with `pip install -e .`
- **Purpose**: Should perform offline analysis related to the FIT detector
- **Standalone**: Should work independently of the toolkit

### Detailed Guidelines

For comprehensive module development guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md#module-development-guidelines).

## Development

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/mateuszpolis/FITDetectorToolkit.git
cd FITDetectorToolkit

# Run the setup script (recommended)
./scripts/setup-dev.sh

# Or manually:
pip install -e .[dev]
pre-commit install --hook-type pre-commit
pre-commit install --hook-type commit-msg
npm install
```

### Project Structure

```
FITDetectorToolkit/
├── fitdetectortoolkit/
│   ├── __init__.py          # Package initialization
│   └── main.py              # Main application with BaseGUI
├── tests/                   # Test files
├── examples/                # Usage examples
├── scripts/                 # Development scripts
├── .github/workflows/       # GitHub Actions CI/CD
├── pyproject.toml          # Project configuration
├── setup.py                # Setup script
├── package.json            # Node.js dependencies
├── .releaserc.json         # Semantic release config
├── .pre-commit-config.yaml # Pre-commit hooks
├── CONTRIBUTING.md         # Contribution guidelines
├── LICENSE                 # MIT License
└── README.md               # This file
```

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:

- **Commitizen**: Enforces conventional commit messages
- **Black**: Code formatting
- **Flake8**: Linting
- **isort**: Import sorting
- **MyPy**: Type checking
- **Bandit**: Security checks
- **pytest**: Test running

```bash
# Install hooks (MANDATORY for contributors)
pre-commit install --hook-type pre-commit
pre-commit install --hook-type commit-msg

# Run manually
pre-commit run --all-files
```

### Commit Message Format

The project uses [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```bash
git commit -m "feat: add new module installation feature"
git commit -m "fix: resolve threading issue in GUI"
git commit -m "docs: update installation instructions"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=fitdetectortoolkit --cov-report=html

# Run specific test file
pytest tests/test_main.py -v
```

### Code Quality Checks

```bash
# Format code
black .

# Sort imports
isort .

# Check linting
flake8

# Type checking
mypy fitdetectortoolkit/

# Security scan
bandit -r .
```

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

1. **Code Quality**: Black, Flake8, MyPy, Bandit, isort
2. **Tests**: Runs on Python 3.8-3.12 across Ubuntu, macOS, and Windows
3. **Security**: Bandit vulnerability scanning and Safety dependency checks
4. **Release**: Automatic semantic versioning

**⚠️ IMPORTANT: All CI checks must pass before Pull Requests can be merged.**

### Automatic Releases

Releases are automatically created based on commit messages:

- `feat:` → Minor version bump
- `fix:` → Patch version bump
- `BREAKING CHANGE:` → Major version bump

The release process:
1. Analyzes commit messages
2. Determines next version
3. Updates version files
4. Creates GitHub release
5. Publishes to PyPI (if configured)

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
   - Check that the module has proper `pyproject.toml` or `setup.py`

2. **Module Launch Fails**
   - Verify module is properly installed
   - Check entry point configuration
   - Review module's main function
   - Ensure the module has a `main()` function

3. **Permission Errors**
   - Ensure write permissions to `~/.fitdetectortoolkit/`
   - Run with appropriate user permissions

4. **CI Pipeline Failures**
   - Run `pre-commit run --all-files` locally
   - Ensure all tests pass with `pytest`
   - Check code formatting with `black .` and `isort .`

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
export FITDETECTOR_DEBUG=1
python -m fitdetectortoolkit.main
```

## Contributing

We welcome contributions! However, please note our contribution policy:

**⚠️ CRITICAL: You CANNOT push directly to the main branch!**

### Contribution Process

1. **Fork the repository** to your GitHub account
2. **Create a feature branch** for your changes
3. **Install pre-commit hooks** (mandatory)
4. **Make your changes** following our code standards
5. **Test thoroughly** - ensure all tests pass
6. **Submit a Pull Request** for review and merging

### Before Contributing

- **Read [CONTRIBUTING.md](CONTRIBUTING.md)** for detailed guidelines
- **Install pre-commit hooks** to ensure code quality
- **Run tests locally** before submitting
- **Follow commit message conventions**

### CI Requirements

Your Pull Request must pass all CI checks:
- Code quality (Black, Flake8, MyPy, Bandit, isort)
- Tests on all supported Python versions and OS
- Security scanning
- Code coverage requirements

**If any check fails, your PR cannot be merged until it's fixed.**

For detailed contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- **Mateusz Polis** - *Initial work* - [mateuszpolis](https://github.com/mateuszpolis)

## Acknowledgments

- **CERN** for the detector analysis context and FIT detector system
- The **Python community** for excellent tools and libraries
- **Contributors** who help improve the toolkit

## Support

- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/mateuszpolis/FITDetectorToolkit/issues)
- **Discussions**: Ask questions and share ideas via [GitHub Discussions](https://github.com/mateuszpolis/FITDetectorToolkit/discussions)
- **Documentation**: See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines
