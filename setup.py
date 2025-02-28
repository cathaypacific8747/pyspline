# NOTE: the meson build system will not use this file.
# This file is kept here for compatibility with the legacy system:
# - setup `config/config.mk`
# - run `make`
# - instead of `pip install .` do `pip3 install setuptools` and `python3 setup.py install`.

import os
import re

from setuptools import setup

__version__ = re.findall(
    r"""__version__ = ["']+([0-9\.]*)["']+""",
    open("pyspline/__init__.py").read(),
)[0]

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open("doc/requirements.txt") as f:
    docs_require = f.read().splitlines()

setup(
    name="pyspline",
    version=__version__,
    description="pySpline is a package containing code for working with b-spline curve, surface, and volume objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="spline b-spline optimization",
    author="",
    author_email="",
    url="https://github.com/mdolab/pyspline",
    license="Apache License Version 2.0",
    packages=["pyspline"],
    package_data={"pyspline": ["*.so"]},
    install_requires=["numpy>=1.21", "scipy>=1.7"],
    extras_require={
        "docs": docs_require,
        "testing": ["parameterized", "testflo>=1.4.5", "mdolab-baseclasses>=1.6.1"],
    },
    classifiers=["Operating System :: Linux", "Programming Language :: Python, Fortran"],
)
