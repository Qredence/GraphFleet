"""
Includes corresponding factories for the graph importers.
"""
from .importer import \
    GraphToolsGraphImporter, \
    IGraphGraphImporter, \
    NetworkxGraphImporter, \
    Neo4jGraphImporter, \
    PyGraphvizGraphImporter, \
    PandasGraphImporter
from .interfaces import \
    GraphImporterInterface


def _get_importer(graph) -> GraphImporterInterface:
    """function to select factory based on graph type"""
    importers = [GraphToolsGraphImporter(), IGraphGraphImporter(), NetworkxGraphImporter(), PyGraphvizGraphImporter(), Neo4jGraphImporter(), PandasGraphImporter()]

    for importer in importers:
        if importer.isInstance(graph):
            return importer

    raise NotImplementedError('Could not find a graph importer factory for type {}'.format(type(graph)))
