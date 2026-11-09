# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2026-11-09

### Added
- Integrated Pydantic models based on the latest `fair-data-schema` specification:
  - `SchemaNode`: Core recursive model covering JSON Schema Draft 2020-12 and all FAIR annotations.
  - `DatasetSchema`: Root dataset schema with `$schema` dialect resolution and I/O helpers (`from_dict`, `from_json`, `from_file`, `to_file`).
  - Helper models: `TemporalCoverage`, `DatasetRelation`, `ChecksumObject`, `LinkDescriptionObject`.
  - Type aliases: `I18nString`, `I18nText`, `JsonType`.
- Modernized `FAIRAnnotation` to Pydantic `BaseModel` supporting all 42 FAIR vocabulary annotation properties and dynamic extensions.
- Expanded test suite covering schema serialization, deserialization, i18n metadata, and helper structures.

### Changed
- Renamed project from `dartfx-fairdataschema` to `fairschema-toolkit` (`dartfx-fairschema`).
- Added `pydantic>=2.10.0` to project dependencies.
