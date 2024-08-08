"""
Includes implementations for a few graph importers.
"""

from typing import Dict, List, Tuple

from .interfaces import GraphImporterInterface

from importlib import import_module

import datetime


def _try_import(moduleName: str, graphTypeName: str = 'Graph'):
    try:
        module = import_module(moduleName)
        try:
            return module.__getattribute__(graphTypeName)
        except AttributeError:
            return None
    except ImportError:
        return None


def _try_import_module(moduleName: str):
    try:
        return import_module(moduleName)
    except ImportError:
        return None


class GraphToolsGraphImporter(GraphImporterInterface):
    """Class for importing graphs from the [graph tool](https://graph-tool.skewed.de/) package.

    Notes
    -----
    Graph properties are ignored.
    Nodes and edges are identified by index.
    Node and edge properties are extracted from corresponding property maps.
    Default values for unset properties are used, due to the way graph tool properties work.
    """

    def __init__(self) -> None:
        super().__init__(_try_import('graph_tool'))

    @staticmethod
    def _collect_nodes(vertex_sequence, keys):
        nodes = []
        for i, vertex_and_properties in enumerate(vertex_sequence):
            if keys:
                vertex, *properties = vertex_and_properties
            else:
                vertex, properties = vertex_and_properties, []
            properties = {k: p for k, p in zip(keys, properties)}
            nodes.append(dict(
                id=i,
                properties=properties
            ))
        return nodes

    @staticmethod
    def _collect_edges(edge_sequence, keys):
        edges = []
        for i, edge_and_properties in enumerate(edge_sequence):
            if keys:
                vertex_source, vertex_target, *properties = edge_and_properties
            else:
                (vertex_source, vertex_target), properties = edge_and_properties, []
            properties = {k: p for k, p in zip(keys, properties)}
            edges.append(dict(
                id=i,
                start=vertex_source,
                end=vertex_target,
                properties=properties
            ))
        return edges

    def _import(self, graph) -> Tuple[List[Dict], List[Dict], bool]:
        nodes = self._collect_nodes(
            graph.iter_vertices(
                [getattr(graph.vertex_properties, key) for key in graph.vertex_properties.keys()]
            ),
            list(graph.vertex_properties.keys())
        )
        edges = self._collect_edges(
            graph.iter_edges(
                [getattr(graph.edge_properties, key) for key in graph.edge_properties.keys()]
            ),
            list(graph.edge_properties.keys())
        )
        return nodes, edges, graph.is_directed(), 'graph_tool'


class Neo4jGraphImporter(GraphImporterInterface):
    """Class for importing graphs from the [neo4j](https://github.com/neo4j/neo4j-python-driver) package.

    Notes
    -----
    Graph properties are ignored.
    Nodes and edges are identified by index.
    Node and edge properties are extracted from corresponding property maps.
    Default values for unset properties are used, due to the way graph tool properties work.
    """

    def __init__(self) -> None:
        super().__init__(None)

    def isInstance(self, graph):
        neograph = _try_import('neo4j', 'graph')
        if neograph is not None:
            return isinstance(graph, neograph.Graph)
        else:
            return False

    # neo4j datetime cannot be serialized automatically, so syncing it in the traitlet would fail
    def _sanitizeNeo4jDateTime(self, kv):
        key = kv[0]
        value = kv[1]

        neotime = _try_import('neo4j', 'time')
        neospatial = _try_import('neo4j', 'spatial')

        if neotime is not None:
            if neotime.Date is not None and isinstance(value, neotime.Date):
                # neo4j date has no timezone as it just helds the year, day, month
                value = datetime.datetime(value.year, value.month, value.day, tzinfo=datetime.timezone.utc)
                
            if neotime.DateTime is not None and isinstance(value, neotime.DateTime):
                value = datetime.datetime(value.year, value.month, value.day,
                                    value.hour, value.minute, int(value.second),
                                    int(value.second * 1000000 % 1000000),
                                    tzinfo=value.tzinfo)
                
        if neospatial is not None:
            if neospatial.Point is not None and isinstance(value, neospatial.Point):
                value = {"x": value[0], "y": value[1], "z": value[2] if len(value) > 2 else 0}

        return key, value

    def _import(self, graph) -> Tuple[List[Dict], List[Dict], bool]:
        nodes = list(map(lambda neoNode: (
            {"id": neoNode.id, "properties": {**dict(map(self._sanitizeNeo4jDateTime, neoNode.items())), "label": ":".join(neoNode.labels)}}),
                         graph.nodes))

        edges = list(map(lambda relationship: (
            {"id": relationship.id, "start": relationship.start_node.id, "end": relationship.end_node.id,
             "properties": {**dict(map(self._sanitizeNeo4jDateTime, relationship.items())), "label": relationship.type}}), graph.relationships))

        return nodes, edges, True, 'neo4j'


class IGraphGraphImporter(GraphImporterInterface):
    """Class for importing graphs from the [igraph](https://igraph.org/python/) package.

    Notes
    -----
    Nodes and edges are identified by index attribute.
    Node and edge properties are provided through attributes method.
    Edges are determined by source and target attribute.
    """

    def __init__(self) -> None:
        super().__init__(_try_import('igraph'))

    @staticmethod
    def _collect_nodes(vertex_sequence):
        nodes = []
        for x in vertex_sequence:
            nodes.append(dict(
                id=x.index,
                properties=x.attributes()
            ))
        return nodes

    @staticmethod
    def _collect_edges(edge_sequence):
        edges = []
        for y in edge_sequence:
            edges.append(dict(
                id=y.index,
                start=y.source,
                end=y.target,
                properties=y.attributes()
            ))
        return edges

    def _import(self, graph) -> Tuple[List[Dict], List[Dict], bool]:
        nodes = self._collect_nodes(graph.vs)
        edges = self._collect_edges(graph.es)
        return nodes, edges, graph.is_directed(), 'igraph'


def _set_label_attr(index: int, value: str, attr: Dict):
    """helper function for determining label attribute value"""
    key = 'label'
    if key in attr.keys():
        key = 'yf_' + key
    attr[key] = value if value else str(index)


class NetworkxGraphImporter(GraphImporterInterface):
    """Class for importing graphs from the [networkx](https://networkx.org/) package.

    Notes
    -----
    Graph attributes are ignored.
    Node identifiers are saved under property key *label* (or *yf_label* if key *label* already exists).
    Node identifiers have to be unique.
    Subgraphs (graph as node, see [here](https://networkx.org/documentation/stable/tutorial.html#using-the-graph-constructors)) are not supported.
    """

    def __init__(self) -> None:
        super().__init__(_try_import('networkx'))

    def _import(self, graph) -> Tuple[List[Dict], List[Dict], bool]:
        from networkx import DiGraph as NXDiGraph, MultiDiGraph as NXMultiDiGraph

        # does not contain node data
        # from networkx import to_dict_of_dicts
        # dict_of_dicts = to_dict_of_dicts(nx_graph)

        working_graph = graph.copy()

        directed = isinstance(working_graph, (NXDiGraph, NXMultiDiGraph))
        nodes = []
        node_name_to_id = {}
        for i, (node, attr) in enumerate(working_graph.nodes(data=True)):
            _set_label_attr(i, str(node), attr)
            _node = dict(id=i, properties=attr)
            nodes.append(_node)
            node_name_to_id[node] = i
        edges = []
        for j, (u, v, attr) in enumerate(working_graph.edges(data=True)):
            u_id = node_name_to_id[u]
            v_id = node_name_to_id[v]
            _edge = dict(id=j, start=u_id, end=v_id, properties=attr)
            edges.append(_edge)

        return nodes, edges, directed, 'networkx'


def pygraphviz_get_element_properties(index, element):
    """generic call of to_dict method of graph element attribute

    method is manual set if it is not available

    Parameters
    ----------
    index: int
    element: pygraphviz.Node | pygraphviz.Edge

    Returns
    -------
    attr_dict: dict

    """
    attr = element.attr.to_dict()
    _set_label_attr(index, element.name, attr)
    return attr


class PyGraphvizGraphImporter(GraphImporterInterface):
    """Class for importing graphs from the [pygraphviz](https://pygraphviz.github.io/) package.

    Notes
    -----
    Graph attributes are ignored.
    Node names are saved under property key *label* (or *yf_label* if key *label* already exists).
    Node names have to be unique.
    Unspecified default node/edge attributes are empty (and shown as null in data viewer).
    Subgraphs are dissolved.
    """

    def __init__(self) -> None:
        super().__init__(_try_import('pygraphviz', 'AGraph'))

    @staticmethod
    def _build_node(idx, node):
        properties = pygraphviz_get_element_properties(idx, node)
        return dict(
            id=idx,
            properties=properties
        )

    @staticmethod
    def _build_edge(idx, edge, node_name_to_id):
        start, end = edge
        properties = pygraphviz_get_element_properties(idx, edge)
        return dict(
            id=idx,
            start=node_name_to_id[start],
            end=node_name_to_id[end],
            properties=properties
        )

    def _import(self, graph) -> Tuple[List[Dict], List[Dict], bool]:
        nodes = []
        node_name_to_id = {}
        for i, n in enumerate(graph.nodes()):
            _node = self._build_node(i, n)
            nodes.append(_node)

            # otherwise no decoding of edge list possible
            assert n.name not in node_name_to_id, \
                'Non unique name {} for node with index {}, ' \
                'previously at index {}'.format(
                    n.name, i, node_name_to_id[n.name]
                )
            node_name_to_id[n.name] = i

        edges = []
        for j, edge in enumerate(graph.edges()):
            _edge = self._build_edge(j, edge, node_name_to_id)
            edges.append(_edge)

        return nodes, edges, graph.is_directed(), 'pygraphviz'


class PandasGraphImporter(GraphImporterInterface):
    """Class for importing graphs from the [pandas](https://pandas.pydata.org/) package.

    Notes
    -----
    Graph attributes are stored as additional node data.
    If there is no id, one is created equal to the column number (count start at 1)
    Node labels are supported

    e.g.
        data = {'source': ['1', '2', '3', '4'],
                'target': ['2', '3', '4', '2'],
                'label': ['1', '2', '3', '5']}
        df = pd.DataFrame(data)
        w.import_graph(df)
    """

    def __init__(self) -> None:
        super().__init__(None)

    def isInstance(self, graph):
        pandas = _try_import_module('pandas')
        if pandas is not None:

            return isinstance(graph, pandas.DataFrame)
        else:
            return False

    @staticmethod
    def get_or_create_node_id(node_name, node_name_to_id):
        if node_name is not None:
            if node_name not in node_name_to_id:
                node_id = len(node_name_to_id) + 1
                node_name_to_id[node_name] = node_id
            return node_name_to_id[node_name]
        return None

    def _import(self, graph) -> Tuple[List[Dict], List[Dict], bool]:
        edges = []
        nodes = []
        node_name_to_id = {}

        for i, row in graph.iterrows():
            node_id = row.get('id', None)
            if node_id is None:
                node_id = i + 1

            _prop = {}
            _node = {'id': node_id, 'properties': _prop}

            source_id = self.get_or_create_node_id(row.get('source', None), node_name_to_id)
            target_id = self.get_or_create_node_id(row.get('target', None), node_name_to_id)

            for attr in graph.columns:
                if attr not in ['source', 'target', 'id']:
                    if row.get(attr, None) is not None:
                        _prop[attr] = row[attr]

            _node['properties'] = _prop
            nodes.append(_node)

            if row.get('source', None) is not None and row.get('target', None) is not None:
                _edge = {'id': i, 'start': source_id, 'end': target_id}
                edges.append(_edge)

        directed = True

        return nodes, edges, directed, 'pandas'


