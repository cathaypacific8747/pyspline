.. _pySpline_install:

Installation
============

Before you begin, ensure you have the following installed:

*   **Python 3.7 or later.**
*   **C and Fortran compilers.** ``gfortran`` or ``ifort`` are recommended
*   On Linux, Python header files (``python3-dev`` or similar) are required.

Install From Source
-------------------
First, create a virtual environment and activate it. Clone the repository, navigate to the root directory of ``pyspline`` and run:

.. prompt:: bash

    git clone https://github.com/mdolab/pyspline.git
    cd pyspline
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

Editable Installs
-----------------

To facilitate package development, the project can be installed in editable mode, allowing Python source files to be modified without needing to reinstall the package. However, note that by default, ``pip install --editable .`` creates a temporary isolated build environment and deletes it when the build is complete. This will cause further rebuilds to fail. 

.. tabs::

    .. tab:: pip
        It is recommended to first have the build dependencies available in your virtual environment, then install the package with build isolation disabled:

        .. prompt:: bash

            pip install meson-python meson ninja numpy
            pip install --no-build-isolation --editable .

        You can also inspect the compilation log during a rebuild by setting the `MESONPY_EDITABLE_VERBOSE <https://mesonbuild.com/meson-python/reference/environment-variables.html#envvar-MESONPY_EDITABLE_VERBOSE>`_ environment variable, or more permanently:

        .. prompt:: bash

            pip install --no-build-isolation --config-settings=editable-verbose=true --editable . 

    .. tab:: uv

        Add the following lines to your ``pyproject.toml`` :

        .. code-block:: toml
            :emphasize-lines: 5, 7-8, 11, 14

            [project]
            name = "my-project"
            version = "0.1.0"
            requires-python = ">=3.7"
            dependencies = ["pyspline"]

            [dependency-groups]
            dev = ["meson-python", "ninja", "numpy"]

            [tool.uv]
            no-build-isolation-package = ["pyspline"]

            [tool.uv.sources]
            pyspline = { path = "path/to/your/local/pyspline", editable = true }

        Run:

        .. code-block:: console

            $ uv sync --only-dev
            Using CPython 3.12.3 interpreter at: /usr/bin/python3
            Creating virtual environment at: .venv
            Resolved 20 packages in 3ms
            Prepared 6 packages in 230ms
            Installed 6 packages in 6ms
            + meson==1.7.0
            + meson-python==0.17.1
            + ninja==1.11.1.3
            + numpy==2.2.3
            + packaging==24.2
            + pyproject-metadata==0.9.0
            $ uv sync
            Resolved 20 packages in 6ms
                Built pyspline @ file:///path/to/your/local/pyspline
            Prepared 3 packages in 2.20s
            Installed 3 packages in 7ms
            + mdolab-baseclasses==1.8.2
            + pyspline==1.5.3 (from file:///path/to/your/local/pyspline)
            + scipy==1.15.2


Building with Make and setuptools
--------

While ``pip install .`` is the recommended method, the original build system based on Makefiles is still available. This section provides instructions for building pySpline using Makefiles, which may be helpful for advanced users or for troubleshooting purposes.


For speed purposes, pySpline uses a small compiled Fortran library for doing the time consuming computational operations.
It is therefore necessary to build this library before using pySpline.

pySpline follows the standard MDO Lab build procedure.
To start, create a virtual environment with ``numpy`` installed, and find a configuration file close to your current setup in::

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

    python3 setup_deprecated.py install
