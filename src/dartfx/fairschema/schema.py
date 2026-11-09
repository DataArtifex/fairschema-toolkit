"""Core operations for inspecting, validating, and annotating FAIR Data JSON Schemas."""

from __future__ import annotations

from typing import Any

from dartfx.fairschema.constants import (
    FAIR_PREFIX,
    FAIR_SCHEMA_DEV_DIALECT_URI,
    FAIR_SCHEMA_DIALECT_URI,
)
from dartfx.fairschema.models import (
    FAIRAnnotation,
    I18nString,
    I18nText,
    SchemaNode,
)


def is_fair_schema(schema: dict[str, Any] | SchemaNode) -> bool:
    """Check whether a schema specifies the FAIR Data JSON Schema dialect URI or contains fair: annotations."""
    if isinstance(schema, SchemaNode):
        schema_dict = schema.to_dict()
    else:
        schema_dict = schema

    schema_uri = schema_dict.get("$schema", "")
    if schema_uri and (
        schema_uri == FAIR_SCHEMA_DIALECT_URI
        or schema_uri == FAIR_SCHEMA_DEV_DIALECT_URI
        or schema_uri.startswith(FAIR_SCHEMA_DIALECT_URI)
    ):
        return True

    return any(key.startswith(FAIR_PREFIX) for key in schema_dict)


def extract_fair_annotations(schema_obj: dict[str, Any] | SchemaNode) -> FAIRAnnotation:
    """Extract all fair: prefixed keywords from a property or root schema into a FAIRAnnotation instance."""
    if isinstance(schema_obj, SchemaNode):
        return schema_obj.fair_annotations

    fair_dict = {k: v for k, v in schema_obj.items() if k.startswith(FAIR_PREFIX)}
    return FAIRAnnotation.model_validate(fair_dict)


def annotate_property(
    schema_node: dict[str, Any] | SchemaNode,
    *,
    resource_type: str | None = None,
    label: I18nString | None = None,
    description: I18nText | None = None,
    concept: I18nString | None = None,
    concept_ref: str | None = None,
    measurement_unit: I18nString | None = None,
    measurement_unit_ref: str | None = None,
    measurement_technique: I18nString | None = None,
    measurement_technique_ref: str | None = None,
    quantity: I18nString | None = None,
    quantity_ref: str | None = None,
    measurement_scale: I18nString | None = None,
    measurement_scale_ref: str | None = None,
    unit_type: I18nString | None = None,
    unit_type_ref: str | None = None,
    universe: I18nString | None = None,
    universe_ref: str | None = None,
    variable_ref: str | None = None,
    instance_variable_ref: str | None = None,
    represented_variable_ref: str | None = None,
    conceptual_variable_ref: str | None = None,
    classification: I18nString | None = None,
    classification_ref: list[Any] | None = None,
    sentinel: bool | None = None,
    clamped: bool | None = None,
    byte_size: int | None = None,
    compress_format: str | None = None,
    **extra_annotations: Any,
) -> dict[str, Any]:
    """Return a new schema node dictionary enriched with specified fair: metadata annotations."""
    if isinstance(schema_node, SchemaNode):
        updated = schema_node.to_dict()
    else:
        updated = dict(schema_node)

    # Prefix any un-prefixed extra keyword args if needed
    normalized_extra: dict[str, Any] = {}
    for k, v in extra_annotations.items():
        prefix_key = k if k.startswith(FAIR_PREFIX) else f"{FAIR_PREFIX}{k}"
        normalized_extra[prefix_key] = v

    annotation = FAIRAnnotation(
        resource_type=resource_type,
        label=label,
        description=description,
        concept=concept,
        concept_ref=concept_ref,
        measurement_unit=measurement_unit,
        measurement_unit_ref=measurement_unit_ref,
        measurement_technique=measurement_technique,
        measurement_technique_ref=measurement_technique_ref,
        quantity=quantity,
        quantity_ref=quantity_ref,
        measurement_scale=measurement_scale,
        measurement_scale_ref=measurement_scale_ref,
        unit_type=unit_type,
        unit_type_ref=unit_type_ref,
        universe=universe,
        universe_ref=universe_ref,
        variable_ref=variable_ref,
        instance_variable_ref=instance_variable_ref,
        represented_variable_ref=represented_variable_ref,
        conceptual_variable_ref=conceptual_variable_ref,
        classification=classification,
        classification_ref=classification_ref,
        sentinel=sentinel,
        clamped=clamped,
        byte_size=byte_size,
        compress_format=compress_format,
        **normalized_extra,
    )
    updated.update(annotation.to_dict())
    return updated
