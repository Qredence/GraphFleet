"""
Includes corresponding factories for the layout configurations.
"""

from .interfaces import \
    LayoutConfigurationInterface, \
    LayoutConfigurationFactoryInterface, \
    EdgeRouterConfigurationInterface, \
    EdgeRouterConfigurationFactoryInterface
from .configurations import \
    CircularLayoutConfiguration, \
    OrganicLayoutConfiguration, \
    HierarchicLayoutConfiguration, \
    OrthogonalLayoutConfiguration, \
    RadialLayoutConfiguration, \
    TreeLayoutConfiguration, \
    OrthogonalEdgeRouterConfiguration, \
    OrganicEdgeLayoutConfiguration, \
    MapLayoutConfiguration, \
    InteractiveOrganicLayoutConfiguration


class CircularLayoutConfigurationFactory(LayoutConfigurationFactoryInterface):
    """factory providing circular layout configuration"""

    # noinspection PyMethodMayBeStatic
    def _get_configuration(self) -> LayoutConfigurationInterface:
        return CircularLayoutConfiguration()


class HierarchicLayoutConfigurationFactory(LayoutConfigurationFactoryInterface):
    """factory providing hierarchic layout configuration"""

    # noinspection PyMethodMayBeStatic
    def _get_configuration(self) -> LayoutConfigurationInterface:
        return HierarchicLayoutConfiguration()


class OrganicLayoutConfigurationFactory(LayoutConfigurationFactoryInterface):
    """factory providing organic layout configuration"""

    # noinspection PyMethodMayBeStatic
    def _get_configuration(self) -> LayoutConfigurationInterface:
        return OrganicLayoutConfiguration()


class OrthogonalLayoutConfigurationFactory(LayoutConfigurationFactoryInterface):
    """factory providing orthogonal layout configuration"""

    # noinspection PyMethodMayBeStatic
    def _get_configuration(self) -> LayoutConfigurationInterface:
        return OrthogonalLayoutConfiguration()


class RadialLayoutConfigurationFactory(LayoutConfigurationFactoryInterface):
    """factory providing radial layout configuration"""

    # noinspection PyMethodMayBeStatic
    def _get_configuration(self) -> LayoutConfigurationInterface:
        return RadialLayoutConfiguration()


class TreeLayoutConfigurationFactory(LayoutConfigurationFactoryInterface):
    """factory providing tree layout configuration"""

    # noinspection PyMethodMayBeStatic
    def _get_configuration(self) -> LayoutConfigurationInterface:
        return TreeLayoutConfiguration()


class OrthogonalEdgeRouterConfigurationFactory(EdgeRouterConfigurationFactoryInterface):
    """factory providing orthogonal edge router configuration"""

    # noinspection PyMethodMayBeStatic
    def _get_configuration(self) -> EdgeRouterConfigurationInterface:
        return OrthogonalEdgeRouterConfiguration()


class OrganicEdgeRouterConfigurationFactory(EdgeRouterConfigurationFactoryInterface):
    """factory providing organic edge router configuration"""

    # noinspection PyMethodMayBeStatic
    def _get_configuration(self) -> EdgeRouterConfigurationInterface:
        return OrganicEdgeLayoutConfiguration()

class MapConfigurationFactory(LayoutConfigurationFactoryInterface):
    """factory providing map layout configuration"""

    # noinspection PyMethodMayBeStatic
    def _get_configuration(self) -> MapLayoutConfiguration:
        return MapLayoutConfiguration()

class InteractiveOrganicLayoutConfigurationFactory(LayoutConfigurationFactoryInterface):
    """factory providing map layout configuration"""

    # noinspection PyMethodMayBeStatic
    def _get_configuration(self) -> LayoutConfigurationInterface:
        return InteractiveOrganicLayoutConfiguration()


def _get_layout_factory(name) -> LayoutConfigurationFactoryInterface:
    factories = {
        "circular": CircularLayoutConfigurationFactory(),
        "hierarchic": HierarchicLayoutConfigurationFactory(),
        "organic": OrganicLayoutConfigurationFactory(),
        "orthogonal": OrthogonalLayoutConfigurationFactory(),
        "radial": RadialLayoutConfigurationFactory(),
        "tree": TreeLayoutConfigurationFactory(),
        "orthogonal_edge_router": OrthogonalEdgeRouterConfigurationFactory(),
        "organic_edge_router": OrganicEdgeRouterConfigurationFactory(),
        "map": MapConfigurationFactory(),
        "interactive_organic": InteractiveOrganicLayoutConfigurationFactory()
    }
    return factories[name]
