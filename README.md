# GraphFleet

A powerful graph-based knowledge management and query system designed for large-scale data processing and analysis. GraphFleet combines semantic search, knowledge graphs, and advanced analytics to provide deep insights into your data.

## 🚀 Key Features

- **Advanced Document Processing**
  - Semantic indexing and search
  - Automatic knowledge graph construction
  - Multi-format document support (PDF, Markdown, Code, etc.)

- **Graph Analytics**
  - Custom query pipelines
  - Concept drift analysis
  - Community detection
  - Path analysis and recommendations

- **Performance & Scale**
  - Distributed processing support
  - Native extensions for performance-critical operations
  - Efficient batch processing
  - Real-time query capabilities

- **Developer Experience**
  - Modern React frontend
  - RESTful and GraphQL APIs
  - Comprehensive documentation
  - Docker-based development environment

## 🏗️ Architecture

GraphFleet consists of three main components:

1. **Core Engine (graphfleet)**
   - Document processing and indexing
   - Knowledge graph management
   - Query processing

2. **Graph Processing (graspologic)**
   - Graph algorithms implementation
   - Analytics and metrics
   - Visualization utilities

3. **Native Extensions (graspologic-native)**
   - Performance-critical operations in Rust
   - SIMD optimizations
   - Custom memory management

## 🛠️ Installation

### Using uv

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install graphfleet
uv pip install graphfleet[all]
```

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/qredence/graphfleet.git
cd graphfleet
```

2. Set up development environment:
```bash
# Using Docker (recommended)
docker compose up -d

# Or manual setup
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies with uv
uv pip install --upgrade uv  # Ensure latest uv version
uv pip install build hatchling  # Install build tools
uv sync  # Install all dependencies from pyproject.toml
uv pip install -e ".[dev]"  # Install package in editable mode
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

## 📚 Documentation

- [Getting Started Guide](./docs/guides/getting-started.md)
- [API Reference](./docs/api/README.md)
- [Architecture Overview](./docs/architecture/README.md)
- [Contributing Guidelines](./CONTRIBUTING.md)

## 🧪 Examples

The `examples/` directory contains various use cases and tutorials:

- Basic document indexing and search
- Custom query pipeline creation
- Knowledge graph visualization
- Performance optimization techniques

## 🛣️ Project Structure

```
graphfleet/
├── backend/                    # Backend service
│   ├── app/                   # Main application code
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core business logic
│   │   ├── models/           # Data models
│   │   └── utils/            # Utility functions
│   ├── graphfleet/           # GraphFleet core library
│   └── tests/                # Backend tests
├── graspologic/               # Graph processing library
│   ├── src/                  # Source code
│   ├── tests/                # Tests
│   └─�� docs/                 # Library documentation
├── graspologic-native/        # Native extensions
│   ├── src/                  # Rust/C++ source
│   └── python/               # Python bindings
├── frontend/                  # Frontend application
└── docs/                     # Project documentation
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🔒 Security

For security concerns, please refer to our [Security Policy](SECURITY.md).

## 🌟 Acknowledgments

GraphFleet is built on top of several amazing open-source projects:

- [NetworkX](https://networkx.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [sentence-transformers](https://www.sbert.net/)

## ✨ Core Team

- Zachary BENSALEM ([@zbensalem](https://github.com/zbensalem)) - Project Lead
