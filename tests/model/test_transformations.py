import numpy as np
from PySide2.QtGui import QVector3D

from nexus_constructor.model.component import Component
from nexus_constructor.model.dataset import Dataset
from nexus_constructor.model.transformation import Transformation
from nexus_constructor.model.value_type import ValueTypes


def create_transform(
    name="test translation",
    ui_value=42.0,
    vector=QVector3D(1.0, 0.0, 0.0),
    type="Translation",
    values=Dataset(name="", values=None, type=ValueTypes.DOUBLE, size=[1]),
):

    translation = Transformation(
        name=name,
        parent_node=None,
        values=values,
        type=ValueTypes.STRING,
        parent_component=None,
        size=[1],
    )

    translation.vector = vector
    translation.transform_type = type
    translation.ui_value = ui_value

    return translation


def test_can_get_transform_properties():

    test_name = "slartibartfast"
    test_ui_value = 42
    test_vector = QVector3D(1.0, 0.0, 0.0)
    test_type = "Translation"
    test_values = Dataset("test_dataset", None, [1])

    transform = create_transform(
        name=test_name, vector=test_vector, ui_value=test_ui_value, values=test_values
    )

    assert (
        transform.name == test_name
    ), "Expected the transform name to match what was in the NeXus file"
    assert (
        transform.ui_value == test_ui_value
    ), "Expected the transform value to match what was in the NeXus file"
    assert (
        transform.vector == test_vector
    ), "Expected the transform vector to match what was in the NeXus file"
    assert (
        transform.transform_type == test_type
    ), "Expected the transform type to match what was in the NeXus file"
    assert (
        transform.values == test_values
    ), "Expected the transform type to match what was in the NeXus file"


def test_ui_value_for_transform_with_array_magnitude_returns_first_value():
    transform_name = "transform1"
    array = [1.1, 2.2, 3.3]
    transform_ui_value = np.asarray(array, dtype=float)

    transformation = create_transform(name=transform_name, ui_value=transform_ui_value)

    assert transformation.ui_value == array[0]


def test_ui_value_for_transform_with_array_magnitude_of_strings_returns_zero():
    transform_name = "transform1"
    array = ["a1", "b1", "c1"]
    transform_ui_value = np.asarray(array)

    transformation = create_transform(name=transform_name, ui_value=transform_ui_value)
    assert transformation.ui_value == 0


def test_can_set_transform_properties():

    initial_name = "slartibartfast"

    transform = create_transform(initial_name)

    test_name = "beeblebrox"
    test_ui_value = 34.0
    test_vector = QVector3D(0.0, 0.0, 1.0)
    test_type = "Rotation"
    test_values = Dataset("valuedataset", None, [1, 2])

    transform.name = test_name
    transform.ui_value = test_ui_value
    transform.vector = test_vector
    transform.transform_type = test_type
    transform.values = test_values

    assert (
        transform.name == test_name
    ), "Expected the transform name to match what was in the NeXus file"
    assert (
        transform.ui_value == test_ui_value
    ), "Expected the transform value to match what was in the NeXus file"
    assert (
        transform.vector == test_vector
    ), "Expected the transform vector to match what was in the NeXus file"
    assert (
        transform.transform_type == test_type
    ), "Expected the transform type to match what was in the NeXus file"
    assert (
        transform.values == test_values
    ), "Expected the transform type to match what was in the NeXus file"


def test_set_one_dependent():

    transform1 = create_transform("transform_1")
    transform2 = create_transform("transform_2")

    transform1.register_dependent(transform2)

    set_dependents = transform1.dependents

    assert len(set_dependents) == 1
    assert set_dependents[0] == transform2


def test_set_two_dependents():

    transform1 = create_transform("transform_1")
    transform2 = create_transform("transform_2")
    transform3 = create_transform("transform_3")

    transform1.register_dependent(transform2)
    transform1.register_dependent(transform3)

    set_dependents = transform1.dependents

    assert len(set_dependents) == 2
    assert set_dependents[0] == transform2
    assert set_dependents[1] == transform3


def test_set_three_dependents():

    transform1 = create_transform("transform_1")
    transform2 = create_transform("transform_2")
    transform3 = create_transform("transform_3")
    transform4 = create_transform("transform_4")

    transform1.register_dependent(transform2)
    transform1.register_dependent(transform3)
    transform1.register_dependent(transform4)

    set_dependents = transform1.dependents

    assert len(set_dependents) == 3
    assert set_dependents[0] == transform2
    assert set_dependents[1] == transform3
    assert set_dependents[2] == transform4


def test_deregister_dependent():

    transform1 = create_transform("transform_1")
    transform2 = create_transform("transform_2")

    transform1.register_dependent(transform2)
    transform1.deregister_dependent(transform2)

    set_dependents = transform1.dependents

    assert not set_dependents


def test_deregister_unregistered_dependent_alt1():

    transform1 = create_transform("transform_1")
    transform2 = create_transform("transform_2")

    transform1.deregister_dependent(transform2)

    assert not transform1.dependents


def test_deregister_unregistered_dependent_alt2():

    transform1 = create_transform("transform_1")
    transform2 = create_transform("transform_2")
    transform3 = create_transform("transform_3")

    transform1.register_dependent(transform3)
    transform1.deregister_dependent(transform2)

    assert len(transform1.dependents) == 1
    assert transform1.dependents[0] == transform3


def test_deregister_unregistered_dependent_alt3():

    transform1 = create_transform("transform_1")
    transform2 = create_transform("transform_2")
    transform3 = create_transform("transform_2_alt")
    transform4 = create_transform("transform_3")

    transform1.register_dependent(transform3)
    transform1.register_dependent(transform4)
    transform1.deregister_dependent(transform2)

    assert len(transform1.dependents) == 2
    assert transform1.dependents[0] == transform3
    assert transform1.dependents[1] == transform4


def test_reregister_dependent():

    transform1 = create_transform("transform_1")
    transform2 = create_transform("transform_2")
    transform3 = create_transform("transform_3")

    transform1.register_dependent(transform2)
    transform1.deregister_dependent(transform2)
    transform1.register_dependent(transform3)

    set_dependents = transform1.dependents

    assert len(set_dependents) == 1
    assert set_dependents[0] == transform3


def test_set_one_dependent_component():

    transform = create_transform("transform_1")
    component = Component("test_component")
    transform.register_dependent(component)

    set_dependents = transform.dependents

    assert len(set_dependents) == 1
    assert set_dependents[0] == component


def test_set_two_dependent_components():

    transform = create_transform("transform_1")

    component1 = Component("component1")
    component2 = Component("component2")

    transform.register_dependent(component1)
    transform.register_dependent(component2)

    set_dependents = transform.dependents

    assert len(set_dependents) == 2
    assert set_dependents[0] == component1
    assert set_dependents[1] == component2


def test_set_three_dependent_components():

    transform = create_transform("transform_1")

    component1 = Component("test_component1")
    component2 = Component("test_component2")
    component3 = Component("test_component3")

    transform.register_dependent(component1)
    transform.register_dependent(component2)
    transform.register_dependent(component3)

    set_dependents = transform.dependents

    assert len(set_dependents) == 3
    assert set_dependents[0] == component1
    assert set_dependents[1] == component2
    assert set_dependents[2] == component3


def test_deregister_three_dependent_components():

    transform = create_transform("transform_1")

    component1 = Component("test_component1")
    component2 = Component("test_component2")
    component3 = Component("test_component3")

    transform.register_dependent(component1)
    transform.register_dependent(component2)
    transform.register_dependent(component3)

    transform.deregister_dependent(component1)
    transform.deregister_dependent(component2)
    transform.deregister_dependent(component3)

    set_dependents = transform.dependents

    assert len(set_dependents) == 0


def test_register_dependent_twice():

    transform = create_transform("transform_1")
    component1 = Component("test_component1")

    transform.register_dependent(component1)
    transform.register_dependent(component1)

    set_dependents = transform.dependents

    assert len(set_dependents) == 1


def test_can_get_translation_as_4_by_4_matrix():

    test_ui_value = 42.0
    # Note, it should not matter if this is not set to a unit vector
    test_vector = QVector3D(2.0, 0.0, 0.0)
    test_type = "Translation"

    transformation = create_transform(
        ui_value=test_ui_value, vector=test_vector, type=test_type
    )

    test_matrix = transformation.qmatrix
    # NB, -1 * distance because the transformation in the UI is a passive transformation
    expected_matrix = np.array(
        (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, -1 * test_ui_value, 0, 0, 1)
    )
    assert np.allclose(expected_matrix, np.array(test_matrix.data()))


def test_can_get_rotation_as_4_by_4_matrix():

    test_ui_value = 15.0  # degrees
    test_vector = QVector3D(0.0, 1.0, 0.0)  # around y-axis
    test_type = "Rotation"

    transformation = create_transform(
        ui_value=test_ui_value, vector=test_vector, type=test_type
    )

    test_matrix = transformation.qmatrix
    # for a rotation around the y-axis:
    test_value_radians = np.deg2rad(test_ui_value)
    expected_matrix = np.array(
        (
            np.cos(test_value_radians),
            0,
            np.sin(test_value_radians),
            0,
            0,
            1,
            0,
            0,
            -np.sin(test_value_radians),
            0,
            np.cos(test_value_radians),
            0,
            0,
            0,
            0,
            1,
        )
    )
    assert np.allclose(expected_matrix, np.array(test_matrix.data()), atol=1.0e-7)


def test_GIVEN_transformation_with_scalar_value_that_is_not_castable_to_int_WHEN_getting_ui_value_THEN_ui_placeholder_value_is_returned_instead():
    transform_name = "transform_1"
    transform = create_transform(transform_name)

    str_value = "sdfji"
    transform.ui_value = str_value

    assert transform.ui_value != str_value
    assert transform.ui_value == 0
