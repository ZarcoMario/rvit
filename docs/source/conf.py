# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import sphinx_py3doc_enhanced_theme


# -- Project information -----------------------------------------------------

project = 'rvit'
copyright = '2019, Matthew Egbert'
author = 'Matthew Egbert'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinxcontrib.fulltoc',
              'sphinx.ext.autosectionlabel',
              # 'sphinx.ext.autosummary',
              #'autodocsumm',
              'sphinx_automodapi.automodapi',

]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
#html_theme = 'bootstrap-astropy'
#html_theme = 'sphinxdoc'
html_theme = 'pyramid'

html_theme = "sphinx_py3doc_enhanced_theme"
html_theme_path = [sphinx_py3doc_enhanced_theme.get_html_theme_path()]



# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

css_mods = """
div.body code.descclassname { display: none }

div.related {
height: 0px;
margin: 0px;
padding:0px;
}

div.sphinxsidebar {
border-radius: 0px;
width:260px;
}

div.bodywrapper{
margin-left: 260px;
}


div.body {
    font-family: 'arial';
    padding-top: 1em;
}

dl.class {
padding: 0.8em;
background-color: #efefef;
border-radius: 5px;
}

div.body h2 {
background-color: #000;
color: #fff;
text-align: right;
}

"""

html_theme_options = {
    'appendcss': css_mods,
}


    
