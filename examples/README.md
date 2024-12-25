# GraphFleet Examples

This directory contains examples demonstrating how to use GraphFleet for various tasks.

## Text File Indexing Example

The `index_text.py` script shows how to index a text file using GraphFleet. It demonstrates:
- Text chunking with configurable size and overlap
- Metadata handling
- Basic search functionality

### Prerequisites

1. Install GraphFleet with development dependencies:
```bash
./scripts/uv_install.sh install --dev
```

2. Set up your environment variables in `.env`:
```env
GRAPHRAG_API_KEY=your_api_key
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
```

### Usage

1. Basic usage with default settings:
```bash
python examples/index_text.py examples/sample.txt
```

2. Custom chunk size and overlap:
```bash
python examples/index_text.py examples/sample.txt --chunk-size 800 --chunk-overlap 150
```

### Example Output

```
Created 5 chunks from text
Indexed chunk 1/5
Indexed chunk 2/5
Indexed chunk 3/5
Indexed chunk 4/5
Indexed chunk 5/5
Indexing complete!

Test Query: What is the main topic discussed in this text?
Result: The main topic discussed in this text is GraphRAG, which is an innovative approach...
```

### Understanding the Code

The example demonstrates several key concepts:

1. Text Chunking:
   - Uses sentence-based chunking for better context preservation
   - Configurable chunk size and overlap
   - Handles text splitting intelligently

2. Metadata Handling:
   - Tracks source file information
   - Maintains chunk ordering
   - Preserves relationships between chunks

3. Indexing Process:
   - Asynchronous processing for better performance
   - Progress tracking
   - Error handling

4. Search Capabilities:
   - Simple query interface
   - Context-aware responses
   - Graph-based retrieval

### Customization

You can modify the script to:
- Add custom metadata
- Implement different chunking strategies
- Add additional processing steps
- Customize the search behavior

### Additional Examples

Check out other examples in this directory for more advanced usage scenarios:
- Batch document processing
- Custom entity extraction
- Advanced search patterns
- Graph visualization 