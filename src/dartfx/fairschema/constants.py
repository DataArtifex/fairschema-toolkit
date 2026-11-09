"""Constants and URI definitions for FAIR Data JSON Schema."""

FAIR_SCHEMA_DIALECT_URI: str = "https://highvaluedata.net/fair-data-schema"
FAIR_SCHEMA_DEV_DIALECT_URI: str = "https://highvaluedata.net/fair-data-schema/dev"
FAIR_PREFIX: str = "fair:"

RESOURCE_TYPES: tuple[str, ...] = ("data-product", "dataset", "variable")
STRUCTURE_TYPES: tuple[str, ...] = ("wide", "long", "dimensional", "key-value")

DEFAULT_CHECKSUM_ALGORITHM: str = "SHA256"
DEFAULT_CHECKSUM_ALGORITHM_REF: str = "http://spdx.org/rdf/terms#checksumAlgorithm_sha256"
