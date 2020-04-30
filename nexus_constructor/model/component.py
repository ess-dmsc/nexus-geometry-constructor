from typing import Tuple, Union
from PySide2.Qt3DCore import Qt3DCore
from PySide2.QtGui import QMatrix4x4, QVector3D
from PySide2.QtWidgets import QListWidget

from nexus_constructor.common_attrs import CommonAttrs
from nexus_constructor.component.component_shape import (
    PIXEL_SHAPE_GROUP_NAME,
    SHAPE_GROUP_NAME,
)
import attr
from nexus_constructor.model.group import Group
from nexus_constructor.model.node import _generate_incremental_name
from nexus_constructor.model.transformation import Transformation, TransformationGroup
from nexus_constructor.pixel_data import PixelGrid, PixelMapping
from nexus_constructor.pixel_data_to_nexus_utils import (
    get_detector_number_from_pixel_mapping,
    get_x_offsets_from_pixel_grid,
    get_y_offsets_from_pixel_grid,
    get_z_offsets_from_pixel_grid,
    get_detector_ids_from_pixel_grid,
    PIXEL_FIELDS,
)
from nexus_constructor.transformation_types import TransformationType
from nexus_constructor.ui_utils import show_warning_dialog


def _normalise(input_vector: QVector3D) -> Tuple[QVector3D, float]:
    """
    Normalise to unit vector

    :param input_vector: Input vector
    :return: Unit vector, magnitude
    """
    magnitude = input_vector.length()
    if magnitude == 0:
        return QVector3D(0.0, 0.0, 0.0), 0.0

    return input_vector.normalized(), magnitude


@attr.s
class Component(Group):
    """
    Base class for a component object. In the NeXus file this would translate to the component group.
    """

    @property
    def description(self):
        return self.get_field_value(CommonAttrs.DESCRIPTION)

    @description.setter
    def description(self, new_description: str):
        self.set_field_value(CommonAttrs.DESCRIPTION, new_description)

    @property
    def transform(self):
        """
        Creates a QTransform based on the full chain of transforms this component points to.
        :return: QTransform of final transformation
        """
        transform_matrix = QMatrix4x4()
        for transform in self.transforms_full_chain:
            transform_matrix *= transform.qmatrix
        transformation = Qt3DCore.QTransform()
        transformation.setMatrix(transform_matrix)
        return transformation

    @property
    def transforms(self):
        """
        Gets transforms in the depends_on chain but only those which are local to
        this component's group in the NeXus file
        :return:
        """
        raise NotImplementedError
        # transforms = TransformationsList(self)
        # depends_on = self.get_field(CommonAttrs.DEPENDS_ON)
        # self._get_transform(depends_on, transforms, local_only=True)
        # return transforms

    @property
    def transforms_full_chain(self):
        """
        Gets all transforms in the depends_on chain for this component
        :return: List of transforms
        """
        raise NotImplementedError
        # transforms = TransformationsList(self)
        # depends_on = self.get_field(CommonAttrs.DEPENDS_ON)
        # self._get_transform(depends_on, transforms)
        # return transforms

    def add_translation(
        self, vector: QVector3D, name: str = None, depends_on: Transformation = None
    ) -> Transformation:
        """
        Note, currently assumes translation is in metres
        :param vector: direction and magnitude of translation as a 3D vector
        :param name: name of the translation group (Optional)
        :param depends_on: existing transformation which the new one depends on (otherwise relative to origin)
        """
        unit_vector, magnitude = _normalise(vector)
        return self._create_transform(
            name,
            TransformationType.TRANSLATION,
            magnitude,
            "m",
            unit_vector,
            depends_on,
        )

    def add_rotation(
        self,
        axis: QVector3D,
        angle: float,
        name: str = None,
        depends_on: Transformation = None,
    ) -> Transformation:
        """
        Note, currently assumes angle is in degrees
        :param axis: axis
        :param angle:
        :param name: Name of the rotation group (Optional)
        :param depends_on: existing transformation which the new one depends on (otherwise relative to origin)
        """
        return self._create_transform(
            name, TransformationType.ROTATION, angle, "degrees", axis, depends_on
        )

    def _create_transform(
        self,
        name: str,
        transformation_type: TransformationType,
        angle_or_magnitude: float,
        units: str,
        vector: QVector3D,
        depends_on: Transformation,
    ):
        transforms_group = self.__create_transformations_group_if_does_not_exist()
        if name is None:
            name = _generate_incremental_name(transformation_type, transforms_group)
        transform = Transformation(name, angle_or_magnitude)
        transform.type = transformation_type
        transform.ui_value = angle_or_magnitude
        transform.units = units
        transform.vector = vector
        transform.depends_on = depends_on
        return transform

    def __create_transformations_group_if_does_not_exist(self) -> TransformationGroup:
        for item in self.children:
            if isinstance(item, TransformationGroup):
                return item
        group = TransformationGroup()
        self.children.append(group, name="transformations")
        return group

    @property
    def shape(self):
        raise NotImplementedError

    def remove_shape(self):
        raise NotImplementedError

    def set_off_shape(
        self, loaded_geometry, units: str = "", filename: str = "", pixel_data=None,
    ):
        raise NotImplementedError

    def set_cylinder_shape(
        self,
        axis_direction: QVector3D = QVector3D(0.0, 0.0, 1.0),
        height: float = 1.0,
        radius: float = 1.0,
        units: Union[str, bytes] = "m",
        pixel_data=None,
    ):
        raise NotImplementedError

    def create_shape_group(self, nx_class: str, shape_is_single_pixel: bool = False):
        if shape_is_single_pixel:
            self[PIXEL_SHAPE_GROUP_NAME] = Group(PIXEL_SHAPE_GROUP_NAME,)
            return self[PIXEL_SHAPE_GROUP_NAME]
            # nexus_name, self.group
            # )
            # self._shape = PixelShape(self.file, self.group)
        else:
            self[SHAPE_GROUP_NAME] = None
            return self[SHAPE_GROUP_NAME]
            # shape_group = self.file.create_nx_group(
            #     SHAPE_GROUP_NAME, nexus_name, self.group
            # )
            # self._shape = ComponentShape(self.file, self.group)

    def clear_pixel_data(self):
        for field_name in PIXEL_FIELDS:
            try:
                del self[field_name]
            except AttributeError:
                pass

    def record_pixel_grid(self, pixel_grid: PixelGrid):
        """
        Records the pixel grid data to the NeXus file.
        :param pixel_grid: The PixelGrid created from the input provided to the Add/Edit Component Window.
        """
        self.set_field_value(
            "x_pixel_offset", get_x_offsets_from_pixel_grid(pixel_grid), "float64"
        )
        self.set_field_value(
            "y_pixel_offset", get_y_offsets_from_pixel_grid(pixel_grid), "float64"
        )
        self.set_field_value(
            "z_pixel_offset", get_z_offsets_from_pixel_grid(pixel_grid), "float64"
        )
        self.set_field_value(
            "detector_number", get_detector_ids_from_pixel_grid(pixel_grid), "int64"
        )

    def record_pixel_mapping(self, pixel_mapping: PixelMapping):
        """
        Records the pixel mapping data to the NeXus file.
        :param pixel_mapping: The PixelMapping created from the input provided to the Add/Edit Component Window.
        """
        self.set_field_value(
            "detector_number",
            get_detector_number_from_pixel_mapping(pixel_mapping),
            "int64",
        )


def add_fields_to_component(component: Component, fields_widget: QListWidget):
    """
    Adds fields from a list widget to a component.
    :param component: Component to add the field to.
    :param fields_widget: The field list widget to extract field information such the name and value of each field.
    """
    for i in range(fields_widget.count()):
        widget = fields_widget.itemWidget(fields_widget.item(i))
        try:
            component[widget.name] = widget.value
        except ValueError as error:
            show_warning_dialog(
                f"Warning: field {widget.name} not added",
                title="Field invalid",
                additional_info=str(error),
                parent=fields_widget.parent().parent(),
            )