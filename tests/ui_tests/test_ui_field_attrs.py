from unittest.mock import patch

import pytest
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QListWidget

from nexus_constructor.field_attrs import FieldAttrsDialog, FieldAttrFrame
import numpy as np
from tests.helpers import file  # noqa: F401


@pytest.fixture(scope="function")
def field_attrs_dialog(qtbot):

    dialog = FieldAttrsDialog()
    qtbot.addWidget(dialog)
    return dialog


def get_attribute_widget(index: int, list_widget: QListWidget) -> FieldAttrFrame:
    item = list_widget.item(index)
    return list_widget.itemWidget(item)


@pytest.mark.parametrize("attr_val", ["test", 123, 1.1, np.ushort(12)])
def test_GIVEN_existing_field_with_attr_WHEN_editing_component_THEN_both_field_and_attrs_are_filled_in_correctly(
    qtbot, file, attr_val, field_attrs_dialog
):
    attr_key = "units"

    ds = file.create_dataset(name="test", data=123)
    ds.attrs[attr_key] = attr_val

    field_attrs_dialog.fill_existing_attrs(ds)

    assert len(field_attrs_dialog.get_attrs()) == 1
    assert field_attrs_dialog.get_attrs()[attr_key] == attr_val


def test_GIVEN_add_attribute_button_pressed_WHEN_changing_attributes_THEN_new_attribute_is_created(
    qtbot, field_attrs_dialog
):

    qtbot.mouseClick(field_attrs_dialog.add_button, Qt.LeftButton)
    assert field_attrs_dialog.list_widget.count() == 1


def test_GIVEN_remove_attribute_button_pressed_WHEN_changing_attributes_THEN_selected_attribute_is_removed(
    qtbot, field_attrs_dialog
):

    qtbot.mouseClick(field_attrs_dialog.add_button, Qt.LeftButton)
    qtbot.mouseClick(
        get_attribute_widget(0, field_attrs_dialog.list_widget), Qt.LeftButton
    )
    qtbot.mouseClick(field_attrs_dialog.remove_button, Qt.LeftButton)
    assert field_attrs_dialog.list_widget.count() == 0


def test_GIVEN_data_type_changes_WHEN_editing_component_THEN_validate_method_is_called(
    qtbot, field_attrs_dialog
):

    qtbot.mouseClick(field_attrs_dialog.add_button, Qt.LeftButton)
    widget = get_attribute_widget(0, field_attrs_dialog.list_widget)

    with patch(
        "nexus_constructor.field_attrs.FieldValueValidator.validate"
    ) as mock_validate:
        widget.attr_dtype_combo.setCurrentIndex(2)
        mock_validate.assert_called_once()


def test_GIVEN_edit_array_button_pressed_WHEN_attribute_is_an_array_THEN_array_widget_opens(
    qtbot, field_attrs_dialog
):

    qtbot.mouseClick(field_attrs_dialog.add_button, Qt.LeftButton)
    widget = get_attribute_widget(0, field_attrs_dialog.list_widget)
    widget.array_or_scalar_combo.setCurrentText("Array")

    qtbot.mouseClick(widget.array_edit_button, Qt.LeftButton)
    assert widget.dialog.isVisible()


def test_GIVEN_attribute_is_an_array_WHEN_getting_data_THEN_array_is_returned(
    qtbot, field_attrs_dialog
):

    qtbot.mouseClick(field_attrs_dialog.add_button, Qt.LeftButton)
    widget = get_attribute_widget(0, field_attrs_dialog.list_widget)
    widget.array_or_scalar_combo.setCurrentText("Array")

    data = np.arange(9).reshape((3, 3))
    qtbot.mouseClick(widget.array_edit_button, Qt.LeftButton)
    widget.dialog.model.array = data

    assert np.array_equal(widget.value, data)
