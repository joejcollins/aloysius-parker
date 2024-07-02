"""Configuration file for the Sphinx documentation builder."""

# sourcery skip: avoid-global-variables
import os
import sys

sys.path.insert(0, os.path.abspath("../"))

# Project information
project = "Aloysius Parker"
copyright = "2024, Joe J Collins"
author = "j.collins"
release = "1"

# General configuration
extensions = ["sphinx.ext.autodoc", "sphinxcontrib.mermaid"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# Options for HTML output
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}
