#!/usr/bin/env python
# coding: utf-8
"""Jupyter (ipy)widget powered by yFiles.

The main GraphWidget class is defined in this module.

Notes
-----
To learn more about widget behaviour look at GraphWidget class directly.

Attributes
----------
NEIGHBORHOOD_TAB_ID: str
    Specify neighborhood tab id.
DATA_TAB_ID: str
    Specify data tab id.
SEARCH_TAB_ID: str
    Specify search tab id.
ABOUT_TAB_ID: str
    Specify about tab id.
CONTEXT_PANE_MAPPING: list
    Define the order and mapping to id and title of the context pane tabs.

    Each element is a dictionary with keys ("id", "title").
    By defining it on the python side of the widget
    it makes it possible (and easier) to check user input for correctness.
"""

from typing import Any, Dict as TDict, List as TList, Optional, Union
import inspect

from IPython.display import  display
from ipywidgets import DOMWidget, Layout
from traitlets import Unicode, List, Dict, Bool

from ._frontend import module_name, module_version
from .graph import import_
from .layout import layout_

NEIGHBORHOOD_TAB_ID = 'Neighborhood'
DATA_TAB_ID = 'Data'
SEARCH_TAB_ID = 'Search'
ABOUT_TAB_ID = 'About'
CONTEXT_PANE_MAPPING = [
    {'id': NEIGHBORHOOD_TAB_ID, 'title': NEIGHBORHOOD_TAB_ID},
    {'id': DATA_TAB_ID, 'title': DATA_TAB_ID},
    {'id': SEARCH_TAB_ID, 'title': SEARCH_TAB_ID},
    {'id': ABOUT_TAB_ID, 'title': ABOUT_TAB_ID}
]
SCALING_PER_NODE = 10
COLOR_PALETTE = ['#2196F3', '#4CAF50', '#F44336', '#607D8B', '#673AB7', '#CDDC39', '#9E9E9E', '#9C27B0']


class GraphWidget(DOMWidget):
    """The main widget class.

    Example
    -------
    .. code::

       from yfiles_jupyter_graphs import GraphWidget
       w = GraphWidget()
       w.show()

    See notebooks for more examples.

    Notes
    -----
    Nodes and edges properties should be constructed recursively with basic python types
    otherwise {de-}serializers will fail.

    """
    _model_name = Unicode('GraphModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('GraphView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    _nodes = List().tag(sync=True)
    _edges = List().tag(sync=True)
    _directed = Bool().tag(sync=True)
    _graph_layout = Dict().tag(sync=True)
    _highlight = List().tag(sync=True)
    _neighborhood = Dict().tag(sync=True)
    _sidebar = Dict().tag(sync=True)
    _context_pane_mapping = List().tag(sync=True)
    _overview = Dict().tag(sync=True)
    _data_importer = Unicode('unknown').tag(sync=True)
    _selected_graph = List().tag(sync=True)
    _license = Dict().tag(sync=True)

    # a mapping of node/edge types to a color, e.g. for neo4j where the item types are automatically mapped to
    # different colors
    _itemtype2colorIdx = {}

    def __init__(
            self,
            widget_layout: Optional[Layout] = None,
            overview_enabled: Optional[bool] = None,
            context_start_with: Optional[str] = '',
            graph: Optional = None,
            license: Optional[dict] = None
    ):
        """GraphWidget constructor.

        Parameters
        ----------
        widget_layout: ipywidgets.Layout, optional
            Can be used to specify general widget appearance through css attributes.
            See ipywidgets documentation for the available keywords.
        overview_enabled: bool, optional
            Enable graph overview component.
            Default behaviour depends on cell width.
        context_start_with: str, optional
            Specify context tab name to start with that tab opened.
            Default behaviour is open with About dialog.
            Use None to start with closed sidebar.
        graph: networkx.{Multi}{Di}Graph | graph_tool.Graph | igraph.Graph | pygraphviz.AGraph | pandas, optional
            Specify the graph to import. Same as calling 'import_graph' after construction
        """
        # the info above should be in class docstring according to official and numpydoc style guide
        # but https://youtrack.jetbrains.com/issue/PY-28900
        if widget_layout is None:
            widget_layout = Layout(height='500px', width='100%')
            self._widget_layout_set_manually = False
        else:
            self._widget_layout_set_manually = True
        super().__init__(layout=widget_layout)
        self._overview = dict(enabled=overview_enabled, overview_set=overview_enabled is not None)
        self._context_pane_mapping = CONTEXT_PANE_MAPPING
        self._sidebar = dict(enabled=context_start_with is not None, start_with=context_start_with)
        if graph is not None:
            self.import_graph(graph)
        if license is not None:
            self._license = license



    def get_nodes(self):
        """Getter for the nodes traitlets property.

        Notes
        -----
        This function acts as an alias for using GraphWidget.nodes property
        e.g. w.nodes == w.get_nodes().

        Returns
        -------
        nodes: typing.List[typing.Dict]
            Each node has the keys id: int and properties: typing.Dict.
            It might include keys that are not set directly,
            see (default) node mappings for details.

        """
        return self._nodes

    def set_nodes(self, nodes):
        """Setter for the nodes traitlets property.

        Parameters
        ----------
        nodes: typing.List[typing.Dict]
            Each node should have the keys id: int and properties: typing.Dict.
            Properties should be constructed recursively with basic python types,
            otherwise {de-}serializers will fail.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           w.set_nodes([
                {'id': 0, 'properties': {'label': 'Hello World'}},
                {'id': 1, 'properties': {'label': 'This is a second node.'}}
           ])

        Notes
        -----
        This function acts as an alias for using GraphWidget.nodes property
        e.g. w.nodes = [{...}] has the same effect as using w.set_nodes([{...}]).

        Returns
        -------

        """
        self._nodes = nodes

    nodes = property(get_nodes, set_nodes)

    def get_edges(self):
        """Getter for the edges traitlets property.

        Notes
        -----
        This function acts as an alias for using GraphWidget.edges property
        e.g. w.edges == w.get_edges() is true.

        Returns
        -------
        edges: typing.List[typing.Dict]
            Each edge has the keys id: int, start: int, end: int and properties: typing.Dict.
            It might include keys that are not set directly,
            see (default) edge mappings for details.

        """
        return self._edges

    def set_edges(self, edges):
        """Setter for the edges traitlets property.

        Parameters
        ----------
        edges: typing.List[typing.Dict]
            Each edge should have the keys id: int, start: int, end:int
            and properties: typing.Dict.
            Ids for start and end should be among used node ids,
            otherwise the edge does not appear.
            Properties should be constructed recursively with basic python types,
            otherwise {de-}serializers will fail.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           w.set_edges([
               {'id': 0, 'start': 0, 'end': 1, 'properties': {'label': 'edge between first and second node'}}
           ])

        Notes
        -----
        This function acts as an alias for using GraphWidget.edges property
        e.g. w.edges = [{...}] has the same effect as using w.set_edges([{...}]).

        Returns
        -------

        """
        self._edges = edges

    edges = property(get_edges, set_edges)

    def get_directed(self):
        """Getter for the directed traitlets property.

        Notes
        -----
        This function acts as an alias for using GraphWidget.directed property
        e.g. w.directed == w.get_directed() is true.

        Returns
        -------
        directed: bool
            Whether the graph is interpreted as directed.

        """
        return self._directed

    def set_directed(self, directed):
        """Setter for the directed traitlets property.

        Parameters
        ----------
        directed: bool
            Whether the graph is interpreted as directed.

        Notes
        -----
        This function acts as an alias for using GraphWidget.directed property
        e.g. w.directed = x has the same effect as using w.set_directed(x).

        Returns
        -------

        """
        self._directed = directed

    directed = property(get_directed, set_directed)

    def get_heat_mapping(self):
        """Getter for the heat mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_heat_mapping` is returned.

        Returns
        -------
        heat_mapping: callable | str
            A function that produces heat values or the name of the property to use for the heat binding.

        """
        return self._get_attribute_by_name('_heat_mapping', 'default')

    def set_heat_mapping(self, heat_mapping):
        """Setter for the heat mapping property.

        Parameters
        ----------
        heat_mapping: callable | str
            A function that produces heat values or the name of the property to use for the heat binding.
            The function should have the same signature as `default_heat_mapping`
            e.g. take in a dictionary and return a number.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_heat_mapping(node: dict):
           ...
           w.set_heat_mapping(custom_heat_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._heat_mapping = heat_mapping

    def del_heat_mapping(self):
        """Deleter for the heat mapping property.

        Remove a custom heat mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_heat_mapping')

    def get_node_label_mapping(self):
        """Getter for the node label mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_node_label_mapping` is returned.

        Returns
        -------
        node_label_mapping: callable | str
            A function that produces node labels or the name of the property to use for the label binding.

        """
        return self._get_attribute_by_name('_node_label_mapping', 'default')

    def set_node_label_mapping(self, node_label_mapping):
        """Setter for the node label mapping property.

        Parameters
        ----------
        node_label_mapping: callable | str
            A function that produces node labels or the name of the property to use for the label binding.
            The function should have the same signature as `default_node_label_mapping`
            e.g. take in a node dictionary and return a string.

        Example
        -------

        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           w.node_label_mapping = 'id'

        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_label_mapping(node: dict):
           ...
           w.set_node_label_mapping(custom_node_label_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._node_label_mapping = node_label_mapping

    def del_node_label_mapping(self):
        """Deleter for the node label mapping property.

        Remove a custom node label mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_node_label_mapping')

    node_label_mapping = property(get_node_label_mapping, set_node_label_mapping, del_node_label_mapping)

    def get_edge_label_mapping(self):
        """Getter for the edge label mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_edge_label_mapping` is returned.

        Returns
        -------
        edge_label_mapping: callable | str
            A function that produces edge labels or the name of the property to use for the label binding.

        """
        return self._get_attribute_by_name('_edge_label_mapping', 'default')

    def set_edge_label_mapping(self, edge_label_mapping):
        """Setter for the edge label mapping property.

        Parameters
        ----------
        edge_label_mapping: callable | str
            A function that produces edge labels or the name of the property to use for the label binding.
            The function should have the same signature as `default_edge_label_mapping`
            e.g. take in an edge dictionary and return a string.

        Example
        -------

        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           w.edge_label_mapping = 'id'

        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_edge_label_mapping(node: dict):
           ...
           w.set_edge_label_mapping(custom_edge_label_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._edge_label_mapping = edge_label_mapping

    def del_edge_label_mapping(self):
        """Deleter for the edge label mapping property.

        Remove a custom edge label mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_edge_label_mapping')

    edge_label_mapping = property(get_edge_label_mapping, set_edge_label_mapping, del_node_label_mapping)

    def get_node_property_mapping(self):
        """Getter for the node property mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_node_property_mapping` is returned.

        Returns
        -------
        node_property_mapping: callable | str
            A function that produces node properties or the name of the property to use for the property binding.

        """
        return self._get_attribute_by_name('_node_property_mapping', 'default')

    def set_node_property_mapping(self, node_property_mapping):
        """Setter for the node property mapping property.

        Parameters
        ----------
        node_property_mapping: callable | str
            A function that produces node properties or the name of the property to use for the property binding.
            The function should have the same signature as `default_node_property_mapping`
            e.g. take in a node dictionary and return a dictionary.

        Notes
        -----
        Properties are changed inplace by this mapping.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_property_mapping(node: dict):
           ...
           w.set_node_property_mapping(custom_node_property_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._node_property_mapping = node_property_mapping

    def del_node_property_mapping(self):
        """Deleter for the node property mapping property.

        Remove a custom node property mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_node_property_mapping')

    node_property_mapping = property(get_node_property_mapping, set_node_property_mapping, del_node_property_mapping)

    def get_edge_property_mapping(self):
        """Getter for the edge property mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_edge_property_mapping` is returned.

        Returns
        -------
        edge_property_mapping: callable | str
            A function that produces edge properties or the name of the property to use for the property binding.

        """
        return self._get_attribute_by_name('_edge_property_mapping', 'default')

    def set_edge_property_mapping(self, edge_property_mapping):
        """Setter for the edge property mapping property.

        Parameters
        ----------
        edge_property_mapping: callable | str
            A function that produces edge properties or the name of the property to use for the property binding.
            The funtion should have the same signature as `default_edge_property_mapping`
            e.g. take in an edge dictionary and return a dictionary.

        Notes
        -----
        Properties are changed inplace by this mapping.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_edge_property_mapping(node: dict):
           ...
           w.set_edge_property_mapping(custom_edge_property_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._edge_property_mapping = edge_property_mapping

    def del_edge_property_mapping(self):
        """Deleter for the edge property mapping property.

        Remove a custom edge property mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_edge_property_mapping')

    edge_property_mapping = property(get_edge_property_mapping, set_edge_property_mapping, del_edge_property_mapping)

    def get_node_color_mapping(self):
        """Getter for the node color mapping mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_node_color_mapping` is returned.

        Returns
        -------
        node_color_mapping: callable | str
            A function that produces node colors or the name of the property to use for the color binding.

        """
        return self._get_attribute_by_name('_node_color_mapping', 'default')

    def set_node_color_mapping(self, node_color_mapping):
        """Setter for the node color mapping mapping property.

        Parameters
        ----------
        node_color_mapping: callable | str
            A function that produces node colors or the name of the property to use for the color binding.
            The function should have the same signature as `default_node_color_mapping`
            e.g. take in a node dictionary and return a string.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_color_mapping(node: dict):
           ...
           w.set_node_color_mapping(custom_node_color_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._node_color_mapping = node_color_mapping

    def del_node_color_mapping(self):
        """Deleter for the node color mapping mapping property.

        Remove a custom node color mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_node_color_mapping')

    node_color_mapping = property(get_node_color_mapping, set_node_color_mapping, del_node_color_mapping)

    def get_edge_color_mapping(self):
        """Getter for the edge color mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_edge_color_mapping` is returned.

        Returns
        -------
        edge_color_mapping: callable | str
            A function that produces edge colors or the name of the property to use for the color binding.

        """
        return self._get_attribute_by_name('_edge_color_mapping', 'default')

    def set_edge_color_mapping(self, edge_color_mapping):
        """Setter for the edge color mapping property.

        Parameters
        ----------
        edge_color_mapping: callable | str
            A function that produces edge colors or the name of the property to use for the color binding.
            The function should have the same signature as `default_edge_color_mapping`
            e.g. take in an edge dictionary and return a string.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_edge_color_mapping(node: dict):
           ...
           w.set_edge_color_mapping(custom_edge_color_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._edge_color_mapping = edge_color_mapping

    def del_edge_color_mapping(self):
        """Deleter for the edge color mapping property.

        Remove a custom edge color mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_edge_color_mapping')

    edge_color_mapping = property(get_edge_color_mapping, set_edge_color_mapping, del_edge_color_mapping)

    def get_node_styles_mapping(self):
        """Getter for the node styles mapping mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_node_styles_mapping` is returned.

        Returns
        -------
        node_styles_mapping: callable | str
            A function that produces node styles or the name of the property to use for the style object binding.

        """
        return self._get_attribute_by_name('_node_styles_mapping', 'default')

    def set_node_styles_mapping(self, node_styles_mapping):
        """Setter for the node styles mapping mapping property.

        Parameters
        ----------
        node_styles_mapping: callable | str
            A function that produces node styles or the name of the property to use for the style object binding.
            The function should have the same signature as `default_node_styles_mapping`
            e.g. take in a node dictionary and return a typing.Dict.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_styles_mapping(node: dict):
           ...
           w.set_node_styles_mapping(custom_node_styles_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._node_styles_mapping = node_styles_mapping

    def del_node_styles_mapping(self):
        """Deleter for the node styles mapping mapping property.

        Remove a custom node styles mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_node_styles_mapping')

    node_styles_mapping = property(get_node_styles_mapping, set_node_styles_mapping, del_node_styles_mapping)

    def get_node_scale_factor_mapping(self):
        """Getter for the node scale factor mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_node_scale_factor_mapping` is returned.

        Returns
        -------
        node_scale_factor_mapping: callable | str
            A function that produces node scale factor or the name of the property to use for the scale binding.

        """
        return self._get_attribute_by_name('_node_scale_factor_mapping', 'default')

    def set_node_scale_factor_mapping(self, node_scale_factor_mapping):
        """Setter for the node scale factor mapping property.

        Parameters
        ----------
        node_scale_factor_mapping: callable | str
            A function that produces node scale factors or the name of the property to use for the scale binding.
            The function should have the same signature as `default_node_scale_factor_mapping`
            e.g. take in a node dictionary and return a positive float.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_scale_factor_mapping(node: dict):
           ...
           w.set_node_scale_factor_mapping(custom_node_scale_factor_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._node_scale_factor_mapping = node_scale_factor_mapping

    def del_node_scale_factor_mapping(self):
        """Deleter for the node scale factor mapping property.

        Remove a custom node scale factor mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_node_scale_factor_mapping')

    node_scale_factor_mapping = property(get_node_scale_factor_mapping, set_node_scale_factor_mapping,
                                         del_node_scale_factor_mapping)

    def get_node_size_mapping(self):
        """Getter for the node size mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_node_size_mapping` is returned.


        Returns
        -------
        node_size_mapping: callable | str
            A function that produces node size or the name of the property to use for the size binding.

        """
        return self._get_attribute_by_name('_node_size_mapping', 'default')

    def set_node_size_mapping(self, node_size_mapping):
        """Setter for the node size mapping property.

        Parameters
        ----------
        node_size_mapping: callable | str
            A function that produces node sizes or the name of the property to use for the size binding.
            The function should have the same signature as `default_node_size_mapping`
            e.g. take in an index and node dictionary and return a positive number.


        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._node_size_mapping = node_size_mapping

    def del_node_size_mapping(self):
        """Deleter for the node size mapping property.

        Remove a custom node size mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_node_size_mapping')

    node_size_mapping = property(get_node_size_mapping, set_node_size_mapping, del_node_size_mapping)

    def get_node_layout_mapping(self):
        """Getter for the node layout mapping property.

                Notes
                -----
                If no mapping is explicitly set, `default_node_layout_mapping` is returned.

                Returns
                -------
                node_layout_mapping: callable | str
                    A function that produces node layouts or the name of the property to use for the node layout

        """

        return self._get_attribute_by_name('_node_layout_mapping', 'default')

    def set_node_layout_mapping(self, node_layout_mapping):
        """Setter for the node layout mapping property.

        Parameters
        ----------
        node_layout_mapping: callable | str
            A function that produces node layouts or the name of the property to use for the layout binding.
            The function should have the same signature as `default_node_layout_mapping`
            e.g. take in an index and node dictionary and return a positive float 4-tuple.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_layout_mapping(node: dict):
           ...
           w.set_node_layout_mapping(custom_node_layout_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._node_layout_mapping = node_layout_mapping

    def del_node_layout_mapping(self):
        """Deleter for the node layout mapping property.

        Remove a custom node layout mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_node_layout_mapping')

    node_layout_mapping = property(get_node_layout_mapping, set_node_layout_mapping,
                                   del_node_layout_mapping)
    def get_edge_thickness_factor_mapping(self):
        """Getter for the edge thickness factor mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_edge_thickness_factor_mapping` is returned.

        Returns
        -------
        edge_thickness_factor_mapping: callable | str
            A function that produces edge thickness factors or the name of the property to use for the thickness binding.

        """
        return self._get_attribute_by_name('_edge_thickness_factor_mapping', 'default')

    def set_edge_thickness_factor_mapping(self, edge_thickness_factor_mapping):
        """Setter for the edge thickness factor mapping property.

        Parameters
        ----------
        edge_thickness_factor_mapping: callable | str
            A function that produces edge thickness factors or the name of the property to use for the thickness binding.
            The function should have the same signature as `default_edge_thickness_factor_mapping`
            e.g. take in an edge dictionary and return a positive float.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_edge_thickness_factor_mapping(node: dict):
           ...
           w.set_edge_thickness_factor_mapping(custom_edge_thickness_factor_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._edge_thickness_factor_mapping = edge_thickness_factor_mapping

    def del_edge_thickness_factor_mapping(self):
        """Deleter for the edge thickness factor mapping property.

        Remove a custom edge thickness factor mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_edge_thickness_factor_mapping')

    edge_thickness_factor_mapping = property(get_edge_thickness_factor_mapping, set_edge_thickness_factor_mapping,
                                             del_edge_thickness_factor_mapping)

    def get_node_type_mapping(self):
        """Getter for the node type mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_node_type_mapping` is returned.

        Returns
        -------
        node_type_mapping: callable | str
            A function that produces node types or the name of the property to use for the type binding.

        """
        return self._get_attribute_by_name('_node_type_mapping', 'default')

    def set_node_type_mapping(self, node_type_mapping):
        """Setter for the node type mapping property.

        Parameters
        ----------
        node_type_mapping: callable | str
            A function that produces node types or the name of the property to use for the type binding.
            The function should have the same signature as `default_node_type_mapping`
            e.g. take in a node dictionary and return a bool/int/float or str value.

        Notes
        -----
        Node types give more information for some layout algorithms.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_type_mapping(node: dict):
           ...
           w.set_node_type_mapping(custom_node_type_mapping)

        References
        ----------
        Layout with Custom Node Types <https://docs.yworks.com/yfileshtml/#/dguide/layout-summary#node_types>

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._node_type_mapping = node_type_mapping

    def del_node_type_mapping(self):
        """Deleter for the node type mapping property.

        Remove a custom node type mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_node_type_mapping')

    node_type_mapping = property(get_node_type_mapping, set_node_type_mapping, del_node_type_mapping)
    def get_node_parent_mapping(self):
        """Getter for the node parent mapping property to create a nested graph hierarchy.

        Notes
        -----
        If no mapping is explicitly set, `default_node_parent_mapping` is returned.

        Returns
        -------
        node_parent_mapping: callable | str
            A function that produces node parent IDs or the name of the property to use for the parent binding.

        """
        return self._get_attribute_by_name('_node_parent_mapping', 'default')

    def set_node_parent_mapping(self, node_parent_mapping):
        """Setter for the node parent mapping property.

        Parameters
        ----------
        node_parent_mapping: callable | str
            A function that produces node parent IDs or the name of the property to use for the parent binding.
            The function should have the same signature as `default_node_parent_mapping`
            e.g. take in a node dictionary and return a str or `None` value.
            It is expected that the returned value corresponds to the ID of another node (see `nodes`). This parent node
            is then created as a group node that groups the corresponding child nodes.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_parent_mapping(node: dict):
           ...
           w.set_node_parent_mapping(custom_node_parent_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._node_parent_mapping = node_parent_mapping

    def del_node_parent_mapping(self):
        """Deleter for the node parent mapping property.

        Remove a custom node parent mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_node_parent_mapping')

    node_parent_mapping = property(get_node_parent_mapping, set_node_parent_mapping, del_node_parent_mapping)

    def get_node_position_mapping(self):
        """Getter for the node position mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_node_position_mapping` is returned.

        Returns
        -------
        node_position_mapping: callable | str
            A function that produces node positions or the name of the property to use for position binding.

        """
        return self._get_attribute_by_name('_node_position_mapping', 'default')

    def set_node_position_mapping(self, node_position_mapping):
        """Setter for the node position mapping property.

        Parameters
        ----------
        node_position_mapping: callable | str
            A function that produces node positions or the name of the property to use for the position binding.
            The function should have the same signature as `default_node_position_mapping`
            e.g. take in a node dictionary and return a float 2-tuple.

        Notes
        -----
        Only edge router algorithms consider node positions,
        all other algorithms calculate node positions themselves.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_position_mapping(node: dict):
           ...
           w.set_node_position_mapping(custom_node_position_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._node_position_mapping = node_position_mapping

    def del_node_position_mapping(self):
        """Deleter for the node position mapping property.

        Remove a custom node position mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_node_position_mapping')

    node_position_mapping = property(get_node_position_mapping, set_node_position_mapping, del_node_position_mapping)

    def get_node_coordinate_mapping(self):
        """Getter for the node coordinate mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_node_coordinate_mapping` is returned.

        Returns
        -------
        node_coordinate_mapping: callable | str
            A function that produces node coordinates or the name of the property to use for coordinate binding.

        """
        return self._get_attribute_by_name('_node_coordinate_mapping', 'default')

    def set_node_coordinate_mapping(self, node_coordinate_mapping):
        """Setter for the node coordinate mapping property.

        Parameters
        ----------
        node_coordinate_mapping: callable | str
            A function that produces node coordinates or the name of the property to use for the coordinate binding.
            The function should have the same signature as `default_node_coordinate_mapping`
            e.g. take in a node dictionary and return a float 2-tuple.

        Notes
        -----
        Only edge router algorithms consider node coordinates,
        all other algorithms calculate node coordinates themselves.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_coordinate_mapping(node: dict):
           ...
           w.set_node_coordinate_mapping(custom_node_coordinate_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._node_coordinate_mapping = node_coordinate_mapping

    def del_node_coordinate_mapping(self):
        """Deleter for the node coordinate mapping property.

        Remove a custom node coordinate mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_node_coordinate_mapping')

    node_coordinate_mapping = property(get_node_coordinate_mapping, set_node_coordinate_mapping, del_node_coordinate_mapping)

    def set_node_label_style_mapping(self, node_label_style_mapping):
        # noinspection PyAttributeOutsideInit
        self._node_label_style_mapping = node_label_style_mapping

    def get_node_label_style_mapping(self):
        return self._get_attribute_by_name('_node_label_style_mapping', 'default')

    def del_node_label_style_mapping(self):
        self.__safe_delete_mapping('_node_label_style_mapping')

    def get_directed_mapping(self):
        """Getter for the edge direction mapping property.

        Notes
        -----
        If no mapping is explicitly set, `default_directed_mapping` is returned.

        Returns
        -------
        directed_mapping: callable | str
            A function that produces edge directions or the name of the property to use for the direction binding.

        """
        return self._get_attribute_by_name('_directed_mapping', 'default')

    def set_directed_mapping(self, directed_mapping):
        """Setter for the edge direction mapping property.

        Parameters
        ----------
        directed_mapping: callable | str
            A function that produces edge directions or the name of the property to use for the direction binding.
            The function should have the same signature as `default_directed_mapping`
            e.g. take in an edge dictionary and return a boolean value.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_directed_mapping(node: dict):
           ...
           w.set_directed_mapping(custom_directed_mapping)

        Returns
        -------

        """
        # noinspection PyAttributeOutsideInit
        self._directed_mapping = directed_mapping

    def del_directed_mapping(self):
        """Deleter for the edge direction mapping property.

        Remove a custom directed mapping.

        Returns
        -------

        """
        self.__safe_delete_mapping('_directed_mapping')

    directed_mapping = property(get_directed_mapping, set_directed_mapping, del_directed_mapping)

    def __safe_delete_mapping(self, mapping):
        """Deleter for mapping properties.

        Ensures save deletion.

        Returns
        -------

        """
        if hasattr(self, mapping):
            delattr(self, mapping)

    @staticmethod
    def default_element_label_mapping(index: int, element: TDict):
        """The default label mapping for graph elements.

        Element (dict) should have key properties which itself should be a dict.
        Then one of the following values (in descending priority) is used as label if the label is a string:

        - properties["label"]
        - properties["yf_label"]

        If a label styling is given the following is used as a label:

        - label["text"]

        Parameters
        ----------
        index: int (optional)
        element: typing.Dict

        Notes
        -----
        This is the default value for the {`node|edge`}_label_mapping property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        When a string is provided as the function argument, the key will be searched for in both the properties
        dictionary and the element keys.

        Example
        -------

        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           w.{node|edge}_label_mapping = 'id'

        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_element_label_mapping(element: typing.Dict):
           ...
           w.set_{node|edge}_label_mapping(custom_element_label_mapping)

        Returns
        -------
        label: str

        """
        properties = element.get('properties', {})
        return str(properties.get('label', properties.get('yf_label', '')))

    @staticmethod
    def default_node_label_mapping(index: int, node: TDict):
        """See default element label mapping."""
        return GraphWidget.default_element_label_mapping(index, node)

    @staticmethod
    def default_edge_label_mapping(index: int, edge: TDict):
        """See default element label mapping."""
        return GraphWidget.default_element_label_mapping(index, edge)

    # noinspection PyUnusedLocal
    @staticmethod
    def default_element_property_mapping(index: int, element: TDict):
        """The default property mapping for graph elements.

        Simply selects the properties value of element dictionary.

        Parameters
        ----------
        index: int (optional)
        element: typing.Dict

        Notes
        -----
        This is the default value for the {`node|edge`}_property_mapping property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_element_property_mapping(element: typing.Dict):
           ...
           w.set_{node|edge}_property_mapping(custom_element_property_mapping)

        Returns
        -------
        properties: typing.Dict

        """
        return element.get('properties', {})

    @staticmethod
    def default_node_property_mapping(index: int, node: TDict):
        """See default element property mapping."""
        return GraphWidget.default_element_property_mapping(index, node)

    @staticmethod
    def default_edge_property_mapping(index: int, edge: TDict):
        """See default element property mapping."""
        return GraphWidget.default_element_property_mapping(index, edge)

    def default_neo4j_color_mapping(self, index: int, element: TDict):
        itemtype = element['properties']['label']
        if itemtype not in self._itemtype2colorIdx:
            self._itemtype2colorIdx[itemtype] = len(self._itemtype2colorIdx)

        color_index = self._itemtype2colorIdx[itemtype] % len(COLOR_PALETTE)
        return COLOR_PALETTE[color_index]

    # noinspection PyUnusedLocal
    def default_node_color_mapping(self, index: int, node: TDict):
        """The default color mapping for nodes.

        Provides constant value of '#15AFAC' for all nodes, or different colors per label/type when importing a Neo4j
        graph.

        Parameters
        ----------
        index: int (optional)
        node: typing.Dict

        Notes
        -----
        This is the default value for the `node_color_mapping` property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_color_mapping(node: typing.Dict):
           ...
           w.set_node_color_mapping(custom_node_color_mapping)

        Returns
        -------
        color: str
            css color value

        References
        ----------
        css color value <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value>

        yFiles docs Fill api <https://docs.yworks.com/yfileshtml/#/api/Fill>

        """
        if self._data_importer == 'neo4j':
            return self.default_neo4j_color_mapping(index, node)
        else:
            return '#15AFAC'

    # noinspection PyUnusedLocal
    @staticmethod
    def default_node_styles_mapping(index: int, node: TDict):
        """The default styles mapping for nodes.

        Parameters
        ----------
        index: int (optional)
        node: typing.Dict

        Notes
        -----
        This is the default value for the `node_styles_mapping` property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_styles_mapping(node: typing.Dict):
           ...
           w.set_node_styles_mapping(custom_node_styles_mapping)

        Returns
        -------
        
        styles: typing.Dict
            can contain the following key-value-pairs:
                "color": str
                    css color value
                "shape": str
                    possible values: 'ellipse', 'hexagon', 'hexagon2', 'octagon', 'pill', 'rectangle', 'round-rectangle' or 'triangle'
                "image": str
                    url or data URL of the image

        References
        ----------
        css color value <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value>

        Data URL <https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs>

        """
        return {}
    @staticmethod
    def default_node_label_style_mapping(index: int, node: TDict):
        return {}

    # noinspection PyUnusedLocal

    def default_edge_color_mapping(self, index: int, edge: TDict):
        """The default color mapping for edges.

        Provides constant value of '#15AFAC' for all edges.

        Parameters
        ----------
        index: int (optional)
        edge: typing.Dict

        Notes
        -----
        This is the default value for the `edge_color_mapping` property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_edge_color_mapping(edge: typing.Dict):
           ...
           w.set_edge_color_mapping(custom_edge_color_mapping)

        Returns
        -------
        color: str
            css color value

        References
        ----------
        css color value <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value>

        yFiles docs Fill api <https://docs.yworks.com/yfileshtml/#/api/Fill>

        """
        if self._data_importer == 'neo4j':
            return self.default_neo4j_color_mapping(index, edge)
        else:
            return '#15AFAC'

    # noinspection PyUnusedLocal
    @staticmethod
    def default_node_scale_factor_mapping(index: int, node: TDict):
        """The default scale factor mapping for nodes.

        Provides constant value of 1.0 for all nodes.

        Parameters
        ----------
        index: int (optional)
        node: typing.Dict

        Notes
        -----
        This is the default value for the `node_scale_factor_mapping` property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_scale_factor_mapping(node: typing.Dict):
           ...
           w.set_node_scale_factor_mapping(custom_node_scale_factor_mapping)

        Returns
        -------
        node_scale_factor: float

        """
        return 1.0

    @staticmethod
    def default_heat_mapping(element: TDict):
        """The default scale factor mapping for nodes.

                Provides constant value of None for all elements.

                Parameters
                ----------
                index: int (optional)
                element: typing.Dict

                Notes
                -----
                This is the default value for the `heat_mapping` property.
                Can be 'overwritten' by setting the property
                with a function of the same signature.

                If the given mapping function has only one parameter (that is not typed as int),
                then it will be called with the element (typing.Dict) as first parameter.

                Example
                -------
                .. code::

                   from yfiles_jupyter_graphs import GraphWidget
                   w = GraphWidget()
                   def custom_heat_mapping(element: typing.Dict):
                   ...
                   w.set_heat_mapping(custom_heat_mapping)

                Returns
                -------
                heat: float | None

                """
        return None

    # noinspection PyUnusedLocal
    @staticmethod
    def default_node_size_mapping(index: int, node: TDict):
        """The default size mapping for nodes.

                Provides constant value 55.0, 55.0 for the width and height of all nodes.

                Parameters
                ----------
                index: int (optional)
                node: typing.Dict

                Notes
                -----
                This is the default value for the `node_size_mapping` property.
                Can be 'overwritten' by setting the property
                with a function of the same signature.

                If the given mapping function has only one parameter (that is not typed as int),
                then it will be called with the element (typing.Dict) as first parameter.

                Example
                -------
                .. code::

                   from yfiles_jupyter_graphs import GraphWidget
                   w = GraphWidget()
                   def custom_node_size_mapping(node: typing.Dict):
                   ...
                   w.set_node_size_mapping(custom_node_size_mapping)

                Returns
                -------
                size: float 2-tuple

                """
        return 55.0, 55.0


    @staticmethod
    def default_node_layout_mapping(index:int, node: TDict):
        """The default layout mapping for nodes.

                Provides constant value None for all nodes.
                Position and size mappings are used instead.
                Default position and size mappings are a constant value of 0.0, 0.0 and 55.0,55.0 respectively.

                Parameters
                ----------
                index: int (optional)
                node: typing.Dict

                Notes
                -----
                This is the default value for the `node_layout_mapping` property.
                Can be 'overwritten' by setting the property
                with a function returning a float 4-tuple.

                The layout overwrites position and size mappings if not None.

                If the given mapping function has only one parameter (that is not typed as int),
                then it will be called with the element (typing.Dict) as first parameter.

                Example
                -------
                .. code::

                   from yfiles_jupyter_graphs import GraphWidget
                   w = GraphWidget()
                   def custom_node_layout_mapping(node: typing.Dict):
                   ...
                   w.set_node_layout_mapping(custom_node_layout_mapping)

                Returns
                -------
                layout: None | float 4-tuple

                """
        return None

    # noinspection PyUnusedLocal
    @staticmethod
    def default_edge_thickness_factor_mapping(index: int, edge: TDict):
        """The default thickness factor mapping for edges.

        Provides constant value of 1.0 for all edges.

        Parameters
        ----------
        index: int (optional)
        edge: typing.Dict

        Notes
        -----
        This is the default value for the `edge_thickness_factor_mapping` property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_edge_thickness_factor_mapping(edge: typing.Dict):
           ...
           w.set_edge_thickness_factor_mapping(custom_edge_thickness_factor_mapping)

        Returns
        -------
        edge_thickness_factor: float

        """
        return 1.0

    # noinspection PyUnusedLocal
    @staticmethod
    def default_node_type_mapping(index: int, node: TDict):
        """The default type mapping for nodes.

        Provides the mapped node color to distinguish different node types

        Parameters
        ----------
        index: int (optional)
        node: typing.Dict

        Notes
        -----
        This is the default value for the `node_type_mapping` property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_type_mapping(node: typing.Dict):
           ...
           w.set_node_type_mapping(custom_node_type_mapping)

        Returns
        -------
        type: None

        """
        if 'color' in node:
            return node['color']
        else:
            return None
        
    @staticmethod
    def default_node_parent_mapping(index: int, node: TDict):
        """The default parent mapping for nodes.

        Provides constant value None for all nodes

        Parameters
        ----------
        index: int (optional)
        node: typing.Dict

        Notes
        -----
        This is the default value for the `node_parent_mapping` property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_parent_mapping(node: typing.Dict):
           ...
           w.set_node_parent_mapping(custom_node_parent_mapping)

        Returns
        -------
        parent: None

        """
        return None

    # noinspection PyUnusedLocal
    @staticmethod
    def default_node_position_mapping(index: int, node: TDict):
        """The default position mapping for nodes.

        Provides constant value of 0.0, 0.0 for all nodes.

        Parameters
        ----------
        index: int (optional)
        node: typing.Dict

        Notes
        -----
        This is the default value for the `node_position_mapping` property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_position_mapping(node: typing.Dict):
           ...
           w.set_node_position_mapping(custom_node_position_mapping)

        Returns
        -------
        position: float 2-tuple

        """
        return 0.0, 0.0

    @staticmethod
    def default_node_coordinate_mapping(index: int, node: TDict):
        """The default coordinate mapping for nodes.

        Provides constant value of None for all nodes.

        Parameters
        ----------
        index: int (optional)
        node: typing.Dict

        Notes
        -----
        This is the default value for the `node_coordinate_mapping` property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_node_coordinate_mapping(node: typing.Dict):
           ...
           w.set_node_coordinate_mapping(custom_node_coordinate_mapping)

        Returns
        -------
        coordinate: float 2-tuple

        """
        return None

    # noinspection PyUnusedLocal
    def default_directed_mapping(self, index: int, edge: TDict):
        """The default directed mapping for edges.

        Uses the graph wide directed attribute for all edges.

        Parameters
        ----------
        index: int (optional)
        edge: typing.Dict

        Notes
        -----
        This is the default value for the `directed_mapping` property.
        Can be 'overwritten' by setting the property
        with a function of the same signature.

        If the given mapping function has only one parameter (that is not typed as int),
        then it will be called with the element (typing.Dict) as first parameter.

        Example
        -------
        .. code::

           from yfiles_jupyter_graphs import GraphWidget
           w = GraphWidget()
           def custom_directed_mapping(edge: typing.Dict):
           ...
           w.set_directed_mapping(custom_directed_mapping)

        Returns
        -------
        directed: bool

        """
        return self._directed

    def _get_attribute_by_name(
            self,
            attribute_name: str,
            fallback_to: Optional[str] = None
    ):
        """get the specified attribute by name

        if fallback_to is set to a string
        then get attribute with name {fallback_to}{attribute_name}

        Parameters
        ----------
        attribute_name: str
        fallback_to: typing.Optional[str]

        Returns
        -------
        attribute: typing.Any

        """
        try:
            return getattr(self, attribute_name)
        except AttributeError as e:
            if fallback_to is not None:
                return getattr(self, fallback_to + attribute_name)
            raise e

    def _get_wrapped_mapping_function(
            self,
            function: Union[callable, str],
            key: str,
            strict: bool = True,
            remove_keys: Optional[TList[str]] = None
    ):
        """wrap mapping function so that return value is used for inplace update
        and for compatibility with arguments index and element

        mapping function return only one value
        but the underlying element (dict) should save this value


        Parameters
        ----------
        function: callable | str
            function to be wrapped or the property key whose value should be returned
        key: str
            element (dict) key that should be used
            to save the return value of the function
        strict: bool
            check if the element already has the key
        remove_keys: typing.Optional[typing.List[str]]
            specify optional list of keys that should be removed from element

        Returns
        -------
        wrapped: callable
            wrapped function

        """

        # helper function
        def _get_function_value(function: Union[callable, str], index: int, element: TDict):
            if isinstance(function, str):
                res = element.get('properties', {}).get(function, None)
                if res is None:
                    res = element.get(function, None)
                    if res is None:
                        return None
                return res

            parameters = inspect.signature(function).parameters
            if len(parameters) == 0:
                return function()
            elif len(parameters) == 1 and parameters[list(parameters)[0]].annotation == int:
                return function(index)
            elif len(parameters) == 1:
                return function(element)
            else:
                return function(index, element)


        def wrapped(index: int, element: TDict):
            """wrap mapping function"""
            try:
                value = _get_function_value(function, index, element)
            except (NameError, TypeError, KeyError, ValueError) as error:
                self.errorMessage = ''.join(f"Could not resolve the mapping function for the given data object \n "
                                            f"{{ \n \t {element} \n }} \n ")
                self.error = error
                return element
            assert not strict or key not in element.keys()

            if key == 'label':
                if isinstance(value, dict):
                    label = value.pop('text', '')
                    element['label'] = label
                    if 'styles' in element:
                        #node case
                        styles = element['styles']
                        styles['label_styles'] = value
                        element['styles'] = styles
                    else:
                        #edge case
                        element['label_styles'] = value
                elif value is not None:
                    element[key] = str(value)

            elif key == 'layout':
                if value is not None:
                    # layout mapping overwrites previous position and size results
                    element['position'] = value[:2]
                    element['size'] = value[2:]
            elif value is not None:
                element[key] = value

            if remove_keys:
                for r_key in remove_keys:
                    del element[r_key]

            return element

        return wrapped

    def _get_wrapped_mapping_function_by_name(self, function_name: str, *args, **kwargs):
        function = self._get_attribute_by_name(function_name, 'default')
        return self._get_wrapped_mapping_function(function, *args, **kwargs)

    def _get_mapping_functions_by_name(self, function_dict: TDict):
        return [
            self._get_wrapped_mapping_function_by_name(fn, **kwargs)
            for fn, kwargs in function_dict.items()
        ]

    def _get_node_mapping_functions(self):
        return self._get_mapping_functions_by_name({
            '_node_property_mapping': {'key': 'properties', 'strict': False},
            '_node_color_mapping': {'key': 'color', 'strict': False},
            '_node_styles_mapping': {'key': 'styles', 'strict': False},
            '_node_label_mapping': {'key': 'label', 'strict': False},
            '_node_scale_factor_mapping': {'key': 'scale_factor', 'strict': False},
            '_node_type_mapping': {'key': 'type', 'strict': False},
            '_node_size_mapping': {'key': 'size', 'strict': False},
            '_node_position_mapping': {'key': 'position', 'strict': False},
            '_node_layout_mapping': {'key': 'layout', 'strict': False},
            '_heat_mapping': {'key': 'heat', 'strict': False},
            '_node_coordinate_mapping': {'key': 'coordinates', 'strict': False},
            '_node_parent_mapping': {'key': 'parentId', 'strict': False}
        })

    def _get_edge_mapping_functions(self):
        return self._get_mapping_functions_by_name({
            '_edge_label_mapping': {'key': 'label', 'strict': False},
            '_edge_property_mapping': {'key': 'properties', 'strict': False},
            '_edge_color_mapping': {'key': 'color', 'strict': False},
            '_edge_thickness_factor_mapping': {'key': 'thickness_factor', 'strict': False},
            '_directed_mapping': {'key': 'directed', 'strict': False},
            '_heat_mapping': {'key': 'heat', 'strict': False}
        })

    @staticmethod
    def _apply_elements_mappings(elements: TList[TDict], mappings: TList[callable]):
        """for each element apply all mappings inorder and inplace

        Parameters
        ----------
        elements: typing.List[typing.Dict]
        mappings: typing.List[callable]

        Returns
        -------
        elements: typing.List[typing.Dict]

        """
        for index, element in enumerate(elements):
            for mapping in mappings:
                element = mapping(index, element)
            elements[index] = element
        return elements

    def _apply_mapping_and_change_value(
            self,
            key: str,
            mapping: callable,
            *args,
            temp_value: Optional[Any] = None,
            **kwargs
    ):
        """handle traitlet value change

        this is one possible solution to the problem that traitlets lists/dicts
        can not be changed inplace

        no checking is done if self really has traitlet attribute of name key

        https://stackoverflow.com/q/51482598

        related
        https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Events.html
        https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Custom.html
        https://github.com/jupyter-widgets/ipywidgets/issues/2916
        https://github.com/jupyter-widgets/ipywidgets/issues/2922
        https://github.com/ipython/traitlets/issues/443
        https://github.com/ipython/traitlets/pull/466
        https://github.com/ipython/traitlets/issues/495
        https://github.com/ipython/traitlets/issues/496
        https://github.com/ipython/traitlets/issues/557

        Parameters
        ----------
        key: str
            traitlet attribute to change
        mapping: callable
            function that calculates new traitlet value
            takes old value, args and kwargs as inputs
            return value is new traitlet value
        args: typing.List
        temp_value: typing.Optional[typing.Any]
            value for traitlet during mapping calculation
        kwargs: typing.Dict

        Returns
        -------

        """
        value = getattr(self, key)
        setattr(self, key, temp_value)
        value = mapping(value, *args, **kwargs)
        setattr(self, key, value)

    def _apply_node_mappings(self):
        self._apply_mapping_and_change_value(
            '_nodes',
            self._apply_elements_mappings,
            self._get_node_mapping_functions(),
            temp_value=[]
        )

    def _apply_edge_mappings(self):
        self._apply_mapping_and_change_value(
            '_edges',
            self._apply_elements_mappings,
            self._get_edge_mapping_functions(),
            temp_value=[]
        )

    def _scale_widget_layout(self):
        """
           Default widget layout is 500px height.
           If the graph has more than 10 nodes, for every node the height is increased by 10px.
           There is an upper limit at 800px
           The widget layout height is in [500px, 800px]

        """
        graph_size = len(self.get_nodes())
        if graph_size > 10 and not self._widget_layout_set_manually:
            new_height = min(800, 500 + SCALING_PER_NODE * graph_size)
            new_layout = Layout(height=(str(new_height)+'px'), width='100%')
            self.layout = new_layout

    def _ipython_display_(self, **kwargs):
        self.error = None
        self._apply_node_mappings()
        self._apply_edge_mappings()
        self._scale_widget_layout()
        # raise exception here to make sure mappings are always applied if possible
        if self.error is not None:
            raise Exception(self.errorMessage) from self.error
        # ipywidget version < 8.0
        if hasattr(super(), '_ipython_display_') and callable(getattr(super(), '_ipython_display_')):
            super()._ipython_display_(**kwargs)
        # ipywidget version >= 8.0
        elif hasattr(super(), '_repr_mimebundle_') and callable(getattr(super(), '_repr_mimebundle_')):
            display(super()._repr_mimebundle_(**kwargs), raw=True)
        else:
            raise AttributeError("The version of ipywidget is not supported. Consider creating a new issue here: https://github.com/yWorks/yfiles-jupyter-graphs/issues")

    def show(self):
        """Display widget in Jupyter.

        Same as using single object reference in cell directly.

        Notes
        -----
        Mappings will only be applied shortly before showing the widget.

        Returns
        -------

        """
        self._ipython_display_()

    def import_graph(self, graph):
        """Import a graph object defined in an external module.

        Sets the nodes, edges and directed traitlets properties
        with information extracted from the graph object.
        See yfiles_jupyter_graphs.graph.importer for object specific transformation details.

        Parameters
        ----------
        graph: networkx.{Multi}{Di}Graph | graph_tool.Graph | igraph.Graph | pygraphviz.AGraph
            graph data structure

        Example
        -------
        .. code::

            from networkx import florentine_families_graph
            from yfiles_jupyter_graphs import GraphWidget
            w = GraphWidget()
            w.import_graph(florentine_families_graph())

        Notes
        -----
        Some graph data structures have special attributes for labels, some don't.
        Same goes for other graph properties.
        This method and the underlying transformations should be seen as best effort
        to provide an easy way to input data into the widget.
        For more granular control use nodes and edges properties directly.

        Returns
        -------

        """
        self._nodes, self._edges, self._directed, self._data_importer = import_(graph)

    def get_graph_layout(self):
        """Getter for the graph layout traitlet property.

        Notes
        -----
        This function acts as an alias for using GraphWidget.graph_layout property
        e.g. w.graph_layout == w.get_graph_layout() is true.

        Returns
        -------
        graph_layout: typing.Dict
            Returned dict has keys algorithm: str and options: dict, however options are empty
            because the algorithms use default settings from yFiles library.

        """
        return self._graph_layout

    def set_graph_layout(self, algorithm):
        """Choose graph layout.

        Currently the algorithms use default settings from yFiles library.

        Parameters
        ----------
        algorithm: str
            Specify graph layout (or edge router) algorithm.
            Available algorithms are:
            ["circular", "hierarchic", "organic", "orthogonal", "radial", "tree",
            "orthogonal_edge_router", "organic_edge_router", "map"]

        Notes
        -----
        This function acts as an alias for using GraphWidget.graph_layout property
        e.g. w.graph_layout = 'organic' has the same effect
        as using w.set_graph_layout('organic').
        Setting w.graph_layout = {'algorithm': 'organic'} works as well,
        which corresponds to using value given through the associated getter.
        In case you want to use the edge routers
        you should set a custom node position mapping as well.

        See yFiles docs <https://docs.yworks.com/yfileshtml/#/dguide/layout-summary>
        for more details about the algorithms.

        Returns
        -------

        """
        if isinstance(algorithm, dict):
            _algorithm = algorithm
            algorithm = _algorithm.pop('algorithm', None)

        self._graph_layout = layout_(algorithm, **{})

    graph_layout = property(get_graph_layout, set_graph_layout)

    def map_layout(self):
        """Alias for self.set_graph_layout(algorithm="map").

        Uses geo-coordinates and a map background to visualize the graph.
        """
        self.set_graph_layout(**dict(algorithm="map"))

    def interactive_organic_layout(self):
        """Alias for self.set_graph_layout(algorithm="interactive_organic").

        See yFiles interactive organic layout guide
        <https://docs.yworks.com/yfileshtml/#/dguide/organic_layout#interactive_organic_layout>
        for more details about this specific algorithm.
        """
        self.set_graph_layout(**dict(algorithm="interactive_organic"))

    def circular_layout(self):
        """Alias for self.set_graph_layout(algorithm="circular").

        See yFiles circular layout guide
        <https://docs.yworks.com/yfileshtml/#/dguide/layout-summary#layout_styles-circular>
        for more details about this specific algorithm.
        """
        self.set_graph_layout(**dict(algorithm="circular"))

    def hierarchic_layout(self):
        """Alias for self.set_graph_layout(algorithm="hierarchic").

        See yFiles hierarchic layout guide
        <https://docs.yworks.com/yfileshtml/#/dguide/layout-summary#layout_styles-hierarchical>
        for more details about this specific algorithm.
        """
        self.set_graph_layout(**dict(algorithm="hierarchic"))

    def organic_layout(self):
        """Alias for self.set_graph_layout(algorithm="organic").

        See yFiles organic layout guide
        <https://docs.yworks.com/yfileshtml/#/dguide/layout-summary#layout_styles-organic>
        for more details about this specific algorithm.
        """
        self.set_graph_layout(**dict(algorithm="organic"))

    def orthogonal_layout(self):
        """Alias for self.set_graph_layout(algorithm="orthogonal").

        See yFiles orthogonal layout guide
        <https://docs.yworks.com/yfileshtml/#/dguide/layout-summary#layout_styles-orthogonal>
        for more details about this specific algorithm.
        """
        self.set_graph_layout(**dict(algorithm="orthogonal"))

    def radial_layout(self):
        """Alias for self.set_graph_layout(algorithm="radial").

        See yFiles radial layout guide
        <https://docs.yworks.com/yfileshtml/#/dguide/layout-summary#layout_styles-radial>
        for more details about this specific algorithm.
        """
        self.set_graph_layout(**dict(algorithm="radial"))

    def tree_layout(self):
        """Alias for self.set_graph_layout(algorithm="tree").

        See yFiles tree layout guide
        <https://docs.yworks.com/yfileshtml/#/dguide/layout-summary#layout_styles-tree>
        for more details about this specific algorithm.
        """
        self.set_graph_layout(**dict(algorithm="tree"))

    def orthogonal_edge_router(self):
        """Alias for self.set_graph_layout(algorithm="orthogonal_edge_router").

        See yFiles orthogonal edge router guide
        <https://docs.yworks.com/yfileshtml/#/dguide/layout-summary#layout_styles-polyline_router>
        for more details about this specific algorithm.
        """
        self.set_graph_layout(**dict(algorithm="orthogonal_edge_router"))

    def organic_edge_router(self):
        """Alias for self.set_graph_layout(algorithm="organic_edge_router").

        See yFiles organic edge router guide
        <https://docs.yworks.com/yfileshtml/#/dguide/layout-summary#layout_styles-organic_router>
        for more details about this specific algorithm.
        """
        self.set_graph_layout(**dict(algorithm="organic_edge_router"))

    def get_neighborhood(self):
        """Getter for the neighborhood traitlets property.

        Returns
        -------
        neighborhood: typing.Dict
            Returned dict has keys max_distance: int and selected_nodes: list,
            a list of node ids.

        """
        return self._neighborhood

    def set_neighborhood(self, max_distance: int = 1, selected_nodes: Optional[list] = None):
        """Specify the neighborhood view in the widget.

        The number of hops and focused nodes can be chosen.

        Parameters
        ----------
        max_distance: int
            Set the maximum distance between selected and included nodes.
            If there are multiple paths to one (or multiple) selected nodes,
            the smallest path length is considered for this threshold.
        selected_nodes: typing.Optional[typing.List]
            Choose a list of node ids that are highlighted in both
            main and neighborhood component.
            They act as starting points for neighborhood calculation.

        Notes
        -----
        This function acts as an alias for using GraphWidget.neighborhood property.
        You can assign values by w.neighborhood = {'max_distance': 2, 'selected_nodes':[2]}
        or w.set_neighborhood(2, [2]), both are equivalent.
        The short form w.neighborhood = 3 sets only the max_distance variable
        and resets the selected nodes.

        Returns
        -------

        """
        if isinstance(max_distance, dict):
            _neighborhood = max_distance
            max_distance = _neighborhood.pop('max_distance', 1)
            selected_nodes = _neighborhood.pop('selected_nodes', None)
        if selected_nodes is None:
            selected_nodes = []
        self._neighborhood = dict(max_distance=max_distance, selected_nodes=selected_nodes)

    neighborhood = property(get_neighborhood, set_neighborhood)

    def get_selection(self):
        """Getter for the exported selection.

            Returns
            -------
            nodes: typing.List[typing.Dict], edges: typing.List[typing.Dict]

                Each node has the keys id: int and properties: typing.Dict.
                Each edge has the keys id: int, start: int, end: int and properties: typing.Dict.

        """
        if not self._selected_graph:
            self._selected_graph = [[], []]
        return self._selected_graph

    def get_sidebar(self):
        """Getter for the sidebar traitlets property.

        Returns
        -------
        sidebar: typing.Dict
            Returned dict has keys enabled: bool and start_with: str,
            whereat first one indicates open or closed sidebar and
            second one indicates start panel on widget show.

        """
        return self._sidebar

    def set_sidebar(self, enabled=True, start_with: str = ''):
        """Specify the appearance of the sidebar in the widget.

        Can be used to collapse sidebar or start with any panel.

        Parameters
        ----------
        enabled: bool
            Whether to open or collapse sidebar at widget startup.
        start_with: str
            The start panel identifier.
            Available are 'Neighborhood', 'Data', 'Search' and 'About' (the default).

        Notes
        -----
        This function acts as an alias for using GraphWidget.sidebar property.
        You can assign values by w.sidebar = {'enabled': True, 'start_with': 'Search'}
        or w.set_sidebar(True, 'Search'), both are equivalent.
        The short form w.sidebar = True sets only the enabled variable
        and resets the start_with back to the default.

        Returns
        -------

        """
        if isinstance(enabled, dict):
            _sidebar = enabled
            enabled = _sidebar.pop('enabled', True)
            start_with = _sidebar.pop('start_with', '')
        self._sidebar = dict(enabled=enabled, start_with=start_with)

    sidebar = property(get_sidebar, set_sidebar)

    def get_overview(self):
        """Getter for the overview traitlets property.

        Returns
        -------
        overview: bool
            Indicates open or closed overview state.
            A value of None means that a specific behaviour based on widget layout is followed.

        """
        return self._overview.get('enabled')

    def set_overview(self, enabled=True):
        """Specify the appearance of the overview component in the widget.

        Can be used to force open overview in case of a small widget layout or
        force collapsed overview in case of large widget layout.

        Parameters
        ----------
        enabled: bool
            Whether to open or collapse overview at widget startup.

        Returns
        -------

        """
        self._overview = dict(enabled=enabled, overview_set=True)

    overview = property(get_overview, set_overview)
