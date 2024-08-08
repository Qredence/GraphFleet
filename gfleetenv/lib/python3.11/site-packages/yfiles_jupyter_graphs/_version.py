"""
Provide version information of the package.
"""

from ._frontend import _fetch_package_info

__all__ = ["__version__"]

__version__, _ = _fetch_package_info()
__version__ = __version__.replace("-alpha.", "a").replace("-beta.", "b").replace("-rc.", "rc")
