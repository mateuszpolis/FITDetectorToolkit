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
│   └── main.py              # Main application
├── tests/                   # Test files
├── examples/                # Usage examples
├── scripts/                 # Development scripts
├── .github/workflows/       # GitHub Actions
├── pyproject.toml          # Project configuration
├── setup.py                # Setup script
├── package.json            # Node.js dependencies
├── .releaserc.json         # Semantic release config
├── .pre-commit-config.yaml # Pre-commit hooks
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
# Install hooks
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

1. **Tests**: Runs on multiple Python versions and OS
2. **Code Quality**: Black, Flake8, MyPy, Bandit
3. **Security**: Safety checks
4. **Release**: Automatic semantic versioning

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
