# Contributing to FIT Detector Toolkit

Thank you for your interest in contributing to FIT Detector Toolkit! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Contribution Workflow](#contribution-workflow)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Adding New Modules](#adding-new-modules)
- [Module Development Guidelines](#module-development-guidelines)
- [Pull Request Process](#pull-request-process)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [Questions and Discussions](#questions-and-discussions)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- **Be respectful** and inclusive of all contributors
- **Be collaborative** and open to different viewpoints
- **Be constructive** in feedback and discussions
- **Be professional** in all interactions

## Contribution Workflow

### Important: Pull Request Only Policy

**⚠️ CRITICAL: You CANNOT push directly to the main branch!**

- **Fork the repository** to your GitHub account
- **Create a feature branch** for your changes
- **Submit a Pull Request** for review and merging
- **All changes must go through Pull Requests** - no direct pushes allowed
- **CI pipelines will run automatically** on all Pull Requests
- **Code quality checks must pass** before merging is allowed

### Why This Policy?

- **Code Quality**: Ensures all code meets our standards
- **Code Review**: Allows maintainers to review changes
- **CI Validation**: Automatically runs tests and quality checks
- **Collaboration**: Fosters discussion and improvement of contributions
- **Safety**: Prevents breaking changes from reaching the main branch

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Node.js 16+ (for development tools)

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/FITDetectorToolkit.git
   cd FITDetectorToolkit
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/mateuszpolis/FITDetectorToolkit.git
   ```

## Development Setup

### Quick Setup (Recommended)

```bash
# Run the automated setup script
./scripts/setup-dev.sh
```

### Manual Setup

```bash
# Install the package in development mode
pip install -e .[dev]

# Install pre-commit hooks (MANDATORY)
pre-commit install --hook-type pre-commit
pre-commit install --hook-type commit-msg

# Install Node.js dependencies
npm install
```

### Verify Setup

```bash
# Run tests to ensure everything works
pytest tests/ -v

# Run code quality checks
pre-commit run --all-files
```

## Code Standards

### Python Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting (line length: 88 characters)
- **isort**: Import sorting and organization
- **Flake8**: Linting and style checking
- **MyPy**: Type checking
- **Bandit**: Security vulnerability scanning

### Code Formatting

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check code quality
flake8
mypy fitdetectortoolkit/
bandit -r .
```

### Type Hints

- Use type hints for all function parameters and return values
- Use `Optional[T]` for parameters that can be `None`
- Use `Union[T1, T2]` for parameters that can be multiple types
- Use `Tuple[T1, T2]` for tuple types

Example:
```python
def process_data(data: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """Process the input data and return success status and message."""
    # ... implementation
```

### Documentation

- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Comments**: Add comments for complex logic
- **README**: Keep documentation up to date

Example docstring:
```python
def install_module(self, module_name: str) -> bool:
    """Install a module from GitHub.

    Args:
        module_name: The name of the module to install.

    Returns:
        True if installation was successful, False otherwise.

    Raises:
        ModuleNotFoundError: If the module configuration is not found.
        GitError: If there's an error cloning the repository.
    """
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=fitdetectortoolkit --cov-report=html

# Run specific test file
pytest tests/test_main.py -v

# Run tests matching a pattern
pytest -k "test_install"
```

### Writing Tests

- **Test coverage**: Aim for at least 80% code coverage
- **Test organization**: Group related tests in classes
- **Test names**: Use descriptive names that explain what is being tested
- **Mocking**: Use mocks for external dependencies (Tkinter, Git, etc.)

Example test:
```python
def test_install_module_success(self):
    """Test successful module installation."""
    # Arrange
    module_name = "test_module"
    mock_git = Mock()

    # Act
    with patch("git.Repo", mock_git):
        result = self.module_manager.install_module(module_name)

    # Assert
    assert result is True
    mock_git.clone_from.assert_called_once()
```

### Test Structure

```
tests/
├── __init__.py
├── test_main.py          # Main application tests
├── test_module_manager.py # Module management tests
├── conftest.py           # Test configuration and fixtures
└── integration/          # Integration tests
    └── test_gui.py
```

## Adding New Modules

### Overview

The FIT Detector Toolkit is designed to launch programs for **offline analysis related to the FIT detector**. New modules should follow this purpose and integrate seamlessly with the toolkit's module management system.

### How to Add a New Module

#### 1. **Fork and Clone** (if you haven't already)
```bash
git clone https://github.com/YOUR_USERNAME/FITDetectorToolkit.git
cd FITDetectorToolkit
git remote add upstream https://github.com/mateuszpolis/FITDetectorToolkit.git
```

#### 2. **Create a Feature Branch**
```bash
git checkout main
git pull upstream main
git checkout -b feature/add-new-module
```

#### 3. **Add Module Configuration**
Edit `fitdetectortoolkit/main.py` and add your module to the `modules` dictionary in the `ModuleManager.load_modules_config()` method:

```python
self.modules = {
    "AgeingAnalysis": {
        "url": "https://github.com/mateuszpolis/AgeingAnalysis.git",
        "branch": "main",
        "description": "Analyze and visualize ageing factors in the FIT detector.",
        "entry_point": "ageing_analysis.main",
        "installed": False,
        "version": "latest",
        "icon": "📊",
    },
    "YourNewModule": {  # Add your module here
        "url": "https://github.com/yourusername/your-module.git",
        "branch": "main",
        "description": "Brief description of what your module does for FIT detector analysis.",
        "entry_point": "your_module.main",
        "installed": False,
        "version": "latest",
        "icon": "🔬",  # Choose an appropriate emoji icon
    }
}
```

#### 4. **Test Your Changes**
```bash
# Run tests to ensure nothing is broken
pytest tests/ -v

# Test the module installation (if you have access to the repository)
python -m fitdetectortoolkit.main --install YourNewModule
```

#### 5. **Commit and Push**
```bash
git add fitdetectortoolkit/main.py
git commit -m "feat: add YourNewModule to toolkit

- Add YourNewModule for FIT detector analysis
- Repository: https://github.com/yourusername/your-module.git
- Entry point: your_module.main"
git push origin feature/add-new-module
```

#### 6. **Create Pull Request**
- Go to your fork on GitHub
- Create a Pull Request to the main repository
- **Base branch**: `main`
- **Title**: `feat: add YourNewModule to toolkit`
- **Description**: Explain what your module does and why it's useful

## Module Development Guidelines

### Module Requirements

To be compatible with the FIT Detector Toolkit, your module must meet these requirements:

#### 1. **Repository Structure**
```
your-module/
├── pyproject.toml        # Preferred (modern Python packaging)
├── setup.py              # Alternative (legacy)
├── README.md             # Clear documentation
├── your_module/          # Main package directory
│   ├── __init__.py
│   └── main.py          # Entry point function
└── requirements.txt      # Dependencies
```

#### 2. **Entry Point Function**
Your module must have a `main()` function that serves as the entry point:

```python
# your_module/main.py
def main():
    """Main entry point for the YourNewModule application."""
    # Your application logic here
    # This function will be called when the user clicks "Launch"
    pass

if __name__ == "__main__":
    main()
```

#### 3. **Installation Compatibility**
- **Prefer `pyproject.toml`** over `setup.py` (modern Python packaging)
- Ensure your module can be installed with `pip install -e .`
- List all dependencies clearly
- Avoid conflicts with existing packages

#### 4. **FIT Detector Focus**
- **Purpose**: Your module should perform offline analysis related to the FIT detector
- **Data Formats**: Support common detector data formats
- **Output**: Provide meaningful analysis results
- **Documentation**: Explain how it relates to FIT detector analysis

#### 5. **User Experience**
- **Standalone**: Should work independently of the toolkit
- **Clear Interface**: Intuitive user interface or command-line interface
- **Error Handling**: Graceful error handling with helpful messages
- **Progress Feedback**: Show progress for long-running operations

### Example Module Structure

```python
# Example: FIT Detector Calibration Module
self.modules = {
    "FITCalibration": {
        "url": "https://github.com/username/fit-calibration.git",
        "branch": "main",
        "description": "Calibrate and validate FIT detector parameters using offline data analysis.",
        "entry_point": "fit_calibration.main",
        "installed": False,
        "version": "latest",
        "icon": "⚡",
    }
}
```

### Testing Your Module

Before submitting a Pull Request:

1. **Test Installation**: Ensure your module installs correctly
2. **Test Launch**: Verify the module launches without errors
3. **Test Integration**: Confirm it works with the toolkit's module manager
4. **Run Toolkit Tests**: Ensure no existing functionality is broken

## Pull Request Process

### Before Submitting

1. **Ensure tests pass**: Run `pytest` locally
2. **Check code quality**: Run `pre-commit run --all-files`
3. **Update documentation**: Update README, docstrings, and other docs as needed
4. **Add tests**: Include tests for new functionality
5. **Verify CI compliance**: Your code must pass all CI checks

### Creating a Pull Request

1. **Create a feature branch** from `main`:
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit them following our commit message guidelines

3. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** on GitHub:
   - **Base branch**: `main`
   - **Title**: Follow commit message format
   - **Description**: Explain what the PR does and why
   - **Checklist**: Use the PR template

### CI Pipeline Requirements

**⚠️ IMPORTANT: All CI checks must pass before merging!**

Your Pull Request will automatically run:

1. **Code Quality Checks**:
   - Black formatting
   - isort import sorting
   - Flake8 linting
   - MyPy type checking
   - Bandit security scanning

2. **Tests**:
   - Python 3.8, 3.9, 3.10, 3.11, 3.12
   - Ubuntu, macOS, Windows
   - Code coverage requirements

3. **Security Scan**:
   - Bandit vulnerability scanning
   - Safety dependency checks

**If any check fails, your PR cannot be merged until it's fixed.**

### Pull Request Template

```markdown
## Description
Brief description of what this PR accomplishes.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] All tests pass locally
- [ ] Code quality checks pass
- [ ] Pre-commit hooks pass

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have installed and configured pre-commit hooks
- [ ] All CI checks pass (code quality, tests, security)
```

## Commit Message Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **`feat`**: New feature
- **`fix`**: Bug fix
- **`docs`**: Documentation changes
- **`style`**: Formatting, missing semi-colons, etc.
- **`refactor`**: Code refactoring
- **`test`**: Adding or updating tests
- **`chore`**: Maintenance tasks, dependencies, etc.
- **`perf`**: Performance improvements
- **`ci`**: CI/CD changes
- **`build`**: Build system changes

### Examples

```bash
git commit -m "feat: add FITCalibration module to toolkit"
git commit -m "fix: resolve threading issue in GUI"
git commit -m "docs: update module development guidelines"
git commit -m "test: add tests for module installation"
git commit -m "refactor: simplify module configuration loading"
```

### Breaking Changes

For breaking changes, add `!:` after the type and include `BREAKING CHANGE:` in the footer:

```bash
git commit -m "feat!: change module configuration format

BREAKING CHANGE: Module configuration now requires 'entry_point' field"
```

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Environment information**:
   - Operating system and version
   - Python version
   - FITDetectorToolkit version

2. **Steps to reproduce**:
   - Clear, step-by-step instructions
   - Sample data if applicable

3. **Expected vs. actual behavior**:
   - What you expected to happen
   - What actually happened

4. **Error messages**:
   - Full error traceback
   - Screenshots if applicable

### Issue Template

```markdown
## Bug Description
Brief description of the bug.

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., macOS 12.0]
- Python: [e.g., 3.11.0]
- FITDetectorToolkit: [e.g., 0.1.0]

## Additional Information
Any other context, logs, or screenshots.
```

## Feature Requests

### Before Requesting

1. **Check existing issues**: Search for similar feature requests
2. **Check roadmap**: Look for planned features
3. **Consider scope**: Ensure the feature fits the project's goals

### Feature Request Template

```markdown
## Feature Description
Brief description of the feature you'd like to see.

## Use Case
Explain why this feature would be useful and how you would use it.

## Proposed Implementation
If you have ideas on how to implement this, share them.

## Alternatives Considered
What alternatives have you considered?

## Additional Information
Any other context or examples.
```

## Questions and Discussions

### Getting Help

- **GitHub Discussions**: Use the Discussions tab for questions
- **GitHub Issues**: Use issues for bugs and feature requests
- **Code Review**: Ask questions in PR reviews

### Contributing to Discussions

- **Be respectful** and constructive
- **Provide context** when asking questions
- **Help others** when you can
- **Stay on topic** and relevant to the project

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):

- **Major version** (X.0.0): Breaking changes
- **Minor version** (0.X.0): New features, backward compatible
- **Patch version** (0.0.X): Bug fixes, backward compatible

### Release Process

1. **Automatic releases** based on commit messages
2. **Manual review** of release notes
3. **GitHub release** creation
4. **PyPI publication** (if configured)

## Recognition

Contributors will be recognized in:

- **README.md**: List of contributors
- **Release notes**: Credit for significant contributions
- **GitHub contributors**: Automatic recognition

## Getting Help

If you need help with contributing:

1. **Check this document** first
2. **Search existing issues** and discussions
3. **Ask in GitHub Discussions**
4. **Contact maintainers** for complex questions

## Thank You

Thank you for contributing to FIT Detector Toolkit! Your contributions help make this project better for everyone in the detector analysis community.

---

*This document is based on best practices from the open-source community and adapted for the specific needs of FIT Detector Toolkit.*
