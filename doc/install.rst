.. _pySpline_install:

Installation
============

Building
--------

Before you begin, ensure you have the following installed:

*   **Python 3.7 or later.**
*   **C and Fortran compilers.** ``gfortran`` or ``ifort`` are recommended
*   On Linux, Python header files (``python3-dev`` or similar) are required.

The easiest way to install pyspline is via ``pip``. First, create a virtual environment and activate it. After cloning the repository, navigate to the root directory of pySpline in your terminal and run:

.. prompt:: bash

    pip install .

This command will automatically handle the build process, including installing the Meson build system, compiling the necessary Fortran library and installing the Python package.

.. tip:: **Specifying Compilers**

   If you need to explicitly specify the C and Fortran compilers to use (e.g., to use Intel compilers like `ifort` and `icc`), you can do so by setting `certain environment variables <https://mesonbuild.com/Reference-tables.html#compiler-and-linker-selection-variables>`_ before running ``pip install .``. For example:

   .. prompt:: bash

       FC=$(which ifort) CC=$(which icc) pip install .

Verification
------------
pySpline contains a set of tests that can be run automatically to ensure it reproduces the expected reference results.
To do so, testing dependencies need to be installed first:

.. prompt:: bash

    pip install .[testing]

Once testing dependencies are installed, then to execute all tests, run the following in the root directory,

.. prompt:: bash

    testflo .


Building with Make and setuptools
--------

While ``pip install .`` is the recommended method, the original build system based on Makefiles is still available. This section provides instructions for building pySpline using Makefiles, which may be helpful for advanced users or for troubleshooting purposes.

For speed purposes, pySpline uses a small compiled Fortran library for doing the time consuming computational operations.
It is therefore necessary to build this library before using pySpline.

pySpline follows the standard MDO Lab build procedure.
To start, find a configuration file close to your current setup in::

    config/defaults

and copy it to ``config/config.mk``. For example:

.. prompt:: bash

    cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk

If you are a beginner user installing the packages on a linux desktop,
you should use the ``config.LINUX_GFORTRAN.mk`` versions of the configuration
files. The ``config.LINUX_INTEL.mk`` versions are usually used on clusters.
Once you have copied the config file, compile pySpline by running:

.. prompt:: bash

    make

If everything was successful, the following lines will be printed to
the screen (near the end)::

   Testing if module libspline can be imported...
   Module libspline was successfully imported.

If you don't see this, it will be necessary to configure the build manually.
To configure manually, open ``config/config.mk`` and modify options as necessary.

Lastly, to build and install the Python interface, type:

.. prompt:: bash

    python3 setup.py install
