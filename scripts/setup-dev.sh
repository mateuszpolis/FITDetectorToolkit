#!/bin/bash

# Setup script for FITDetectorToolkit development environment

set -e

echo "🚀 Setting up FITDetectorToolkit development environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi

# Install the package in development mode
echo "📦 Installing package in development mode..."
pip install -e .[dev]

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pre-commit install --hook-type pre-commit
pre-commit install --hook-type commit-msg

# Install Node.js dependencies for semantic-release
if command -v npm &> /dev/null; then
    echo "📦 Installing Node.js dependencies..."
    npm install
else
    echo "⚠️  npm not found. Node.js dependencies will be installed by GitHub Actions."
fi

# Run initial checks
echo "🔍 Running initial code quality checks..."
pre-commit run --all-files

echo "✅ Development environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Make your changes"
echo "2. Use conventional commit messages (e.g., 'feat: add new feature')"
echo "3. Commit your changes: git commit -m 'your message'"
echo "4. Push to trigger CI/CD: git push"
echo ""
echo "📚 Commit message format:"
echo "  feat: new feature"
echo "  fix: bug fix"
echo "  docs: documentation changes"
echo "  style: formatting changes"
echo "  refactor: code refactoring"
echo "  test: adding tests"
echo "  chore: maintenance tasks"
