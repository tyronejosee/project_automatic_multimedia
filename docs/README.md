# **Sphinx Documentation**

## **Verify that `sphinx` and `sphinx.ext.autodoc` are installed**

If you haven't done so, install Sphinx and its necessary extensions:

```bash
pip install sphinx sphinx-autobuild sphinx-rtd-theme
```

## **Configure `conf.py`**

Edit `docs/conf.py` and add the following:

```python
import os
import sys

# Add the project's root directory and 'core/' to the path so Sphinx can find the modules
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../core'))

# Sphinx extensions
extensions = [
    'sphinx.ext.autodoc',      # Automatically extracts docstrings
    'sphinx.ext.napoleon',     # Supports Google-style and NumPy docstrings
    'sphinx.ext.viewcode',     # Adds links to the source code
]

# Set the documentation theme
html_theme = 'sphinx_rtd_theme'

# Configuration for `autodoc`
autodoc_default_options = {
    'members': True,
    'undoc-members': True,  # Documents methods even without docstrings
    'show-inheritance': True
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
```

## **Generate `.rst` files from your code automatically**

Navigate to the `docs/` directory and run:

```bash
sphinx-apidoc -o source ../core
```

This will generate `.rst` files inside `docs/source/`, which will automatically document your code in `core/`.

## **Add the generated modules to `index.rst`**

Open `docs/source/index.rst` and ensure the generated modules are included.

```rst
.. tyronejosee-project_automatic_multimedia documentation master file

Welcome to the project documentation!
=====================================

Contents:

.. toctree::
   :maxdepth: 2
   :caption: Modules:

   core/index
```

If there are more submodules, add a line for each one in the `toctree`.

## **Build the documentation**

```bash
.\make html
```

This will generate the documentation in `_build/html/`.

## **Verify the documentation**

Open `_build/html/index.html` in your browser to view the automatically generated documentation.

## **Automate with `sphinx-autobuild` (Optional)**

If you want the documentation to regenerate automatically when changes are made:

```bash
sphinx-autobuild docs/_build/html
```

This will start a server and update the documentation live.
