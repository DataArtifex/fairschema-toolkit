"""Data models and helper classes for FAIR Data JSON Schema.

This module provides Pydantic models for the FAIR Data JSON Schema dialect.
It covers the full JSON Schema Draft 2020-12 vocabulary plus all FAIR extension
annotations defined in https://highvaluedata.net/fair-data-schema.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

#: A string or a BCP-47 language-mapped dict, e.g. {"en": "Age", "fr": "Âge"}.
I18nString = str | dict[str, str]

#: A Markdown-formatted string or a language-mapped dict of Markdown strings.
I18nText = str | dict[str, str]

#: Valid JSON Schema ``type`` values.
JsonType = Literal["string", "integer", "number", "boolean", "array", "object", "null"]


# ---------------------------------------------------------------------------
# Helper models (generated from inline object definitions in the vocab)
# ---------------------------------------------------------------------------


class TemporalCoverage(BaseModel):
    """Time period covered by the dataset (``fair:temporalCoverage``)."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")
    description: I18nString | None = Field(None)
    start: str | None = Field(None, description="ISO date string")
    end: str | None = Field(None, description="ISO date string")


class DatasetRelation(BaseModel):
    """One relationship entry within ``fair:datasetRelations``."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")
    relation_type: str = Field(alias="relationType")
    target_ref: str = Field(alias="targetRef")
    source_variables: list[str] | None = Field(None, alias="sourceVariables")
    target_variables: list[str] | None = Field(None, alias="targetVariables")
    cardinality: str | None = Field(None)
    description: I18nString | None = Field(None)


class ChecksumObject(BaseModel):
    """Bit-level checksum (aligned with RDA PID Kernel spdx:checksum / etag)."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")
    algorithm: str | None = Field(default="SHA256")
    algorithm_ref: str | None = Field(
        default="http://spdx.org/rdf/terms#checksumAlgorithm_sha256", alias="algorithmRef"
    )
    value: str = Field(...)


class LinkDescriptionObject(BaseModel):
    """Link to a dataset distribution or API endpoint (RFC 8288 / Hyper-Schema)."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")
    href: str = Field(...)
    rel: I18nString = Field(...)
    rel_ref: str | None = Field(None, alias="relRef")
    target_media_type: str | None = Field(None, alias="targetMediaType")
    target_schema: Any | None = Field(None, alias="targetSchema")
    title: I18nString | None = Field(None)
    description: I18nText | None = Field(None)
    fair_byte_size: int | None = Field(None, alias="fair:byteSize")
    fair_checksum: ChecksumObject | None = Field(None, alias="fair:checksum")
    fair_compress_format: str | None = Field(None, alias="fair:compressFormat")


# ---------------------------------------------------------------------------
# FAIRAnnotation — focused FAIR metadata model
# ---------------------------------------------------------------------------


class FAIRAnnotation(BaseModel):
    """Represents FAIR metadata annotations extracted from or to be added to a JSON Schema object."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    resource_type: str | None = Field(None, alias="fair:resourceType")
    concept_ref: str | None = Field(None, alias="fair:conceptRef")
    concept: I18nString | None = Field(None, alias="fair:concept")
    label: I18nString | None = Field(None, alias="fair:label")
    description: I18nText | None = Field(None, alias="fair:description")
    identifiers: list[Any] | None = Field(None, alias="fair:identifiers")
    version: I18nString | None = Field(None, alias="fair:version")
    checksum: ChecksumObject | None = Field(None, alias="fair:checksum")
    dataset_relations: list[DatasetRelation] | None = Field(None, alias="fair:datasetRelations")
    contributors: list[dict[str, Any]] | None = Field(None, alias="fair:contributors")
    provider: I18nString | None = Field(None, alias="fair:provider")
    provider_ref: str | None = Field(None, alias="fair:providerRef")
    license: I18nString | None = Field(None, alias="fair:license")
    license_ref: str | None = Field(None, alias="fair:licenseRef")
    temporal_coverage: TemporalCoverage | None = Field(None, alias="fair:temporalCoverage")
    temporal_coverage_ref: str | None = Field(None, alias="fair:temporalCoverageRef")
    spatial_coverage: I18nString | None = Field(None, alias="fair:spatialCoverage")
    spatial_coverage_ref: str | None = Field(None, alias="fair:spatialCoverageRef")
    population: I18nString | None = Field(None, alias="fair:population")
    population_ref: str | None = Field(None, alias="fair:populationRef")
    structure_type: str | None = Field(None, alias="fair:structureType")
    quality: list[dict[str, Any]] | None = Field(None, alias="fair:quality")
    classification: I18nString | None = Field(None, alias="fair:classification")
    classification_ref: list[Any] | None = Field(None, alias="fair:classificationRef")
    measurement_unit: I18nString | None = Field(None, alias="fair:measurementUnit")
    measurement_unit_ref: str | None = Field(None, alias="fair:measurementUnitRef")
    measurement_technique: I18nString | None = Field(None, alias="fair:measurementTechnique")
    measurement_technique_ref: str | None = Field(None, alias="fair:measurementTechniqueRef")
    quantity: I18nString | None = Field(None, alias="fair:quantity")
    quantity_ref: str | None = Field(None, alias="fair:quantityRef")
    measurement_scale: I18nString | None = Field(None, alias="fair:measurementScale")
    measurement_scale_ref: str | None = Field(None, alias="fair:measurementScaleRef")
    unit_type: I18nString | None = Field(None, alias="fair:unitType")
    unit_type_ref: str | None = Field(None, alias="fair:unitTypeRef")
    universe: I18nString | None = Field(None, alias="fair:universe")
    universe_ref: str | None = Field(None, alias="fair:universeRef")
    variable_ref: str | None = Field(None, alias="fair:variableRef")
    instance_variable_ref: str | None = Field(None, alias="fair:instanceVariableRef")
    represented_variable_ref: str | None = Field(None, alias="fair:representedVariableRef")
    conceptual_variable_ref: str | None = Field(None, alias="fair:conceptualVariableRef")
    sentinel: bool | None = Field(None, alias="fair:sentinel")
    clamped: bool | None = Field(None, alias="fair:clamped")
    byte_size: int | None = Field(None, alias="fair:byteSize")
    compress_format: str | None = Field(None, alias="fair:compressFormat")

    def __init__(self, /, **data: Any):
        extra_data = data.pop("extra", None)
        super().__init__(**data)
        if extra_data and isinstance(extra_data, dict):
            if self.__pydantic_extra__ is None:
                self.__pydantic_extra__ = {}
            self.__pydantic_extra__.update(extra_data)

    @property
    def extra(self) -> dict[str, Any]:
        """Return any extra unmodeled fields."""
        return self.__pydantic_extra__ or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert non-None FAIR annotations back into JSON-serializable dict using fair: keys."""
        return self.model_dump(by_alias=True, exclude_none=True)


# ---------------------------------------------------------------------------
# SchemaNode — core recursive class
# ---------------------------------------------------------------------------


class SchemaNode(BaseModel):
    """A node in a FAIR-extended JSON Schema document.

    Covers the full JSON Schema Draft 2020-12 vocabulary (all seven vocabularies
    declared in the FAIR dialect) plus FAIR annotation extensions.

    All FAIR extension fields use the ``fair_`` prefix to mirror the ``fair:``
    JSON prefix and to prevent any naming collision with standard JSON Schema
    keywords, both present and future.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    # ── JSON Schema: core ────────────────────────────────────────────────────
    id: str | None = Field(None, alias="$id")
    ref: str | None = Field(None, alias="$ref")
    anchor: str | None = Field(None, alias="$anchor")
    defs: dict[str, SchemaNode] | None = Field(None, alias="$defs")
    vocabulary: dict[str, bool] | None = Field(None, alias="$vocabulary")
    comment: str | None = Field(None, alias="$comment")

    # ── JSON Schema: meta-data ───────────────────────────────────────────────
    title: str | None = None
    description: str | None = None
    default: Any = None
    deprecated: bool | None = None
    read_only: bool | None = Field(None, alias="readOnly")
    write_only: bool | None = Field(None, alias="writeOnly")
    examples: list[Any] | None = None
    links: list[LinkDescriptionObject] | None = None

    # ── JSON Schema: validation ──────────────────────────────────────────────
    type: JsonType | list[JsonType] | None = None
    enum: list[Any] | None = None
    const: Any = None
    minimum: int | float | None = None
    maximum: int | float | None = None
    exclusive_minimum: int | float | None = Field(None, alias="exclusiveMinimum")
    exclusive_maximum: int | float | None = Field(None, alias="exclusiveMaximum")
    multiple_of: int | float | None = Field(None, alias="multipleOf")
    min_length: int | None = Field(None, alias="minLength")
    max_length: int | None = Field(None, alias="maxLength")
    pattern: str | None = None
    min_items: int | None = Field(None, alias="minItems")
    max_items: int | None = Field(None, alias="maxItems")
    unique_items: bool | None = Field(None, alias="uniqueItems")
    min_contains: int | None = Field(None, alias="minContains")
    max_contains: int | None = Field(None, alias="maxContains")
    required: list[str] | None = None
    dependent_required: dict[str, list[str]] | None = Field(None, alias="dependentRequired")
    min_properties: int | None = Field(None, alias="minProperties")
    max_properties: int | None = Field(None, alias="maxProperties")

    # ── JSON Schema: applicator ──────────────────────────────────────────────
    properties: dict[str, SchemaNode] | None = None
    pattern_properties: dict[str, SchemaNode] | None = Field(None, alias="patternProperties")
    additional_properties: SchemaNode | bool | None = Field(None, alias="additionalProperties")
    items: SchemaNode | None = None
    prefix_items: list[SchemaNode] | None = Field(None, alias="prefixItems")
    contains: SchemaNode | None = None
    all_of: list[SchemaNode] | None = Field(None, alias="allOf")
    any_of: list[SchemaNode] | None = Field(None, alias="anyOf")
    one_of: list[SchemaNode] | None = Field(None, alias="oneOf")
    not_: SchemaNode | None = Field(None, alias="not")
    if_: SchemaNode | None = Field(None, alias="if")
    then: SchemaNode | None = None
    else_: SchemaNode | None = Field(None, alias="else")

    # ── JSON Schema: unevaluated ─────────────────────────────────────────────
    unevaluated_properties: SchemaNode | bool | None = Field(None, alias="unevaluatedProperties")
    unevaluated_items: SchemaNode | bool | None = Field(None, alias="unevaluatedItems")

    # ── JSON Schema: format-annotation ──────────────────────────────────────
    format: str | None = None

    # ── JSON Schema: content ─────────────────────────────────────────────────
    content_encoding: str | None = Field(None, alias="contentEncoding")
    content_media_type: str | None = Field(None, alias="contentMediaType")
    content_schema: SchemaNode | None = Field(None, alias="contentSchema")

    # ── FAIR annotations (generated from vocab/annotations) ──────────────────
    fair_resource_type: str | None = Field(None, alias="fair:resourceType")
    fair_concept_ref: str | None = Field(None, alias="fair:conceptRef")
    fair_concept: I18nString | None = Field(None, alias="fair:concept")
    fair_label: I18nString | None = Field(None, alias="fair:label")
    fair_description: I18nText | None = Field(None, alias="fair:description")
    fair_identifiers: list[Any] | None = Field(None, alias="fair:identifiers")
    fair_version: I18nString | None = Field(None, alias="fair:version")
    fair_checksum: ChecksumObject | None = Field(None, alias="fair:checksum")
    fair_dataset_relations: list[DatasetRelation] | None = Field(None, alias="fair:datasetRelations")
    fair_contributors: list[dict[str, Any]] | None = Field(None, alias="fair:contributors")
    fair_provider: I18nString | None = Field(None, alias="fair:provider")
    fair_provider_ref: str | None = Field(None, alias="fair:providerRef")
    fair_license: I18nString | None = Field(None, alias="fair:license")
    fair_license_ref: str | None = Field(None, alias="fair:licenseRef")
    fair_temporal_coverage: TemporalCoverage | None = Field(None, alias="fair:temporalCoverage")
    fair_temporal_coverage_ref: str | None = Field(None, alias="fair:temporalCoverageRef")
    fair_spatial_coverage: I18nString | None = Field(None, alias="fair:spatialCoverage")
    fair_spatial_coverage_ref: str | None = Field(None, alias="fair:spatialCoverageRef")
    fair_population: I18nString | None = Field(None, alias="fair:population")
    fair_population_ref: str | None = Field(None, alias="fair:populationRef")
    fair_structure_type: str | None = Field(None, alias="fair:structureType")
    fair_quality: list[dict[str, Any]] | None = Field(None, alias="fair:quality")
    fair_classification: I18nString | None = Field(None, alias="fair:classification")
    fair_classification_ref: list[Any] | None = Field(None, alias="fair:classificationRef")
    fair_measurement_unit: I18nString | None = Field(None, alias="fair:measurementUnit")
    fair_measurement_unit_ref: str | None = Field(None, alias="fair:measurementUnitRef")
    fair_measurement_technique: I18nString | None = Field(None, alias="fair:measurementTechnique")
    fair_measurement_technique_ref: str | None = Field(None, alias="fair:measurementTechniqueRef")
    fair_quantity: I18nString | None = Field(None, alias="fair:quantity")
    fair_quantity_ref: str | None = Field(None, alias="fair:quantityRef")
    fair_measurement_scale: I18nString | None = Field(None, alias="fair:measurementScale")
    fair_measurement_scale_ref: str | None = Field(None, alias="fair:measurementScaleRef")
    fair_unit_type: I18nString | None = Field(None, alias="fair:unitType")
    fair_unit_type_ref: str | None = Field(None, alias="fair:unitTypeRef")
    fair_universe: I18nString | None = Field(None, alias="fair:universe")
    fair_universe_ref: str | None = Field(None, alias="fair:universeRef")
    fair_variable_ref: str | None = Field(None, alias="fair:variableRef")
    fair_instance_variable_ref: str | None = Field(None, alias="fair:instanceVariableRef")
    fair_represented_variable_ref: str | None = Field(None, alias="fair:representedVariableRef")
    fair_conceptual_variable_ref: str | None = Field(None, alias="fair:conceptualVariableRef")
    fair_sentinel: bool | None = Field(None, alias="fair:sentinel")
    fair_clamped: bool | None = Field(None, alias="fair:clamped")

    # ── Helpers ──────────────────────────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a FAIR JSON Schema dict (``fair:`` prefixed keys, no nulls)."""
        return self.model_dump(by_alias=True, exclude_none=True)

    def to_json(self, indent: int = 2) -> str:
        """Serialise to a FAIR JSON Schema string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @property
    def fair_annotations(self) -> FAIRAnnotation:
        """Extract all fair: annotations from this node into a FAIRAnnotation instance."""
        data = self.model_dump(by_alias=True, exclude_none=True)
        fair_dict = {k: v for k, v in data.items() if k.startswith("fair:")}
        return FAIRAnnotation.model_validate(fair_dict)


# Self-referential resolution required after class definition.
SchemaNode.model_rebuild()


# ---------------------------------------------------------------------------
# DatasetSchema — root-level schema
# ---------------------------------------------------------------------------


class DatasetSchema(SchemaNode):
    """Root-level FAIR dataset schema.

    Extends :class:`SchemaNode` with a ``$schema`` declaration that defaults
    to the FAIR dialect URI for version *dev*.
    """

    fair_schema: str = Field(
        default="https://highvaluedata.net/fair-data-schema/dev",
        alias="$schema",
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DatasetSchema:
        """Parse a FAIR schema from a plain dictionary."""
        return cls.model_validate(data)

    @classmethod
    def from_json(cls, text: str) -> DatasetSchema:
        """Parse a FAIR schema from a JSON string."""
        return cls.from_dict(json.loads(text))

    @classmethod
    def from_file(cls, path: str | Path) -> DatasetSchema:
        """Load and parse a FAIR schema from a JSON file."""
        return cls.from_json(Path(path).read_text(encoding="utf-8"))

    def to_file(self, path: str | Path, indent: int = 2) -> None:
        """Write this schema to a JSON file."""
        Path(path).write_text(self.to_json(indent=indent), encoding="utf-8")
