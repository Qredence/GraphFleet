"""
Information about the frontend package of the widgets.
"""

import json
import os
import pathlib


def _fetch_package_info():
    here = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

    for settings in here.rglob("package.json"):
        try:
            with settings.open() as f:
                package = json.load(f)
                version = package["version"]
                name = package["name"]
                return version, name
        except FileNotFoundError:
            pass

    raise FileNotFoundError(f"Could not find package.json under dir {here!s}")


package_json_version, package_json_name = _fetch_package_info()

module_name = package_json_name
module_version = "^" + package_json_version
