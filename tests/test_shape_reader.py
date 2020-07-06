from typing import List

import pytest
from mock import Mock

from nexus_constructor.json.shape_reader import ShapeReader
from nexus_constructor.model.component import Component, OFF_GEOMETRY_NX_CLASS
from tests.shape_json import off_shape_json

COMPONENT_NAME = "ComponentName"

component_shape = dict()


def getitem(name):
    return component_shape[name]


def setitem(name, val):
    component_shape[name] = val


@pytest.fixture(scope="function")
def mock_component():
    mock_component = Mock(spec=Component)
    mock_component.name = COMPONENT_NAME
    set_item_mock = Mock()
    set_item_mock.side_effect = setitem
    get_item_mock = Mock()
    get_item_mock.side_effect = getitem
    mock_component.__setitem__ = set_item_mock
    mock_component.__getitem__ = get_item_mock
    return mock_component


@pytest.fixture(scope="function")
def off_shape_reader(off_shape_json, mock_component) -> ShapeReader:
    return ShapeReader(mock_component, off_shape_json)


def _any_warning_message_has_substrings(
    sub_strings: List[str], warning_messages: str
) -> bool:
    return any(
        [
            all([substring in warning_message for substring in sub_strings])
            for warning_message in warning_messages
        ]
    )


def test_GIVEN_off_shape_WHEN_reading_shape_information_THEN_error_and_issue_messages_have_expected_content(
    off_shape_reader,
):
    off_shape_reader.add_shape_to_component()

    for message in [off_shape_reader.error_message, off_shape_reader.issue_message]:
        assert OFF_GEOMETRY_NX_CLASS in message
        assert OFF_GEOMETRY_NX_CLASS in message


def test_GIVEN_unrecognised_shape_WHEN_reading_shape_information_THEN_warning_message_is_created(
    off_shape_reader, off_shape_json
):
    n_warnings = len(off_shape_reader.warnings)

    off_shape_json["attributes"][0]["values"] = bad_geometry_type = "NotAValidGeometry"
    off_shape_reader.add_shape_to_component()

    assert len(off_shape_reader.warnings) == n_warnings + 1
    assert _any_warning_message_has_substrings(
        [bad_geometry_type], off_shape_reader.warnings
    )


def test_GIVEN_no_attributes_field_WHEN_reading_shape_information_THEN_warning_message_is_created(
    off_shape_reader, off_shape_json
):

    n_warnings = len(off_shape_reader.warnings)

    del off_shape_json["attributes"]
    off_shape_reader.add_shape_to_component()

    assert len(off_shape_reader.warnings) == n_warnings + 1
    assert "''" in off_shape_reader.warnings[-1]


def test_GIVEN_missing_children_attribute_WHEN_reading_off_information_THEN_warning_message_is_created(
    off_shape_reader, off_shape_json
):
    n_warnings = len(off_shape_reader.warnings)

    del off_shape_json["children"]
    off_shape_reader.add_shape_to_component()

    assert len(off_shape_reader.warnings) == n_warnings + 1
    assert _any_warning_message_has_substrings(
        [
            off_shape_reader.error_message,
            "Unable to find children list in shape group.",
        ],
        off_shape_reader.warnings,
    )


def test_GIVEN_missing_name_WHEN_reading_off_information_THEN_warning_message_is_created_and_substitute_name_is_used(
    off_shape_reader, off_shape_json, mock_component
):
    n_warnings = len(off_shape_reader.warnings)

    del off_shape_json["name"]
    off_shape_reader.add_shape_to_component()

    assert len(off_shape_reader.warnings) == n_warnings + 1
    assert mock_component["shape"].name == "shape"


def test_GIVEN_children_is_not_a_list_WHEN_reading_off_information_THEN_warning_message_is_created(
    off_shape_reader, off_shape_json
):
    n_warnings = len(off_shape_reader.warnings)

    off_shape_json["children"] = "NotAList"
    off_shape_reader.add_shape_to_component()

    assert len(off_shape_reader.warnings) == n_warnings + 1
    assert _any_warning_message_has_substrings(
        [
            off_shape_reader.error_message,
            "Children attribute in shape group is not a list.",
        ],
        off_shape_reader.warnings,
    )


@pytest.mark.parametrize("attribute_to_remove", ["faces", "vertices", "winding_order"])
def test_GIVEN_cant_find_attribute_WHEN_reading_off_information_THEN_warning_message_is_created(
    off_shape_reader, off_shape_json, attribute_to_remove
):
    n_warnings = len(off_shape_reader.warnings)

    attribute = off_shape_reader._get_shape_dataset_from_list(
        attribute_to_remove, off_shape_json["children"]
    )
    off_shape_json["children"].remove(attribute)

    off_shape_reader.add_shape_to_component()

    assert len(off_shape_reader.warnings) == n_warnings + 1
    assert _any_warning_message_has_substrings(
        [attribute_to_remove, off_shape_reader.error_message], off_shape_reader.warnings
    )


def test_GIVEN_faces_type_value_is_not_int_WHEN_checking_type_THEN_issue_message_is_created(
    off_shape_reader, off_shape_json
):
    n_warnings = len(off_shape_reader.warnings)

    faces_dataset = off_shape_reader._get_shape_dataset_from_list(
        "faces", off_shape_json["children"]
    )

    faces_dataset["dataset"]["type"] = "double"
    off_shape_reader.add_shape_to_component()

    assert len(off_shape_reader.warnings) == n_warnings + 1
    assert _any_warning_message_has_substrings(
        [
            off_shape_reader.issue_message,
            "Type attribute for faces does not match expected type int.",
        ],
        off_shape_reader.warnings,
    )


def test_GIVEN_unable_to_find_type_value_WHEN_checking_type_THEN_issue_message_is_created(
    off_shape_reader, off_shape_json
):
    n_warnings = len(off_shape_reader.warnings)

    faces_dataset = off_shape_reader._get_shape_dataset_from_list(
        "faces", off_shape_json["children"]
    )

    del faces_dataset["dataset"]["type"]
    off_shape_reader.add_shape_to_component()

    assert len(off_shape_reader.warnings) == n_warnings + 1
    assert _any_warning_message_has_substrings(
        [off_shape_reader.issue_message, "Unable to find type attribute for faces."],
        off_shape_reader.warnings,
    )


def test_GIVEN_unable_to_find_type_dataset_WHEN_checking_type_THEN_issue_message_is_created(
    off_shape_reader, off_shape_json
):
    n_warnings = len(off_shape_reader.warnings)

    faces_dataset = off_shape_reader._get_shape_dataset_from_list(
        "faces", off_shape_json["children"]
    )

    del faces_dataset["dataset"]
    off_shape_reader.add_shape_to_component()

    assert len(off_shape_reader.warnings) > n_warnings
    assert _any_warning_message_has_substrings(
        [off_shape_reader.issue_message, "Unable to find type attribute for faces."],
        off_shape_reader.warnings,
    )


def test_GIVEN_missing_faces_values_attribute_WHEN_finding_faces_indices_list_THEN_error_message_is_created(
    off_shape_reader, off_shape_json
):
    n_warnings = len(off_shape_reader.warnings)

    faces_dataset = off_shape_reader._get_shape_dataset_from_list(
        "faces", off_shape_json["children"]
    )

    del faces_dataset["values"]
    off_shape_reader.add_shape_to_component()

    assert len(off_shape_reader.warnings) == n_warnings + 1
    assert _any_warning_message_has_substrings(
        [
            off_shape_reader.error_message,
            "Unable to find faces starting indices list in faces dataset.",
        ],
        off_shape_reader.warnings,
    )


def test_GIVEN_faces_values_attribute_is_not_a_list_WHEN_finding_faces_indices_list_THEN_error_message_is_created(
    off_shape_reader, off_shape_json
):
    n_warnings = len(off_shape_reader.warnings)

    faces_dataset = off_shape_reader._get_shape_dataset_from_list(
        "faces", off_shape_json["children"]
    )

    faces_dataset["values"] = True
    off_shape_reader.add_shape_to_component()

    assert len(off_shape_reader.warnings) == n_warnings + 1
    assert _any_warning_message_has_substrings(
        [
            off_shape_reader.error_message,
            "Faces starting indices attribute is not a list.",
        ],
        off_shape_reader.warnings,
    )
