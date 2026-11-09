# FAIR Schema Toolkit

[![Development Status](https://img.shields.io/badge/status-early%20release-orange.svg)](https://github.com/DataArtifex/fairschema-toolkit)
[![Documentation](https://img.shields.io/badge/docs-blue)](https://www.dataartifex.org/fairschema-toolkit/)
[![Ask DeepWiki](https://img.shields.io/badge/Ask%20DeepWiki-AI%20Docs-5C54E5)](https://deepwiki.com/DataArtifex/fairschema-toolkit)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Package Status](https://img.shields.io/badge/PyPI-not%20published-lightgrey)](https://github.com/DataArtifex/fairschema-toolkit)
[![CI](https://github.com/DataArtifex/fairschema-toolkit/actions/workflows/test.yml/badge.svg)](https://github.com/DataArtifex/fairschema-toolkit/actions/workflows/test.yml)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-261230.svg?logo=ruff&logoColor=D7FF64)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

**This project is in its early development stages. Stability is not guaranteed, and documentation is limited. We welcome your feedback and contributions.**

## Overview

FAIR Schema Toolkit (`dartfx-fairschema`) is a Python toolkit for working with FAIR Data JSON Schemas, semantic metadata, and annotations within the Data Artifex ecosystem. It provides models, utilities, and validation helpers for authoring, inspecting, and manipulating FAIR-annotated schemas.

## Bootstrapping a New Project

1. **Rename the Project**: If you are using this repository as a template, run the included rename script to set your project and package names:

```bash
./rename.sh "my-project-name" "my_package_name"
```

2. **Register with DeepWiki**: To ensure your documentation is indexed and discoverable by AI agents, register your new repository at [DeepWiki.com](https://deepwiki.com/).

## Installation

This project recommends using [uv](https://github.com/astral-sh/uv) for fast and reliable Python package management.

### Using uv (Recommended)

To set up the development environment with `uv`:

```bash
# Install dependencies and create virtual environment
uv sync
```

### Using Hatch

You can also use [Hatch](https://hatch.pypa.io/) directly:

```bash
# Run tests
hatch run test

# Enter the default shell
hatch shell
```

### Local Installation

For traditional installation:

```bash
pip install -e .
```

## Development

### Version Management
Versions are managed dynamically in `src/dartfx/fairschema/__about__.py`. You can use `hatch version` to view or bump the version.

### Secret Management
For local development, create a `.env` file in the root directory. This file is git-ignored and can be used to store local API keys or configuration. These are automatically loaded by the test suite.

### Running Tests
```bash
uv run pytest
```

### Building Documentation
```bash
hatch run docs:build
```

## Usage

```python
from dartfx.fairschema import (
    annotate_property,
    extract_fair_annotations,
    is_fair_schema,
)

# Inspect a schema
is_fair = is_fair_schema({"$schema": "https://highvaluedata.net/fair-data-schema"})

# Annotate a property
property_schema = annotate_property(
    {"type": "number"},
    label="Temperature",
    measurement_unit="deg_C",
    concept="Air Temperature",
)
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines and information on how to get started.
