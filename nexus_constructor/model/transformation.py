from typing import List

import attr
import numpy as np
from PySide2.Qt3DCore import Qt3DCore
from PySide2.QtGui import QVector3D, QMatrix4x4

from nexus_constructor.common_attrs import CommonAttrs
from nexus_constructor.model.dataset import Dataset
from nexus_constructor.transformation_types import TransformationType


@attr.s
class Transformation(Dataset):
    """
    Wrapper for an individual transformation. In the NeXus file this would be translated as a transformation dataset.
    """

    _dependents = attr.ib(factory=list, type=List["Transformation"])

    @property
    def type(self) -> str:
        return self.get_attribute_value(CommonAttrs.TRANSFORMATION_TYPE)

    @type.setter
    def type(self, new_type):
        self.set_attribute_value(CommonAttrs.TRANSFORMATION_TYPE, new_type)

    @property
    def vector(self) -> QVector3D:
        vector = self.get_attribute_value(CommonAttrs.VECTOR)
        return (
            QVector3D(vector[0], vector[1], vector[2]) if vector is not None else None
        )

    @vector.setter
    def vector(self, new_vector: QVector3D):
        vector_as_np_array = np.array([new_vector.x(), new_vector.y(), new_vector.z()])
        self.set_attribute_value(CommonAttrs.VECTOR, vector_as_np_array)

    @property
    def ui_value(self) -> float:

        if isinstance(self.dataset, Dataset):
            if np.isscalar(self.dataset.values):
                try:
                    self.ui_value = float(self.dataset.values)
                    return float(self.dataset.values)
                except ValueError:
                    pass
            else:
                try:
                    self.ui_value = float(self.dataset.values[0])
                    return float(self.dataset.values[0])
                except ValueError:
                    pass

        if self.get_attribute_value(CommonAttrs.UI_VALUE) is None:
            default_value = 0.0
            self.ui_value = 0.0
            return default_value

        return self.get_attribute_value(CommonAttrs.UI_VALUE)

    @ui_value.setter
    def ui_value(self, new_value: float):

        if np.isscalar(new_value):
            value = new_value
        else:
            value = new_value[0]
        try:
            self.set_attribute_value(CommonAttrs.UI_VALUE, float(value))
        except ValueError:
            self.set_attribute_value(CommonAttrs.UI_VALUE, 0.0)

    @property
    def qmatrix(self) -> QMatrix4x4:
        """
        Get a Qt3DCore.QTransform describing the transformation
        """
        transform = Qt3DCore.QTransform()
        if self.type == TransformationType.ROTATION:
            quaternion = transform.fromAxisAndAngle(self.vector, self.ui_value)
            transform.setRotation(quaternion)
        elif self.type == TransformationType.TRANSLATION:
            transform.setTranslation(self.vector.normalized() * self.ui_value)
        else:
            raise (RuntimeError(f'Unknown transformation of type "{self.type}".'))
        return transform.matrix()

    @property
    def units(self):
        return self.get_attribute_value(CommonAttrs.UNITS)

    @units.setter
    def units(self, new_units):
        self.set_attribute_value(CommonAttrs.UNITS, new_units)

    @property
    def depends_on(self) -> "Transformation":
        return self.get_attribute_value(CommonAttrs.DEPENDS_ON)

    @depends_on.setter
    def depends_on(self, new_depends_on: "Transformation"):
        self.set_attribute_value(CommonAttrs.DEPENDS_ON, new_depends_on)

    @property
    def dependents(self) -> List["Transformation"]:
        return self._dependents

    def deregister_dependent(self, old_dependent: "Transformation"):
        try:
            self._dependents.remove(old_dependent)
        except ValueError:
            pass

    def register_dependent(self, new_dependent: "Transformation"):
        if new_dependent not in self._dependents:
            self._dependents.append(new_dependent)

    def remove_from_dependee_chain(self):
        pass


def create_transformation(name: str, dataset: Dataset):
    return Transformation(name, dataset)
