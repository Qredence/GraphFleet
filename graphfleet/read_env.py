from dotenv import load_dotenv
import os
import yaml
import re

# Load environment variables from .env file
load_dotenv()

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
