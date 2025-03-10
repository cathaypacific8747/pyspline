#!/usr/bin/env python3
"""
This file contains the version of the pyspline package.

It serves three purposes:
- runtime: imported by `pyspline/__init__.py`.
- build time: standalone executable that writes the version string to stdout.
- build time: parsed with regex in `../setup_deprecated.py`

The Meson build system (`../meson.build`) runs this script to get the version
and provides it to `../pyproject.toml`.
"""

__version__ = "1.5.3"

if __name__ == "__main__":
    print(__version__)
