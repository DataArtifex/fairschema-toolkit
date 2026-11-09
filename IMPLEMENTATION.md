# Technical Implementation

This document describes the technical architecture and implementation details of `fairschema-toolkit` (`dartfx-fairschema`).

## Architecture Overview

`fairschema-toolkit` provides type-safe Pydantic models and functional utilities for inspecting, authoring, and manipulating FAIR-extended JSON Schemas based on the [FAIR Data JSON Schema](https://highvaluedata.net/fair-data-schema) specification.

```
fairschema-toolkit/
├── src/dartfx/fairschema/
│   ├── __about__.py       # Package version metadata (source of truth)
│   ├── __init__.py        # Public API exports
│   ├── constants.py       # Dialect URIs, prefixes, and defaults
│   ├── models.py          # Pydantic 2.x models (SchemaNode, DatasetSchema, FAIRAnnotation, helpers)
│   ├── py.typed           # PEP 561 typing marker
│   └── schema.py          # Dialect inspection, annotation extraction, and enrichment
└── tests/
    ├── conftest.py        # Test fixtures and environment loading
    └── test_fairschema.py # Unit and integration test suite
```

## Core Models

### 1. `SchemaNode`
`SchemaNode` represents any node in a FAIR-extended JSON Schema. It implements:
- **Draft 2020-12 Vocabulary**: Core (`$id`, `$ref`, `$defs`), Metadata (`title`, `description`, `examples`, `links`), Validation (`type`, `enum`, `minimum`, `pattern`, etc.), Applicators (`properties`, `items`, `allOf`, `anyOf`, `oneOf`, etc.), Unevaluated properties/items, Format, and Content keywords.
- **FAIR Annotations**: Fields prefixed with `fair_` mapping directly to their `fair:` aliases (e.g., `fair_label` → `fair:label`, `fair_concept_ref` → `fair:conceptRef`, `fair_measurement_unit` → `fair:measurementUnit`, `fair_clamped` → `fair:clamped`).
- **Methods**:
  - `to_dict()`: Serializes node to JSON Schema dictionary with `fair:` keys, excluding nulls.
  - `to_json()`: Serializes node to formatted JSON string.
  - `fair_annotations`: Property extracting all `fair:` annotations into a `FAIRAnnotation` instance.

### 2. `DatasetSchema`
Subclass of `SchemaNode` representing the root schema of a FAIR dataset:
- Defaults `$schema` to the FAIR dialect URI (`https://highvaluedata.net/fair-data-schema/dev`).
- Factory methods:
  - `from_dict(data: dict[str, Any]) -> DatasetSchema`
  - `from_json(text: str) -> DatasetSchema`
  - `from_file(path: str | Path) -> DatasetSchema`
- Persistence method:
  - `to_file(path: str | Path, indent: int = 2) -> None`

### 3. `FAIRAnnotation`
A focused Pydantic `BaseModel` for working exclusively with FAIR metadata annotations:
- Supports all 42 FAIR vocabulary properties (`label`, `concept`, `conceptRef`, `measurementUnit`, `temporalCoverage`, `license`, `clamped`, `sentinel`, etc.).
- Accommodates unmodeled/custom extensions via `__pydantic_extra__` and the `extra` accessor property.
- Serializes cleanly back to `fair:` prefixed dictionaries via `to_dict()`.

### 4. Supporting Helper Models
- `TemporalCoverage`: ISO-8601 interval representation (`start`, `end`, `description`).
- `DatasetRelation`: Structured dataset and variable relationship links (`relationType`, `targetRef`, `sourceVariables`, `targetVariables`).
- `ChecksumObject`: Bit-level checksum metadata (`algorithm`, `algorithmRef`, `value`).
- `LinkDescriptionObject`: Hypermedia / distribution link descriptor following RFC 8288 and JSON Hyper-Schema with FAIR annotations (`href`, `rel`, `targetMediaType`, `fair:byteSize`, `fair:checksum`, `fair:compressFormat`).

## Utilities (`schema.py`)

- `is_fair_schema(schema)`: Tests whether a schema specifies the FAIR dialect URI or contains any `fair:` annotations. Accepts either dictionaries or `SchemaNode` instances.
- `extract_fair_annotations(schema_obj)`: Extracts all `fair:` annotations from a schema node into a `FAIRAnnotation` instance.
- `annotate_property(schema_node, ...)`: Pure functional helper that produces an enriched copy of a property or node dictionary with specified FAIR annotations.
