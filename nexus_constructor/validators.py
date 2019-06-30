"""Validators to be used on QML input fields"""
from PySide2.QtCore import Signal, QObject
from PySide2.QtGui import QValidator
import pint
import os
from typing import List


class UnitValidator(QValidator):
    """
    Validator to ensure the the text entered is a valid unit of length.
    """

    def __init__(self):
        super().__init__()
        self.ureg = pint.UnitRegistry()

    def validate(self, input: str, pos: int):

        # Attempt to convert the string argument to a unit
        try:
            unit = self.ureg(input)
        except (
            pint.errors.UndefinedUnitError,
            AttributeError,
            pint.compat.tokenize.TokenError,
        ):
            self.is_valid.emit(False)
            return QValidator.Intermediate

        # Attempt to find 1 metre in terms of the unit. This will ensure that it's a length.
        try:
            self.ureg.metre.from_(unit)
        except (pint.errors.DimensionalityError, ValueError):
            self.is_valid.emit(False)
            return QValidator.Intermediate

        # Reject input in the form of "2 metres," "40 cm," etc
        if unit.magnitude != 1:
            self.is_valid.emit(False)
            return QValidator.Intermediate

        self.is_valid.emit(True)
        return QValidator.Acceptable

    is_valid = Signal(bool)


class NameValidator(QValidator):
    """
    Validator to ensure item names are unique within a model that has a 'name' property

    The validationFailed signal is emitted if an entered name is not unique.
    """

    def __init__(self, list_model: List):
        super().__init__()
        self.list_model = list_model

    def validate(self, input: str, pos: int):
        if not input:
            self.is_valid.emit(False)
            return QValidator.Intermediate

        names_in_list = [item.name for item in self.list_model]
        if input in names_in_list:
            self.is_valid.emit(False)
            return QValidator.Intermediate

        self.is_valid.emit(True)
        return QValidator.Acceptable

    is_valid = Signal(bool)


GEOMETRY_FILE_TYPES = {"OFF Files": ["off", "OFF"], "STL Files": ["stl", "STL"]}


class GeometryFileValidator(QValidator):
    """
    Validator to ensure file exists and is the correct file type.
    """

    def __init__(self, file_types):
        """

        :param file_types:
        """
        super().__init__()
        self.file_types = file_types

    def validate(self, input: str, pos: int):
        if not input:
            self.is_valid.emit(False)
            return QValidator.Intermediate
        if not os.path.isfile(input):
            self.is_valid.emit(False)
            return QValidator.Intermediate
        for suffixes in GEOMETRY_FILE_TYPES.values():
            for suff in suffixes:
                if input.endswith(f".{suff}"):
                    self.is_valid.emit(True)
                    return QValidator.Acceptable
        self.is_valid.emit(False)
        return QValidator.Invalid

    is_valid = Signal(bool)


class OkValidator(QObject):
    """
    Validator to enable the OK button. Several criteria have to be met before this can occur depending on the geometry type.
    """

    def __init__(self, no_geometry_button, mesh_button):
        super().__init__()
        self.name_is_valid = False
        self.file_is_valid = False
        self.units_are_valid = False
        self.no_geometry_button = no_geometry_button
        self.mesh_button = mesh_button

    def set_name_valid(self, is_valid):
        self.name_is_valid = is_valid
        print("Name: {}".format(self.name_is_valid))
        self.validate_ok()

    def set_file_valid(self, is_valid):
        self.file_is_valid = is_valid
        print("File: {}".format(self.file_is_valid))
        self.validate_ok()

    def set_units_valid(self, is_valid):
        self.units_are_valid = is_valid
        print("Units: {}".format(self.units_are_valid))
        self.validate_ok()

    def validate_ok(self):
        """
        Validates the fields in order to dictate whether the OK button should be disabled or enabled.
        :return: None, but emits the isValid signal.
        """
        unacceptable = [
            not self.name_is_valid,
            not self.no_geometry_button.isChecked() and not self.units_are_valid,
            self.mesh_button.isChecked() and not self.file_is_valid,
        ]

        print("Is valid {}".format(unacceptable))
        self.is_valid.emit(not any(unacceptable))

    # Signal to indicate that the fields are valid or invalid. False: invalid.
    is_valid = Signal(bool)
