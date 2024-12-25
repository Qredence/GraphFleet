#!/bin/bash

# Function to check if uv is installed
check_uv() {
    if ! command -v uv &> /dev/null; then
        echo "uv is not installed. Installing..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi
}

# Function to create virtual environment
create_venv() {
    echo "Creating virtual environment..."
    uv venv
}

# Function to install dependencies
install_deps() {
    echo "Installing dependencies..."
    uv pip install -r requirements.txt
}

# Main script
check_uv

case "$1" in
    "init")
        create_venv
        install_deps
        ;;
    "install")
        install_deps
        ;;
    "compile")
        echo "Compiling dependencies..."
        uv pip compile requirements.txt -o requirements.lock
        ;;
    "clean")
        echo "Cleaning cache..."
        uv cache clean
        ;;
    *)
        echo "Usage: $0 {init|install|compile|clean}"
        echo "  init     - Create venv and install dependencies"
        echo "  install  - Install dependencies in existing venv"
        echo "  compile  - Compile dependencies to requirements.lock"
        echo "  clean    - Clean uv cache"
        exit 1
        ;;
esac 