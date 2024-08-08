"""
Submodule for graph layout configurations.

Notes
-----
Most of this module is not necessary as
layouts use defaults from yFiles library anyway.
"""

from .factories import _get_layout_factory


def _simplify_layout_name(name):
    return name.lower()


def _get_layout_by_name(name):
    return _get_layout_factory(name)()


def layout_(name: str, **kwargs):
    """construct layout configuration from name and keyword arguments"""
    _name = _simplify_layout_name(name)
    return _get_layout_by_name(_name)(**kwargs)
