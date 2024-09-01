# tree-sitter-wasms
Prebuilt WASM binaries for tree-sitter's language parsers. Forked from https://github.com/Menci/tree-sitter-wasm-prebuilt because I wanted to use GitHub Actions to automate publishing.

## Installation

```bash
pnpm add tree-sitter-wasms
# or
yarn add tree-sitter-wasms
# or
npm install tree-sitter-wasms
```

## Usage

```ts
import treeSitterRust from "tree-sitter-wasms/out/tree-sitter-rust.wasm"
parser.setLanguage(treeSitterCpp);
```

## Supported Languages

Check https://unpkg.com/browse/tree-sitter-wasms@latest/out/ to see all supported languages, and manually download the wasm artifacts directly.
