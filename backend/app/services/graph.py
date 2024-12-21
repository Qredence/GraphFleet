from typing import Dict, List, Optional, Set, Tuple

import networkx as nx
from pydantic import BaseModel

class GraphService:
    def __init__(self):
        self.graph = nx.Graph()
        
    def add_node(self, node_id: str, **attributes):
        """Add a node to the graph with optional attributes."""
        self.graph.add_node(node_id, **attributes)
        
    def add_edge(self, source: str, target: str, **attributes):
        """Add an edge between two nodes with optional attributes."""
        self.graph.add_edge(source, target, **attributes)
        
    def get_neighbors(self, node_id: str) -> List[str]:
        """Get all neighbors of a given node."""
        return list(self.graph.neighbors(node_id))
        
    def get_node_attributes(self, node_id: str) -> Dict:
        """Get all attributes of a given node."""
        return dict(self.graph.nodes[node_id])
        
    def get_edge_attributes(self, source: str, target: str) -> Dict:
        """Get all attributes of a given edge."""
        return dict(self.graph[source][target])
        
    def get_shortest_path(self, source: str, target: str) -> List[str]:
        """Get the shortest path between two nodes."""
        try:
            return nx.shortest_path(self.graph, source, target)
        except nx.NetworkXNoPath:
            return []
            
    def get_connected_components(self) -> List[Set[str]]:
        """Get all connected components in the graph."""
        return list(nx.connected_components(self.graph))
        
    def get_subgraph(self, nodes: List[str]) -> 'GraphService':
        """Get a subgraph containing only the specified nodes."""
        subgraph = GraphService()
        subgraph.graph = self.graph.subgraph(nodes).copy()
        return subgraph
