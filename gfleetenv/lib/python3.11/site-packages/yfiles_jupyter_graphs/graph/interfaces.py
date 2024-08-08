"""
Common interfaces for graph importers.
"""

from abc import ABC, abstractmethod
from typing import Tuple, List, Dict


class GraphImporterInterface(ABC):
    """Common interface for graph importers."""
    def __init__(self, _type) -> None:
        super().__init__()
        self._type = _type

    @abstractmethod
    def _import(self, graph) -> Tuple[List[Dict], List[Dict], bool]:
        """import graph"""

    def isInstance(self, graph):
        return self._type is not None and isinstance(graph, self._type)

    def __call__(self, graph):
        assert self.isInstance(graph)
        return self._import(graph)
