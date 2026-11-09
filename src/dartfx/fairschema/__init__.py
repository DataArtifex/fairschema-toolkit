"""FAIR Schema Toolkit for Data Artifex ecosystem."""

from dartfx.fairschema.__about__ import __version__
from dartfx.fairschema.constants import (
    DEFAULT_CHECKSUM_ALGORITHM,
    DEFAULT_CHECKSUM_ALGORITHM_REF,
    FAIR_PREFIX,
    FAIR_SCHEMA_DEV_DIALECT_URI,
    FAIR_SCHEMA_DIALECT_URI,
    RESOURCE_TYPES,
    STRUCTURE_TYPES,
)
from dartfx.fairschema.models import (
    ChecksumObject,
    DatasetRelation,
    DatasetSchema,
    FAIRAnnotation,
    I18nString,
    I18nText,
    JsonType,
    LinkDescriptionObject,
    SchemaNode,
    TemporalCoverage,
)
from dartfx.fairschema.schema import annotate_property, extract_fair_annotations, is_fair_schema

__all__ = [
    "DEFAULT_CHECKSUM_ALGORITHM",
    "DEFAULT_CHECKSUM_ALGORITHM_REF",
    "FAIRAnnotation",
    "FAIR_PREFIX",
    "FAIR_SCHEMA_DEV_DIALECT_URI",
    "FAIR_SCHEMA_DIALECT_URI",
    "RESOURCE_TYPES",
    "STRUCTURE_TYPES",
    "ChecksumObject",
    "DatasetRelation",
    "DatasetSchema",
    "I18nString",
    "I18nText",
    "JsonType",
    "LinkDescriptionObject",
    "SchemaNode",
    "TemporalCoverage",
    "__version__",
    "annotate_property",
    "extract_fair_annotations",
    "is_fair_schema",
]
