import json
from typing import Union, List

from PySide2.QtWidgets import QWidget

from nexus_constructor.component.component_type import COMPONENT_TYPES
from nexus_constructor.model.component import Component
from nexus_constructor.model.entry import Entry
from nexus_constructor.model.instrument import Instrument
from nexus_constructor.model.transformation import Transformation
from nexus_constructor.ui_utils import show_warning_dialog

NX_CLASS = "NX_class"
NX_INSTRUMENT = "NXinstrument"
NX_SAMPLE = "NXsample"
NX_TRANSFORMATION = "NXtransformation"


def _find_nx_class(entry: dict) -> str:
    """
    Attempts to find the NXclass of a component in the dictionary.
    :param entry: The dictionary containing the NXclass information for a given component.
    :return: The NXclass if it was able to find it, otherwise an empty string is returned.
    """
    if entry.get("name") == NX_CLASS:
        return entry.get("values")
    if entry.get(NX_CLASS):
        return entry.get(NX_CLASS)
    return ""


def _read_nx_class(entry: Union[list, dict]) -> str:
    """
    Attempts to determine the NXclass of a component in a list/dictionary.
    :param entry: A dictionary of list of a dictionary containing NXclass information.
    :return: The NXclass if it can be found, otherwise an emtpy string is returned.
    """
    if isinstance(entry, list):
        for item in entry:
            return _find_nx_class(item)
    elif isinstance(entry, dict):
        return _find_nx_class(entry)


def _contains_transformations(entry: dict) -> bool:
    """
    Determines if a component contains transformations.
    :param entry: Something...
    :return: True if the component has transformations, False otherwise.
    """
    attributes = entry.get("attributes")
    if not attributes:
        return False
    for attribute in attributes:
        if _read_nx_class(attribute) == NX_TRANSFORMATION:
            return True
    return False


def _retrieve_children_list(json_dict: dict) -> list:
    """
    Attempts to retrieve the children from the JSON dictionary.
    :param json_dict: The JSON dictionary loaded by the user.
    :return: The children value is returned if it was found, otherwise an empty list is returned.
    """
    try:
        entry = json_dict["nexus_structure"]["children"][0]
        return entry["children"]
    except (KeyError, IndexError, TypeError):
        return []


class TransformationReader:
    def __init__(self, parent_name: str, parent_component: Component, entry: list):
        self.parent_name = parent_name
        self.entry = entry

    def get_transformations(self):
        """
        Attempts to construct Transformation objects using information from the JSON structure.
        :return: A list of transformations if they were found, otherwise an empty list is returned.
        """
        if self.entry:
            for item in self.entry:
                if _contains_transformations(item):
                    return self._create_transformations(item.get("children"))
        return []

    def _create_transformations(
        self, json_transformations: list
    ) -> List[Transformation]:
        """
        Uses the information contained in the JSON dictionary to construct a list of Transformations.
        :param entry:
        :return:
        """
        transformations = []
        for json_transformation in json_transformations:
            name = json_transformation.get("name")
            value = json_transformation.get("values")
            dtype = json_transformation.get("dataset").get("type")

        return transformations


class JSONReader:
    def __init__(self, parent: QWidget):
        self.entry = Entry()
        self.entry.instrument = Instrument()
        self.parent = parent
        self.warnings = []

    def load_model_from_json(self, filename: str) -> bool:
        """
        Tries to load a model from a JSON file.
        :param filename: The filename of the JSON file.
        :return: True if the model was loaded without problems, False otherwise.
        """
        with open(filename, "r") as json_file:

            json_data = json_file.read()

            try:
                json_dict = json.loads(json_data)
            except ValueError as exception:
                show_warning_dialog(
                    "Provided file not recognised as valid JSON",
                    "Invalid JSON",
                    f"{exception}",
                    self.parent,
                )
                return False

            children_list = _retrieve_children_list(json_dict)

            if not children_list:
                show_warning_dialog(
                    "Provided file not recognised as valid Instrument",
                    "Invalid JSON",
                    parent=self.parent,
                )
                return False

            for child in children_list:
                self._read_json_object(
                    child, json_dict["nexus_structure"]["children"][0].get("name")
                )

            if self.warnings:
                show_warning_dialog(
                    "\n".join(self.warnings),
                    "Warnings encountered loading JSON",
                    parent=self.parent,
                )
                return True

            return True

    def _read_json_object(self, json_object: dict, parent_name: str = None):
        """
        Tries to create a component based on the contents of the JSON file.
        :param json_object:  A component from the JSON dictionary.
        """
        name = json_object.get("name")

        if name:

            nx_class = _read_nx_class(json_object.get("attributes"))

            if nx_class == NX_INSTRUMENT:
                return all(
                    [
                        self._read_json_object(child, name)
                        for child in json_object.get("children")
                    ]
                )

            if not self._validate_nx_class(name, nx_class):
                return

            if nx_class == NX_SAMPLE:
                component = self.entry.instrument.sample
                component.name = name
            else:
                component = Component(name)
                component.nx_class = nx_class
                self.entry.instrument.add_component(component)

            transformations = TransformationReader(
                name, component, json_object.get("children").get_transformations()
            )

            if transformations:
                pass

        else:
            self.warnings.append(
                f"Unable to find object name for child of {parent_name}."
            )

    def _validate_nx_class(self, name: str, nx_class: str) -> bool:
        """
        Validates the NXclass by checking if it was found, and if it matches known NXclasses for components.
        :param nx_class: The NXclass string obtained from the dictionary.
        :return: True if the NXclass is valid, False otherwise.
        """
        if not nx_class:
            self.warnings.append(f"Unable to determine NXclass of component {name}.")
            return False

        if nx_class not in COMPONENT_TYPES:
            return False

        return True
