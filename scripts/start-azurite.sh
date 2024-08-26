#!/bin/sh

# Check if Azurite is installed
if ! command -v azurite >/dev/null 2>&1; then
    echo "Azurite is not installed. Please install it using 'sudo npm install -g azurite'"
    exit 1
fi

# Create directories if they don't exist
mkdir -p ./temp_azurite

# Run Azurite
azurite -L -l ./temp_azurite -d ./temp_azurite/debug.log