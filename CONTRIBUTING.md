# Contributing to GraphFleet

First off, thank you for considering contributing to GraphFleet! It's people like you that make GraphFleet such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Development Process

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

1. Ensure you have Python 3.10+ installed
2. Clone your fork and set up the development environment:

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/graphfleet.git
cd graphfleet

# Set up Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies with uv
curl -LsSf https://astral.sh/uv/install.sh | sh  # Install uv if you haven't already
uv pip install --upgrade uv  # Ensure latest uv version
uv pip install build hatchling  # Install build tools
uv sync  # Install all dependencies from pyproject.toml
uv pip install -e ".[dev]"  # Install package in editable mode

# Set up frontend (if working on UI)
cd frontend
npm install
```

## Project Structure

- `backend/`: Python backend service
  - `app/`: Main application code
  - `graphfleet/`: Core library
  - `tests/`: Backend tests

- `graspologic/`: Graph processing library
  - `src/`: Source code
  - `tests/`: Tests
  - `docs/`: Documentation

- `graspologic-native/`: Native extensions
  - `src/`: Rust source code
  - `python/`: Python bindings

- `frontend/`: React frontend application
  - `src/`: Source code
  - `tests/`: Frontend tests

## Testing

We use pytest for Python tests and Jest for JavaScript tests:

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

## Code Style

We use several tools to maintain code quality:

- Python: black, isort, mypy, ruff
- JavaScript: eslint, prettier

Run linting:

```bash
# Python
ruff check .
black .
isort .
mypy .

# JavaScript
cd frontend
npm run lint
```

## Documentation

- Update documentation for any new features
- Add docstrings to Python functions
- Include JSDoc comments for JavaScript functions
- Update API documentation if endpoints change

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the documentation with details of any new features
3. The PR must pass all CI checks
4. At least one core team member must review and approve

## Release Process

1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Build and publish the package:
```bash
# Build the package
uv pip install build
python -m build

# Publish to PyPI
uv pip install twine
python -m twine upload dist/*
```
4. Create a new GitHub release
5. CI will automatically publish to PyPI

## Getting Help

- Join our [Discord community](https://discord.gg/graphfleet)
- Open a [GitHub Discussion](https://github.com/qredence/graphfleet/discussions)
- Check our [Documentation](https://docs.graphfleet.ai)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

