import pytest
import numpy as np
from mock import Mock, call

from nexus_constructor.geometry.disk_chopper.disk_chopper_geometry_creator import (
    Point,
    DiskChopperGeometryCreator,
    HALF_THICKNESS,
    ARROW_SIZE,
    RESOLUTION,
)

POINT_X = 2.0
POINT_Y = 3.0
POINT_Z = 4.0

R = np.sqrt(2)
THETA = np.deg2rad(45)


def create_list_of_ids(*points: Point):
    return [point.id for point in points]


@pytest.fixture(scope="function")
def point():
    return Point(POINT_X, POINT_Y, POINT_Z)


@pytest.fixture(scope="function")
def geometry_creator(chopper_details):
    return DiskChopperGeometryCreator(chopper_details)


@pytest.fixture(scope="module")
def resolution_array():
    return np.linspace(0, 2 * np.pi, 100 + 1)[:-1]


def expected_slit_boundary_face_points(center_to_slit_start: float, radius: float):
    """
    Creates for points that match the expected points for the face for the slit boundary. Assumes the slit edge has an
    angle of zero.
    :param center_to_slit_start: Distance from disk chopper center to the beginning of the slit.
    :param radius: The radius of the disk chopper.
    :return: Four points that should be roughly equal to the points for slit boundary face.
    """
    expected_upper_front = Point(radius, 0, HALF_THICKNESS)
    expected_lower_front = Point(center_to_slit_start, 0, HALF_THICKNESS)
    expected_upper_back = Point(radius, 0, -HALF_THICKNESS)
    expected_lower_back = Point(center_to_slit_start, 0, -HALF_THICKNESS)

    return (
        expected_lower_back,
        expected_lower_front,
        expected_upper_back,
        expected_upper_front,
    )


def create_two_points():
    """
    Create two points for testing the face connected to front/back centre methods.
    """
    first_point = Point(3, 4, 5)
    first_point.set_id(10)
    second_point = Point(6, 7, 8)
    second_point.set_id(11)

    return first_point, second_point


def test_GIVEN_three_values_WHEN_creating_point_THEN_point_is_initialised_correctly(
    point
):

    assert point.x == POINT_X
    assert point.y == POINT_Y
    assert point.z == POINT_Z
    assert point.id is None


def test_GIVEN_id_WHEN_point_has_no_id_THEN_id_is_set(point):

    id = 300
    point.set_id(id)
    assert point.id == id


def test_GIVEN_id_WHEN_point_already_has_id_THEN_id_doesnt_change(point):

    old_id = 200
    new_id = 300
    point.set_id(old_id)
    point.set_id(new_id)

    assert point.id == old_id


def test_GIVEN_non_integer_id_WHEN_setting_id_THEN_id_is_rejected(point):

    bad_id = "abc"
    point.set_id(bad_id)
    assert point.id is None


def test_GIVEN_point_WHEN_calling_point_to_qvector3d_THEN_expected_vector_is_created(
    point
):

    vector = point.point_to_qvector3d()
    assert vector.x() == POINT_X
    assert vector.y() == POINT_Y
    assert vector.z() == POINT_Z


def test_GIVEN_chopper_details_WHEN_initialising_geometry_creator_THEN_geometry_creator_is_initialised_with_expected_values(
    geometry_creator, chopper_details
):

    expected_z = HALF_THICKNESS

    assert geometry_creator.faces == []
    assert geometry_creator.z == expected_z
    assert geometry_creator.arrow_size == ARROW_SIZE
    assert geometry_creator.resolution == RESOLUTION

    assert geometry_creator._radius == chopper_details.radius
    assert np.array_equal(geometry_creator._slit_edges, chopper_details.slit_edges)
    assert geometry_creator._slit_height == chopper_details.slit_height

    assert len(geometry_creator.points) == 2

    expected_points = [Point(0, 0, expected_z), Point(0, 0, -expected_z)]

    for i in range(2):
        assert geometry_creator.points[i] == expected_points[i]


def test_GIVEN_polar_coordinates_WHEN_converting_polar_to_cartesian_THEN_expected_values_are_returned(
    geometry_creator
):
    x, y = geometry_creator._polar_to_cartesian_2d(R, THETA)
    assert abs(x - 1) < 1e-05
    assert abs(y - 1) < 1e-05


def test_GIVEN_polar_coordinates_WHEN_creating_mirrored_points_THEN_expected_points_are_returned(
    geometry_creator
):

    expected_first_point = Point(1.0, 1.0, HALF_THICKNESS)
    expected_second_point = Point(1.0, 1.0, -HALF_THICKNESS)

    actual_first_point, actual_second_point = geometry_creator._create_mirrored_points(
        R, THETA
    )
    assert actual_first_point == expected_first_point
    assert actual_second_point == expected_second_point


def test_GIVEN_face_should_look_right_WHEN_creating_and_adding_point_set_THEN_expected_face_is_created_with_expected_order(
    geometry_creator
):
    radius = 1
    center_to_slit_start = 0.5
    slit_edge = 0
    right_facing = False

    # Create the expected points
    expected_lower_back, expected_lower_front, expected_upper_back, expected_upper_front = expected_slit_boundary_face_points(
        center_to_slit_start, radius
    )

    # Call the create and add point set method
    actual_upper_front, actual_upper_back, actual_lower_front, actual_lower_back = geometry_creator.create_and_add_point_set(
        radius, center_to_slit_start, slit_edge, right_facing
    )

    # Check that the return points match the expected points
    assert expected_upper_front == actual_upper_front
    assert expected_lower_front == actual_lower_front
    assert expected_upper_back == actual_upper_back
    assert expected_lower_back == actual_lower_back

    # Check that the points have been added to the list
    assert actual_upper_front in geometry_creator.points
    assert actual_lower_front in geometry_creator.points
    assert actual_upper_back in geometry_creator.points
    assert actual_lower_back in geometry_creator.points

    # Check that the face created from the four points has the expected winding order
    expected_winding_order = create_list_of_ids(
        actual_lower_front, actual_upper_front, actual_upper_back, actual_lower_back
    )
    assert expected_winding_order == geometry_creator.faces[-1]


def test_GIVEN_face_should_look_left_WHEN_creating_and_adding_point_set_THEN_expected_face_is_created_with_expected_point_order(
    geometry_creator
):
    radius = 1
    center_to_slit_start = 0.5
    slit_edge = 0
    right_facing = True

    # Create the expected points
    expected_lower_back, expected_lower_front, expected_upper_back, expected_upper_front = expected_slit_boundary_face_points(
        center_to_slit_start, radius
    )

    # Call the create and add point set method
    actual_upper_front, actual_upper_back, actual_lower_front, actual_lower_back = geometry_creator.create_and_add_point_set(
        radius, center_to_slit_start, slit_edge, right_facing
    )

    # Check that the return points match the expected points
    assert expected_upper_front == actual_upper_front
    assert expected_lower_front == actual_lower_front
    assert expected_upper_back == actual_upper_back
    assert expected_lower_back == actual_lower_back

    # Check that the points have been added to the list
    assert actual_upper_front in geometry_creator.points
    assert actual_lower_front in geometry_creator.points
    assert actual_upper_back in geometry_creator.points
    assert actual_lower_back in geometry_creator.points

    # Check that the face created from the four points has the expected winding order
    expected_winding_order = create_list_of_ids(
        actual_lower_back, actual_upper_back, actual_upper_front, actual_lower_front
    )

    assert expected_winding_order == geometry_creator.faces[-1]


def test_GIVEN_r_and_theta_WHEN_creating_and_adding_mirrored_points_THEN_expected_points_are_created_and_added_to_list(
    geometry_creator
):

    r = 20
    theta = 0

    expected_front_point = Point(r, 0, HALF_THICKNESS)
    expected_back_point = Point(r, 0, -HALF_THICKNESS)

    actual_front_point, actual_back_point = geometry_creator.create_and_add_mirrored_points(
        r, theta
    )

    assert expected_front_point == actual_front_point
    assert expected_back_point == actual_back_point

    assert actual_front_point in geometry_creator.points
    assert actual_back_point in geometry_creator.points


def test_GIVEN_points_WHEN_adding_face_connected_to_front_centre_THEN_expected_face_is_created(
    geometry_creator
):

    first_point, second_point = create_two_points()
    geometry_creator.add_face_connected_to_front_centre([first_point, second_point])

    expected_face = create_list_of_ids(
        geometry_creator.front_centre, first_point, second_point
    )
    assert expected_face == geometry_creator.faces[-1]


def test_GIVEN_points_WHEN_adding_face_connected_to_back_centre_THEN_expected_face_is_created(
    geometry_creator
):

    first_point, second_point = create_two_points()
    geometry_creator.add_face_connected_to_back_centre([first_point, second_point])

    expected_face = create_list_of_ids(
        geometry_creator.back_centre, first_point, second_point
    )
    assert expected_face == geometry_creator.faces[-1]


def test_GIVEN_point_WHEN_adding_point_to_list_THEN_point_is_added_and_assigned_an_id(
    geometry_creator
):

    point = Point(1, 2, 3)
    geometry_creator._add_point_to_list(point)

    assert point in geometry_creator.points
    assert point.id == len(geometry_creator.points) - 1


def test_GIVEN_set_of_points_WHEN_adding_face_to_list_THEN_list_of_ids_is_added_to_list_of_faces(
    geometry_creator
):

    num_points = 3
    points = []
    ids = []

    for i in range(num_points):
        ids.append(i + 2)
        points.append(Point(i, i, i))
        points[-1].set_id(ids[-1])

    geometry_creator.add_face_to_list(points)
    assert ids in geometry_creator.faces


def test_GIVEN_length_of_arrow_position_WHEN_adding_top_dead_centre_arrow_THEN_expected_arrow_is_created(
    geometry_creator
):

    length_of_arrow_position = 5

    expected_centre_point = Point(length_of_arrow_position, 0, HALF_THICKNESS)
    expected_left_point = Point(
        length_of_arrow_position - geometry_creator.arrow_size,
        0,
        HALF_THICKNESS + geometry_creator.arrow_size,
    )
    expected_right_point = Point(
        length_of_arrow_position + geometry_creator.arrow_size,
        0,
        HALF_THICKNESS + geometry_creator.arrow_size,
    )

    geometry_creator.add_top_dead_centre_arrow(length_of_arrow_position)

    assert geometry_creator.points[-3] == expected_centre_point
    assert geometry_creator.points[-2] == expected_right_point
    assert geometry_creator.points[-1] == expected_left_point

    expected_face = create_list_of_ids(
        *[geometry_creator.points[i] for i in range(-3, 0)]
    )
    assert expected_face in geometry_creator.faces


def test_GIVEN_second_angle_greater_than_first_angle_THEN_intermediate_angles_method_returns_array_with_values_between_the_two_angles(
    geometry_creator, resolution_array
):

    first_angle = 0.5
    second_angle = 1.5

    trimmed_array = geometry_creator.get_intermediate_angle_values_from_resolution_array(
        resolution_array, first_angle, second_angle
    )

    assert all(trimmed_array > first_angle)
    assert all(trimmed_array < second_angle)

    diff = np.diff(trimmed_array) >= 0
    assert np.all(diff)


def test_GIVEN_first_angle_greater_than_second_angle_THEN_intermediate_angles_method_returns_array_with_values_between_the_two_angles(
    geometry_creator, resolution_array
):

    first_angle = 1.5
    second_angle = 0.5

    trimmed_array = geometry_creator.get_intermediate_angle_values_from_resolution_array(
        resolution_array, first_angle, second_angle
    )

    diff = np.diff(trimmed_array)
    split_index = np.where(diff < 0)[0][0]
    assert not np.all(diff >= 0)

    first_chunk = trimmed_array[: split_index + 1]
    second_chunk = trimmed_array[split_index + 1 :]

    assert all(first_chunk > first_angle)
    assert all(second_chunk < second_angle)


def test_GIVEN_resolution_of_one_WHEN_creating_resolution_angles_THEN_array_only_contains_zero(
    geometry_creator
):

    resolution = 1
    resolution_array = geometry_creator.create_resolution_angles(resolution)
    assert np.array_equal(np.zeros(1), resolution_array)


def test_GIVEN_resolution_greater_than_one_WHEN_creating_resolution_angles_THEN_array_contains_expected_values(
    geometry_creator
):

    resolution = 5
    resolution_array = geometry_creator.create_resolution_angles(resolution)
    expected = np.array([i * ((np.pi * 2) / resolution) for i in range(resolution)])

    assert len(resolution_array) == resolution
    assert np.array_equal(expected, resolution_array)


def test_GIVEN_angle_distance_to_centre_and_two_points_WHEN_creating_wedge_shape_THEN_expected_faces_and_points_are_created(
    geometry_creator
):

    theta = np.pi
    r = 10
    prev_back, prev_front = geometry_creator.create_and_add_mirrored_points(r, theta)
    current_back, current_front = geometry_creator.create_cake_slice(
        theta, prev_back, prev_front, r
    )

    assert current_front == Point(-r, 0, geometry_creator.z)
    assert current_back == Point(-r, 0, -geometry_creator.z)

    assert geometry_creator.faces[-3] == create_list_of_ids(
        prev_front, prev_back, current_back, current_front
    )

    assert geometry_creator.faces[-2] == create_list_of_ids(
        geometry_creator.front_centre, prev_front, current_front
    )

    assert geometry_creator.faces[-1] == create_list_of_ids(
        geometry_creator.back_centre, current_back, prev_back
    )


def test_GIVEN_slit_boundaries_WHEN_creating_intermediate_points_and_faces_THEN_expected_points_and_faces_are_created(
    geometry_creator
):

    # Choose angles for the boundaries of the slit edge
    first_angle = np.deg2rad(80)
    second_angle = np.deg2rad(100)

    # Set a middle angle
    middle_angle = np.deg2rad(90)

    # Set the length of the vertices
    r = 10

    # Create the points for the boundaries of the slit edges
    first_front, first_back = geometry_creator.create_and_add_mirrored_points(
        r, first_angle
    )
    second_front, second_back = geometry_creator.create_and_add_mirrored_points(
        r, second_angle
    )

    # Create a fake set of resolution angles with zero between the first and second angle
    geometry_creator.resolution_angles = np.array(
        [first_angle, middle_angle, second_angle]
    )

    # Call the method for creating the intermediate points and faces
    geometry_creator.create_intermediate_points_and_faces(
        first_angle, second_angle, first_front, first_back, second_front, second_back, r
    )

    # The expected intermediate points should have a distance from the centres of r, an angle of 90 degrees and be
    # separated by 2 * z
    expected_intermediate_front = Point(0, r, geometry_creator.z)
    expected_intermediate_back = Point(0, r, -geometry_creator.z)

    # Check that the last two points that were created in the geometry creator match what was expected
    actual_intermediate_front = geometry_creator.points[-2]
    actual_intermediate_back = geometry_creator.points[-1]

    assert actual_intermediate_front == expected_intermediate_front
    assert actual_intermediate_back == expected_intermediate_back

    # Check that the expected faces were created
    assert geometry_creator.faces[-6] == create_list_of_ids(
        first_front, first_back, actual_intermediate_back, actual_intermediate_front
    )

    assert geometry_creator.faces[-5] == create_list_of_ids(
        geometry_creator.front_centre, first_front, actual_intermediate_front
    )

    assert geometry_creator.faces[-4] == create_list_of_ids(
        geometry_creator.back_centre, actual_intermediate_back, first_back
    )

    assert geometry_creator.faces[-3] == create_list_of_ids(
        actual_intermediate_front, actual_intermediate_back, second_back, second_front
    )

    assert geometry_creator.faces[-2] == create_list_of_ids(
        geometry_creator.front_centre, actual_intermediate_front, second_front
    )

    assert geometry_creator.faces[-1] == create_list_of_ids(
        geometry_creator.back_centre, second_back, actual_intermediate_back
    )


def test_GIVEN_range_of_resolution_angles_contains_zero_WHEN_creating_intermediate_points_and_faces_THEN_top_dead_centre_arrow_is_created(
    geometry_creator
):

    # Choose the angles for the boundaries of the slit edge
    first_angle = np.deg2rad(350)
    second_angle = np.deg2rad(10)

    # Choose a middle angle of 0
    middle_angle = 0

    # Set the length of the vertices
    r = 10

    # Create the points for the boundaries of the slit edges
    first_front, first_back = geometry_creator.create_and_add_mirrored_points(
        r, first_angle
    )
    second_front, second_back = geometry_creator.create_and_add_mirrored_points(
        r, second_angle
    )

    # Create a fake set of resolution angles with zero between the first and second angle
    geometry_creator.resolution_angles = np.array(
        [first_angle, middle_angle, second_angle]
    )

    # Mock the top dead centre arrow method
    geometry_creator.add_top_dead_centre_arrow = Mock()

    # Call the method for creating the intermediate points and faces
    geometry_creator.create_intermediate_points_and_faces(
        first_angle, second_angle, first_front, first_back, second_front, second_back, r
    )

    # Check that the top dead centre method was called with the expected argument
    geometry_creator.add_top_dead_centre_arrow.assert_called_once_with(r)


def test_GIVEN_single_slit_WHEN_converting_chopper_details_to_OFF_THEN_first_set_of_points_are_created_correctly(
    geometry_creator, point
):

    # Create a slit edges array
    angles = [np.deg2rad(30 + i * 20) for i in range(4)]
    geometry_creator._slit_edges = np.array(angles)

    # Calculate distance between centre and bottom of the slit
    centre_to_slit_bottom = geometry_creator._radius - geometry_creator._slit_height

    # Create a mock for the create and add point set method
    mock_create_and_add_point_set = Mock(return_value=(point, point, point, point))
    geometry_creator.create_and_add_point_set = mock_create_and_add_point_set
    geometry_creator.create_intermediate_points_and_faces = Mock()

    geometry_creator.convert_chopper_details_to_off()

    # Check that the calls to create the points for the faces that make up the slit boundaries have been made in the
    # expected order
    expected_calls = [
        call(geometry_creator._radius, centre_to_slit_bottom, angles[i], bool(i % 2))
        for i in range(4)
    ]
    mock_create_and_add_point_set.assert_has_calls(expected_calls)