"""
Submodule for graph importer.
"""
from .factories import _get_importer

def import_(graph):
    """function that uses graph importer and calls it with provided graph"""
    return _get_importer(graph)(graph)
