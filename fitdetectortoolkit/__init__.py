"""
FITDetectorToolkit - A modular toolkit for detector analysis.

This package provides a unified interface for various detector analysis modules,
automatically managing dependencies from GitHub repositories.
"""

__version__ = "0.1.0"
__author__ = "Mateusz Polis"
__email__ = "mateusz.polis@cern.ch"

from .main import FITDetectorToolkit

__all__ = ["FITDetectorToolkit"]
