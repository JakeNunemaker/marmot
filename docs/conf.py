"""Documentation setup for Marmot."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2020, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


# -- Path setup --------------------------------------------------------------
import os
import sys

import marmot

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------
project = "Marmot"
copyright = "2020, Jake Nunemaker"
author = "Jake Nunemaker"
release = marmot.__version__


# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
]

master_doc = "contents"
autodoc_member_order = "bysource"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_theme_path = ["_themes"]
html_theme_options = {"display_version": True, "body_max_width": "70%"}

# Napoleon options
napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True
