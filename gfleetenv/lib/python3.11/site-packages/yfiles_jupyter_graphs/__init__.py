#!/usr/bin/env python
# coding: utf-8
"""
On the top level the module only contains the necessary (and hidden)
functionality to be detected as a jupyter widget.
"""

from ._version import __version__
from .widget import GraphWidget


def _jupyter_labextension_paths():
    """Give info about lab extension paths.

    Called by Jupyter Lab Server to detect if it is a valid labextension and
    to install the widget.

    Returns
    -------
    src: Source directory name to copy files from. Webpack outputs generated files
        into this directory and Jupyter Lab copies from this directory during
        widget installation
    dest: Destination directory name to install widget files to. Jupyter Lab copies
        from `src` directory into <jupyter path>/labextensions/<dest> directory
        during widget installation
    """
    return [{
        'src': 'labextension',
        'dest': 'yfiles-jupyter-graphs',
    }]


def _jupyter_nbextension_paths():
    """Give info about notebook extension paths.

    Called by Jupyter Notebook Server to detect if it is a valid nbextension and
    to install the widget.

    Returns
    -------
    section: The section of the Jupyter Notebook Server to change.
        Must be 'notebook' for widget extensions
    src: Source directory name to copy files from. Webpack outputs generated files
        into this directory and Jupyter Notebook copies from this directory during
        widget installation
    dest: Destination directory name to install widget files to. Jupyter Notebook copies
        from `src` directory into <jupyter path>/nbextensions/<dest> directory
        during widget installation
    require: Path to importable AMD Javascript module inside the
        <jupyter path>/nbextensions/<dest> directory
    """
    return [{
        'section': 'notebook',
        'src': 'nbextension',
        'dest': 'yfiles-jupyter-graphs',
        'require': 'yfiles-jupyter-graphs/extension'
    }]
