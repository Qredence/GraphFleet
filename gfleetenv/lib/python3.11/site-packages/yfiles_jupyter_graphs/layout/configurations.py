"""
Includes implementations for a few layout and edge router configurations.
"""

from .interfaces import LayoutConfigurationInterface, EdgeRouterConfigurationInterface


class CircularLayoutConfiguration(LayoutConfigurationInterface):
    """Configuration for circular layout."""
    def __init__(self):
        super().__init__('circular')

    @staticmethod
    def _parse_options(**kwargs):
        return dict()


class HierarchicLayoutConfiguration(LayoutConfigurationInterface):
    """Configuration for hierarchic layout."""
    def __init__(self):
        super().__init__('hierarchic')

    @staticmethod
    def _parse_options(**kwargs):
        return dict()


class OrganicLayoutConfiguration(LayoutConfigurationInterface):
    """Configuration for organic layout."""
    def __init__(self):
        super().__init__('organic')

    @staticmethod
    def _parse_options(**kwargs):
        return dict()


class OrthogonalLayoutConfiguration(LayoutConfigurationInterface):
    """Configuration for orthogonal layout."""
    def __init__(self):
        super().__init__('orthogonal')

    @staticmethod
    def _parse_options(**kwargs):
        return dict()


class RadialLayoutConfiguration(LayoutConfigurationInterface):
    """Configuration for radial layout."""
    def __init__(self):
        super().__init__('radial')

    @staticmethod
    def _parse_options(**kwargs):
        return dict()


class TreeLayoutConfiguration(LayoutConfigurationInterface):
    """Configuration for tree layout."""
    def __init__(self):
        super().__init__('tree')

    @staticmethod
    def _parse_options(**kwargs):
        return dict()


class OrthogonalEdgeRouterConfiguration(EdgeRouterConfigurationInterface):
    """Configuration for orthogonal edge router."""
    def __init__(self):
        super().__init__('orthogonal_edge_router')

    @staticmethod
    def _parse_options(**kwargs):
        return dict()


class OrganicEdgeLayoutConfiguration(EdgeRouterConfigurationInterface):
    """Configuration for organic edge router."""
    def __init__(self):
        super().__init__('organic_edge_router')

    @staticmethod
    def _parse_options(**kwargs):
        return dict()

class MapLayoutConfiguration(LayoutConfigurationInterface):
    """Configuration for map layout."""
    def __init__(self):
        super().__init__('map')

    @staticmethod
    def _parse_options(**kwargs):
        return dict()

class InteractiveOrganicLayoutConfiguration(LayoutConfigurationInterface):
    """Configuration for interactive organic layout."""
    def __init__(self):
        super().__init__('interactive_organic')

    @staticmethod
    def _parse_options(**kwargs):
        return dict()
