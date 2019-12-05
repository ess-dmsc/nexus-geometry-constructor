import pytest
import numpy as np
from PySide2.QtCore import QModelIndex, Qt
from PySide2.QtWidgets import QWidget
from mock import Mock

from nexus_constructor.array_dataset_table_widget import ArrayDatasetTableWidget
from nexus_constructor.validators import DATASET_TYPE


@pytest.fixture(scope="function")
def template(qtbot):
    return QWidget()


@pytest.fixture(scope="function")
def array_dataset_table_widget(qtbot, template):
    array_dataset_table_widget = ArrayDatasetTableWidget()
    template.ui = array_dataset_table_widget
    qtbot.addWidget(template)
    return array_dataset_table_widget


@pytest.mark.parametrize("array_shape", [(6, 1), (1, 6), (6,), (6, 6)])
def test_UI_GIVEN_data_has_different_shapes_WHEN_getting_array_from_component_THEN_data_returns_correct_value(
    array_dataset_table_widget, array_shape
):

    model_index = Mock(spec=QModelIndex)
    last_value_x = array_shape[0] - 1
    model_index.row.return_value = last_value_x
    value_index = (last_value_x,)

    array_size = array_shape[0]

    if len(array_shape) > 1:
        array_size *= array_shape[1]
        last_value_y = array_shape[1] - 1
        model_index.column.return_value = last_value_y
        value_index = (last_value_x, last_value_y)

    array = np.arange(array_size).reshape(array_shape)
    array_dataset_table_widget.model.array = array

    assert array_dataset_table_widget.model.data(model_index, Qt.DisplayRole) == str(
        array[value_index]
    )


@pytest.mark.parametrize("orig_data_type", DATASET_TYPE.values())
@pytest.mark.parametrize("new_data_type", DATASET_TYPE.values())
def test_UI_GIVEN_data_type_WHEN_changing_data_type_THEN_change_is_successful(
    array_dataset_table_widget, orig_data_type, new_data_type
):

    array = np.arange(10, dtype=orig_data_type)
    array_dataset_table_widget.model.array = array
    array_dataset_table_widget.model.update_array_dtype(np.float16)

    assert np.array_equal(array, array_dataset_table_widget.model.array)


@pytest.mark.skip(
    "Don't actually know what causes the ValueError. All possible conversions appear to work."
)
def test_UI_GIVEN_array_cant_be_converted_WHEN_changing_data_type_THEN_array_resets(
    array_dataset_table_widget
):
    pass


def test_UI_GIVEN_add_row_button_pressed_THEN_array_size_changes(
    array_dataset_table_widget
):

    array_dataset_table_widget.add_row_button.trigger()
    assert array_dataset_table_widget.model.array.shape == (2, 1)


def test_UI_GIVEN_add_column_button_pressed_THEN_array_size_changes(
    array_dataset_table_widget
):

    array_dataset_table_widget.add_column_button.trigger()
    assert array_dataset_table_widget.model.array.shape == (1, 2)


def test_UI_GIVEN_remove_row_button_pressed_THEN_array_size_changes(
    array_dataset_table_widget
):
    pass
