from dartfx.fairschema import (
    DEFAULT_CHECKSUM_ALGORITHM,
    FAIR_SCHEMA_DEV_DIALECT_URI,
    FAIR_SCHEMA_DIALECT_URI,
    ChecksumObject,
    DatasetRelation,
    DatasetSchema,
    FAIRAnnotation,
    LinkDescriptionObject,
    SchemaNode,
    TemporalCoverage,
    annotate_property,
    extract_fair_annotations,
    is_fair_schema,
)


def test_is_fair_schema():
    dialect_schema = {"$schema": FAIR_SCHEMA_DIALECT_URI, "title": "Test Dataset"}
    assert is_fair_schema(dialect_schema) is True

    dev_dialect_schema = {"$schema": FAIR_SCHEMA_DEV_DIALECT_URI, "title": "Dev Dataset"}
    assert is_fair_schema(dev_dialect_schema) is True

    keyword_schema = {"type": "integer", "fair:label": "Observation Year"}
    assert is_fair_schema(keyword_schema) is True

    plain_schema = {"type": "string", "title": "Plain Field"}
    assert is_fair_schema(plain_schema) is False

    node = SchemaNode(title="SchemaNode test", fair_label="Test Node")
    assert is_fair_schema(node) is True


def test_extract_fair_annotations():
    node = {
        "type": "integer",
        "title": "Year",
        "fair:conceptRef": "https://www.wikidata.org/wiki/Q1993",
        "fair:concept": "Year",
        "fair:label": "Observation Year",
        "fair:customExtension": "value",
    }
    anno = extract_fair_annotations(node)
    assert anno.concept_ref == "https://www.wikidata.org/wiki/Q1993"
    assert anno.concept == "Year"
    assert anno.label == "Observation Year"
    assert anno.extra == {"fair:customExtension": "value"}


def test_annotate_property():
    prop = {"type": "number"}
    annotated = annotate_property(
        prop,
        label="Temperature",
        measurement_unit="deg_C",
        concept="Air Temperature",
        clamped=True,
        variable_ref="https://example.org/variables/temperature",
    )
    assert annotated["type"] == "number"
    assert annotated["fair:label"] == "Temperature"
    assert annotated["fair:measurementUnit"] == "deg_C"
    assert annotated["fair:concept"] == "Air Temperature"
    assert annotated["fair:clamped"] is True
    assert annotated["fair:variableRef"] == "https://example.org/variables/temperature"


def test_fair_annotation_to_dict():
    anno = FAIRAnnotation(label="Test", sentinel=True, clamped=False)
    d = anno.to_dict()
    assert d == {"fair:label": "Test", "fair:sentinel": True, "fair:clamped": False}


def test_fair_annotation_i18n():
    anno = FAIRAnnotation(
        label={"en": "Age", "fr": "Âge"},
        description={"en": "Age in years", "fr": "Âge en années"},
    )
    d = anno.to_dict()
    assert d["fair:label"] == {"en": "Age", "fr": "Âge"}
    assert d["fair:description"] == {"en": "Age in years", "fr": "Âge en années"}


def test_helper_models():
    tc = TemporalCoverage(start="2020-01-01", end="2020-12-31", description="Full Year 2020")
    assert tc.start == "2020-01-01"
    assert tc.end == "2020-12-31"

    rel = DatasetRelation(
        relationType="cites",
        targetRef="https://example.org/dataset/2",
        sourceVariables=["varA"],
        targetVariables=["varB"],
    )
    assert rel.relation_type == "cites"
    assert rel.target_ref == "https://example.org/dataset/2"
    assert rel.source_variables == ["varA"]

    cs = ChecksumObject(value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    assert cs.algorithm == DEFAULT_CHECKSUM_ALGORITHM
    assert cs.value.startswith("e3b0c4")

    link = LinkDescriptionObject(
        href="https://example.org/data.csv",
        rel="item",
        targetMediaType="text/csv",
        fair_byte_size=1024,
    )
    assert link.href == "https://example.org/data.csv"
    assert link.target_media_type == "text/csv"
    assert link.fair_byte_size == 1024


def test_schema_node_and_dataset_schema():
    temp_prop = SchemaNode(
        type="number",
        title="Temperature",
        fair_label="Observed Temperature",
        fair_measurement_unit="deg_C",
        fair_clamped=True,
    )
    schema = DatasetSchema(
        title="Weather Station Observations",
        description="Daily weather observations",
        properties={"temperature": temp_prop},
        fair_resource_type="dataset",
        fair_license="https://creativecommons.org/licenses/by/4.0/",
    )

    schema_dict = schema.to_dict()
    assert schema_dict["$schema"] == FAIR_SCHEMA_DEV_DIALECT_URI
    assert schema_dict["title"] == "Weather Station Observations"
    assert schema_dict["fair:resourceType"] == "dataset"
    assert schema_dict["fair:license"] == "https://creativecommons.org/licenses/by/4.0/"
    assert "temperature" in schema_dict["properties"]
    assert schema_dict["properties"]["temperature"]["fair:label"] == "Observed Temperature"
    assert schema_dict["properties"]["temperature"]["fair:clamped"] is True

    # Test roundtrip from dict
    restored = DatasetSchema.from_dict(schema_dict)
    assert restored.title == "Weather Station Observations"
    assert restored.fair_license == "https://creativecommons.org/licenses/by/4.0/"
    assert restored.properties is not None
    assert restored.properties["temperature"].fair_measurement_unit == "deg_C"

    # Test JSON roundtrip
    json_str = schema.to_json()
    from_json_schema = DatasetSchema.from_json(json_str)
    assert from_json_schema.title == restored.title

    # Test property fair_annotations
    annos = temp_prop.fair_annotations
    assert annos.label == "Observed Temperature"
    assert annos.measurement_unit == "deg_C"
    assert annos.clamped is True
