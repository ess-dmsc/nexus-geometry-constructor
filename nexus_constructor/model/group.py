from typing import List, Any, Union

import attr

from nexus_constructor.common_attrs import CommonAttrs
from nexus_constructor.model.attribute import FieldAttribute
from nexus_constructor.model.dataset import DatasetMetadata, Dataset
from nexus_constructor.model.node import Node, _get_item, _set_item
import numpy as np


@attr.s
class Group(Node):
    """
    Base class for any group which has a set of children and an nx_class attribute.
    """

    children = attr.ib(factory=list, init=False)
    type = attr.ib(type=str, default="group", init=False)
    attributes = attr.ib(type=List[FieldAttribute], factory=list, init=False)

    def __getitem__(self, key: str):
        return _get_item(self.children, key)

    def __setitem__(self, key: str, value: Union["Group", Dataset]):
        _set_item(self.children, key, value)

    @property
    def nx_class(self):
        return self.get_attribute_value(CommonAttrs.NX_CLASS)

    @nx_class.setter
    def nx_class(self, new_nx_class: str):
        self.set_attribute_value(
            CommonAttrs.NX_CLASS, new_nx_class,
        )

    def set_field_value(self, name: str, value: Any, dtype: str = None):
        size = [1]
        if isinstance(value, (np.ndarray, np.generic)):
            size = value.size
        self[name] = Dataset(name, DatasetMetadata(size, dtype), value)

    def get_field_value(self, name: str):
        return self[name].values