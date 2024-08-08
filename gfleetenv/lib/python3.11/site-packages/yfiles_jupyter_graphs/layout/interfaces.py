"""
Common interfaces for graph layout configurations.
"""

from abc import ABC, abstractmethod


class ConfigurationInterface(ABC):
    """Common interface for graph layout configurations."""

    def __init__(self, algorithm: str):
        self._algorithm = algorithm

    @staticmethod
    @abstractmethod
    def _parse_options(**kwargs):
        """"""

    def __call__(self, *args, **kwargs):
        return dict(algorithm=self._algorithm, options=self._parse_options(**kwargs))


class ConfigurationFactoryInterface(ABC):
    """Common factory interface for graph layout configurations.

    Provides only one graph layout configuration and
    does not maintain any of the instances it creates.
    """

    @abstractmethod
    def _get_configuration(self) -> ConfigurationInterface:
        """"""

    def __call__(self, *args, **kwargs):
        return self._get_configuration()


class LayoutConfigurationInterface(ConfigurationInterface, ABC):
    """same as parent, different name"""
    pass


class LayoutConfigurationFactoryInterface(ConfigurationFactoryInterface, ABC):
    """same as parent, different name"""
    pass


class EdgeRouterConfigurationInterface(ConfigurationInterface, ABC):
    """same as parent, different name"""
    pass


class EdgeRouterConfigurationFactoryInterface(ConfigurationFactoryInterface, ABC):
    """same as parent, different name"""
    pass
