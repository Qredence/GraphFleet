"""
Module for reading environment variables and configuration files.

This module provides functionality to read environment variables and configuration files
using the `os`, `re`, and `yaml` modules.
"""


import os
import re
import yaml
from dotenv import load_dotenv


# Load environment variables from .env file
def load_dotenv(
    dotenv_path: StrPath | None = None,
    stream: IO[str] | None = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
    encoding: str | None = "utf-8"
):

# Function to replace placeholders with environment variables
def replace_placeholders(content):
    pattern = re.compile(r'\$\(([A-Za-z0-9_]+)\)')
    matches = pattern.findall(content)
    for match in matches:
        env_value = os.getenv(match)
        if env_value is not None:
            content = content.replace(f'${{{match}}}', env_value)
    return content

# Read the settings.yaml file
with open('settings.yaml', 'r') as file:
    yaml_content = file.read()

# Replace placeholders with environment variables
yaml_content = replace_placeholders(yaml_content)

# Parse the YAML content
settings = yaml.safe_load(yaml_content)

# Print the settings to verify
print(yaml.dump(settings, default_flow_style=False))
