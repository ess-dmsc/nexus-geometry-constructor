from PySide2.QtGui import QVector3D, QMatrix4x4
from nexus_constructor.unit_converter import calculate_unit_conversion_factor
from math import sin, cos, pi, acos, degrees
import h5py
from nexus_constructor.nexus import nexus_wrapper as nx
from nexus_constructor.nexus.validation import (
    NexusFormatError,
    ValidateDataset,
    validate_group,
)
from typing import List, TypeVar


# Temporary method here until the one above is no longer needed
def validate_nonzero_qvector(value: QVector3D):
    if value.x() == 0 and value.y() == 0 and value.z() == 0:
        raise ValueError("Vector is zero length")


class OFFGeometry:
    """
    Stores arbitrary 3D geometry as a list of vertices and faces, based on the Object File Format

    vertices:   list of Vector objects used as corners of polygons in the geometry
    faces:  list of integer lists. Each sublist is a winding path around the corners of a polygon. Each sublist item is
            an index into the vertices list to identify a specific point in 3D space
    """

    geometry_str = "OFF"

    def __init__(
        self,
        vertices: List[QVector3D] = None,
        faces: List[List[int]] = None,
        units: str = "",
        file_path: str = "",
    ):
        self.vertices = vertices
        self.faces = faces

        # Source units and file path are retained only for the purpose of populating the edit component window
        # with the options previously chosen by the user
        self.units = units
        self.file_path = file_path

    @property
    def winding_order(self):
        return [point for face in self.faces for point in face]

    @property
    def winding_order_indices(self):
        face_sizes = [len(face) for face in self.faces]
        return [sum(face_sizes[0:i]) for i in range(len(face_sizes))]

    @property
    def off_geometry(self):
        return self


OFFCube = OFFGeometry(
    vertices=[
        QVector3D(-0.5, -0.5, 0.5),
        QVector3D(0.5, -0.5, 0.5),
        QVector3D(-0.5, 0.5, 0.5),
        QVector3D(0.5, 0.5, 0.5),
        QVector3D(-0.5, 0.5, -0.5),
        QVector3D(0.5, 0.5, -0.5),
        QVector3D(-0.5, -0.5, -0.5),
        QVector3D(0.5, -0.5, -0.5),
    ],
    faces=[
        [0, 1, 3, 2],
        [2, 3, 5, 4],
        [4, 5, 7, 6],
        [6, 7, 1, 0],
        [1, 7, 5, 3],
        [6, 0, 2, 4],
    ],
)


class NoShapeGeometry:
    """
    Dummy object for components with no geometry.
    """

    geometry_str = "None"

    def __init__(self):
        pass

    @property
    def off_geometry(self):
        return OFFCube


class CylindricalGeometry:
    """
    Describes the shape of a cylinder in 3D space

    The cylinder is assumed to have the center of its base located at the origin of the local coordinate system, and is
    described by the direction of its axis, its height, and radius.
    """

    geometry_str = "Cylinder"

    def __init__(self, nexus_file: nx.NexusWrapper, group: h5py.Group):
        self.file = nexus_file
        self.group = group
        self._verify_in_file()

    def _verify_in_file(self):
        """
        Check all the datasets and attributes we require are in the NXcylindrical_geometry group
        """
        problems = []
        if "NX_class" in self.group.attrs.items:
            if self.group.attrs["NX_class"] != "NXcylindrical_geometry":
                problems.append(
                    f"Expected {self.group.name} to have NX_class attribute of NXcylindrical_geometry"
                )
        else:
            problems.append(f"Expected {self.group.name} to have an NX_class attribute")
        if problems:
            raise NexusFormatError("\n".join(problems))

        problems = validate_group(
            self.group,
            (
                ValidateDataset(
                    "vertices", shape=(None, 3), attributes={"units": None}
                ),
                ValidateDataset("cylinders", (None, 3)),
            ),
        )
        if problems:
            raise NexusFormatError("\n".join(problems))

    @property
    def units(self):
        return self.group["vertices"].attrs["units"]

    @units.setter
    def units(self, new_units: str):
        self.group["vertices"].attrs["units"] = new_units

    def __init__(
        self,
        units: str = "m",
        axis_direction: QVector3D = QVector3D(1, 0, 0),
        height: float = 1,
        radius: float = 1,
    ):
        validate_nonzero_qvector(axis_direction)
        self.units = units
        self.axis_direction = axis_direction
        self.height = height
        self.radius = radius

    @property
    def base_center_point(self):
        return QVector3D(0, 0, 0)

    @property
    def base_edge_point(self):
        # rotate a point on the edge of a Z axis aligned cylinder by the rotation matrix
        return (
            QVector3D(self.radius * calculate_unit_conversion_factor(self.units), 0, 0)
            * self.rotation_matrix
        )

    @property
    def top_center_point(self):
        return (
            self.axis_direction.normalized()
            * self.height
            * calculate_unit_conversion_factor(self.units)
        )

    @property
    def off_geometry(self, steps=20):
        unit_conversion_factor = calculate_unit_conversion_factor(self.units)

        # A list of vertices describing the circle at the bottom of the cylinder
        bottom_circle = [
            QVector3D(sin(2 * pi * i / steps), cos(2 * pi * i / steps), 0) * self.radius
            for i in range(steps)
        ]

        # The top of the cylinder is the bottom shifted upwards
        top_circle = [vector + QVector3D(0, 0, self.height) for vector in bottom_circle]

        # The true cylinder are all vertices from the unit cylinder multiplied by the conversion factor
        vertices = [
            vector * unit_conversion_factor for vector in bottom_circle + top_circle
        ]

        # rotate each vertex to produce the desired cylinder mesh
        rotate_matrix = self.rotation_matrix
        vertices = [vector * rotate_matrix for vector in vertices]

        def vertex_above(vertex):
            """
            Returns the index of the vertex above this one in the cylinder.
            """
            return vertex + steps

        def next_vertex(vertex):
            """
            Returns the next vertex around in the top or bottom circle of the cylinder.
            """
            return (vertex + 1) % steps

        # Rectangular faces joining the top and bottom
        rectangle_faces = [
            [i, vertex_above(i), vertex_above(next_vertex(i)), next_vertex(i)]
            for i in range(steps)
        ]

        # Step sided shapes describing the top and bottom
        # The bottom uses steps of -1 to preserve winding order
        top_bottom_faces = [
            [i for i in range(steps)],
            [i for i in range((2 * steps) - 1, steps - 1, -1)],
        ]

        return OFFGeometry(vertices=vertices, faces=rectangle_faces + top_bottom_faces)

    @property
    def rotation_matrix(self):
        """
        :return: A QMatrix4x4 describing the rotation from the Z axis to the cylinder's axis
        """
        default_axis = QVector3D(0, 0, 1)
        desired_axis = self.axis_direction.normalized()
        rotate_axis = QVector3D.crossProduct(desired_axis, default_axis)
        rotate_radians = acos(QVector3D.dotProduct(desired_axis, default_axis))
        rotate_matrix = QMatrix4x4()
        rotate_matrix.rotate(degrees(rotate_radians), rotate_axis)
        return rotate_matrix


GeometryType = TypeVar(
    "GeometryType", CylindricalGeometry, NoShapeGeometry, OFFGeometry
)
