import uuid
from functools import partial

import h5py
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QComboBox,
    QGridLayout,
    QLineEdit,
    QDialog,
    QLabel,
    QSpinBox,
    QPushButton,
    QGroupBox,
    QRadioButton,
    QCheckBox,
    QFormLayout,
)
import numpy as np

SCHEMAS = ["ev42", "f142", "hs00", "ns10", "TdcTime"]
F142_TYPES = [
    "byte",
    "ubyte",
    "short",
    "ushort",
    "int",
    "uint",
    "long",
    "ulong",
    "float",
    "double",
    "string",
]

STRING_DTYPE = h5py.special_dtype(vlen=str)


class StreamFieldsWidget(QDialog):
    """
    A stream widget containing schema-specific properties.
    """

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setLayout(QGridLayout())
        self.setWindowModality(Qt.WindowModal)
        self.setModal(True)

        self.hs00_unimplemented_label = QLabel(
            "hs00 (Event histograms) has not yet been fully implemented."
        )

        self.schema_label = QLabel("Schema: ")
        self.schema_combo = QComboBox()

        self.topic_label = QLabel("Topic: ")
        self.topic_line_edit = QLineEdit()
        self.topic_line_edit.setPlaceholderText("broker[:port, default=9092]/topic")

        self.source_label = QLabel("Source: ")
        self.source_line_edit = QLineEdit()

        self.array_size_label = QLabel("Array size")
        self.array_size_spinbox = QSpinBox()
        self.array_size_spinbox.setMaximum(np.iinfo(np.int32).max)

        self.type_label = QLabel("Type: ")
        self.type_combo = QComboBox()
        self.type_combo.addItems(F142_TYPES)

        self.show_advanced_options_button = QPushButton(
            text="Show/hide advanced options"
        )
        self.show_advanced_options_button.setCheckable(True)
        self.show_advanced_options_button.clicked.connect(self._show_advanced_options)

        self._set_up_f142_group_box()
        self._set_up_ev42_group_box()

        self.scalar_radio = QRadioButton(text="Scalar")
        self.scalar_radio.clicked.connect(partial(self._show_array_size, False))
        self.scalar_radio.setChecked(True)
        self.scalar_radio.clicked.emit()

        self.array_radio = QRadioButton(text="Array")
        self.array_radio.clicked.connect(partial(self._show_array_size, True))

        self.schema_combo.currentTextChanged.connect(self._schema_type_changed)
        self.schema_combo.addItems(SCHEMAS)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.parent().close)

        self.set_advanced_options_state()

        self.layout().addWidget(self.schema_label, 0, 0)
        self.layout().addWidget(self.schema_combo, 0, 1)

        self.layout().addWidget(self.topic_label, 1, 0)
        self.layout().addWidget(self.topic_line_edit, 1, 1)

        self.layout().addWidget(self.source_label, 2, 0)
        self.layout().addWidget(self.source_line_edit, 2, 1)

        self.layout().addWidget(self.type_label, 3, 0)
        self.layout().addWidget(self.type_combo, 3, 1)

        self.layout().addWidget(self.scalar_radio, 4, 0)
        self.layout().addWidget(self.array_radio, 4, 1)

        self.layout().addWidget(self.array_size_label, 5, 0)
        self.layout().addWidget(self.array_size_spinbox, 5, 1)

        self.layout().addWidget(self.hs00_unimplemented_label, 6, 0, 1, 2)

        # Spans both rows
        self.layout().addWidget(self.show_advanced_options_button, 7, 0, 1, 2)
        self.layout().addWidget(self.f142_advanced_group_box, 8, 0, 1, 2)

        self.layout().addWidget(self.ev42_advanced_group_box, 9, 0, 1, 2)

        self.layout().addWidget(self.ok_button, 10, 0, 1, 2)

        self._schema_type_changed(self.schema_combo.currentText())

    def _set_up_ev42_group_box(self):
        """
        Sets up the UI for ev42 advanced options.
        """

        self.ev42_advanced_group_box = QGroupBox(
            parent=self.show_advanced_options_button
        )
        self.ev42_advanced_group_box.setLayout(QFormLayout())

        self.ev42_adc_pulse_debug_label = QLabel("adc_pulse_debug")
        self.ev42_adc_pulse_debug_checkbox = QCheckBox()

        minimum_value = 0
        maximum_value = 100000000

        self.ev42_nexus_indices_index_every_mb_label = QLabel(
            "nexus.indices.index_every_mb"
        )
        self.ev42_nexus_indices_index_every_mb_spinbox = QSpinBox()
        self.ev42_nexus_indices_index_every_mb_spinbox.setRange(
            minimum_value, maximum_value
        )

        self.ev42_nexus_indices_index_every_kb_label = QLabel(
            "nexus.indices.index_every_kb"
        )
        self.ev42_nexus_indices_index_every_kb_spinbox = QSpinBox()
        self.ev42_nexus_indices_index_every_kb_spinbox.setRange(
            minimum_value, maximum_value
        )

        self.ev42_nexus_chunk_chunk_mb_label = QLabel("nexus.chunk.chunk_mb")
        self.ev42_nexus_chunk_chunk_mb_spinbox = QSpinBox()
        self.ev42_nexus_chunk_chunk_mb_spinbox.setRange(minimum_value, maximum_value)

        self.ev42_nexus_chunk_chunk_kb_label = QLabel("nexus.chunk.chunk_kb")
        self.ev42_nexus_chunk_chunk_kb_spinbox = QSpinBox()
        self.ev42_nexus_chunk_chunk_kb_spinbox.setRange(minimum_value, maximum_value)

        self.ev42_nexus_buffer_size_mb_label = QLabel("nexus.buffer.size_mb")
        self.ev42_nexus_buffer_size_mb_spinbox = QSpinBox()
        self.ev42_nexus_buffer_size_mb_spinbox.setRange(minimum_value, maximum_value)

        self.ev42_nexus_buffer_size_kb_label = QLabel("nexus.buffer.size_kb")
        self.ev42_nexus_buffer_size_kb_spinbox = QSpinBox()
        self.ev42_nexus_buffer_size_kb_spinbox.setRange(minimum_value, maximum_value)

        self.ev42_nexus_buffer_packet_max_kb_label = QLabel(
            "nexus.buffer.packet_max_kb"
        )
        self.ev42_nexus_buffer_packet_max_kb_spinbox = QSpinBox()
        self.ev42_nexus_buffer_packet_max_kb_spinbox.setRange(
            minimum_value, maximum_value
        )

        self.ev42_advanced_group_box.layout().addRow(
            self.ev42_adc_pulse_debug_label, self.ev42_adc_pulse_debug_checkbox
        )
        self.ev42_advanced_group_box.layout().addRow(
            self.ev42_nexus_indices_index_every_mb_label,
            self.ev42_nexus_indices_index_every_mb_spinbox,
        )
        self.ev42_advanced_group_box.layout().addRow(
            self.ev42_nexus_indices_index_every_kb_label,
            self.ev42_nexus_indices_index_every_kb_spinbox,
        )
        self.ev42_advanced_group_box.layout().addRow(
            self.ev42_nexus_chunk_chunk_mb_label, self.ev42_nexus_chunk_chunk_mb_spinbox
        )
        self.ev42_advanced_group_box.layout().addRow(
            self.ev42_nexus_chunk_chunk_kb_label, self.ev42_nexus_chunk_chunk_kb_spinbox
        )
        self.ev42_advanced_group_box.layout().addRow(
            self.ev42_nexus_buffer_size_mb_label, self.ev42_nexus_buffer_size_mb_spinbox
        )
        self.ev42_advanced_group_box.layout().addRow(
            self.ev42_nexus_buffer_size_kb_label, self.ev42_nexus_buffer_size_kb_spinbox
        )
        self.ev42_advanced_group_box.layout().addRow(
            self.ev42_nexus_buffer_packet_max_kb_label,
            self.ev42_nexus_buffer_packet_max_kb_spinbox,
        )

    def _set_up_f142_group_box(self):
        """
        Sets up the UI for the f142 advanced options.
        """
        self.f142_advanced_group_box = QGroupBox(
            parent=self.show_advanced_options_button
        )
        self.f142_advanced_group_box.setLayout(QFormLayout())

        minimum_value = 0
        maximum_value = 100000000
        self.f142_nexus_indices_index_every_mb_label = QLabel(
            "nexus.indices.index_every_mb"
        )
        self.f142_nexus_indices_index_every_mb_spinbox = QSpinBox()
        self.f142_nexus_indices_index_every_mb_spinbox.setRange(
            minimum_value, maximum_value
        )

        self.f142_nexus_indices_index_every_kb_label = QLabel(
            "nexus.indices.index_every_kb"
        )
        self.f142_nexus_indices_index_every_kb_spinbox = QSpinBox()
        self.f142_nexus_indices_index_every_kb_spinbox.setRange(
            minimum_value, maximum_value
        )

        self.f142_nexus_store_latest_into_label = QLabel("store_latest_into")
        self.f142_nexus_store_latest_into_spinbox = QSpinBox()
        self.f142_nexus_store_latest_into_spinbox.setRange(minimum_value, maximum_value)

        self.f142_advanced_group_box.layout().addRow(
            self.f142_nexus_indices_index_every_mb_label,
            self.f142_nexus_indices_index_every_mb_spinbox,
        )
        self.f142_advanced_group_box.layout().addRow(
            self.f142_nexus_indices_index_every_kb_label,
            self.f142_nexus_indices_index_every_kb_spinbox,
        )
        self.f142_advanced_group_box.layout().addRow(
            self.f142_nexus_store_latest_into_label,
            self.f142_nexus_store_latest_into_spinbox,
        )

    def _show_advanced_options(self):
        schema = self.schema_combo.currentText()
        if schema == "f142":
            self.f142_advanced_group_box.setVisible(
                not self.f142_advanced_group_box.isVisible()
            )
        elif schema == "ev42":
            self.ev42_advanced_group_box.setVisible(
                not self.ev42_advanced_group_box.isVisible()
            )

        self.set_advanced_options_state()

    def set_advanced_options_state(self):
        """Used for getting the stream options when the dialog is closed."""
        self.advanced_options_enabled = (
            True
            if self.ev42_advanced_group_box.isVisible()
            or self.f142_advanced_group_box.isVisible()
            else False
        )

    def _show_array_size(self, show: bool):
        self.array_size_spinbox.setVisible(show)
        self.array_size_label.setVisible(show)

    def _schema_type_changed(self, schema: str):
        self.parent().setWindowTitle(f"Editing {schema} stream field")
        self.hs00_unimplemented_label.setVisible(False)
        self.f142_advanced_group_box.setVisible(False)
        self.ev42_advanced_group_box.setVisible(False)
        self.show_advanced_options_button.setVisible(False)
        self.set_advanced_options_state()
        if schema == "f142":
            self._set_edits_visible(True, True)
            self.show_advanced_options_button.setVisible(True)
            self.f142_advanced_group_box.setVisible(False)
        elif schema == "ev42":
            self._set_edits_visible(False, False)
            self.show_advanced_options_button.setVisible(True)
            self.ev42_advanced_group_box.setVisible(False)
        elif schema == "hs00":
            self._set_edits_visible(True, False)
            self.hs00_unimplemented_label.setVisible(True)
        elif schema == "ns10":
            self._set_edits_visible(True, False, "nicos/<device>/<parameter>")
        elif schema == "TdcTime":
            self._set_edits_visible(True, False)

    def _set_edits_visible(self, source: bool, type: bool, source_hint=None):
        self.source_label.setVisible(source)
        self.source_line_edit.setVisible(source)
        self.type_label.setVisible(type)
        self.type_combo.setVisible(type)
        self.array_radio.setVisible(type)
        self.scalar_radio.setVisible(type)
        if source_hint:
            self.source_line_edit.setPlaceholderText(source_hint)
        else:
            self.source_line_edit.setPlaceholderText("")

    def get_stream_group(self) -> h5py.Group:
        """
        Create the stream group with a temporary in-memory HDF5 file.
        :return: The created HDF group.
        """

        temp_file = h5py.File(
            name=str(uuid.uuid4()), driver="core", backing_store=False
        )
        group = temp_file.create_group("children")
        group.create_dataset(name="type", dtype=STRING_DTYPE, data="stream")
        stream_group = group.create_group(self.parent().parent().name)
        stream_group.attrs["NX_class"] = "NCstream"
        stream_group.create_dataset(
            name="topic", dtype=STRING_DTYPE, data=self.topic_line_edit.text()
        )
        stream_group.create_dataset(
            name="writer_module",
            dtype=STRING_DTYPE,
            data=self.schema_combo.currentText(),
        )

        schema = self.schema_combo.currentText()

        if schema == "f142":
            self._create_f142_fields(stream_group)
        if schema != "ev42":
            stream_group.create_dataset(
                "source", dtype=STRING_DTYPE, data=self.source_line_edit.text()
            )
        elif schema == "ev42":
            self._create_ev42_fields(stream_group)
        return stream_group

    def _create_ev42_fields(self, stream_group: h5py.Group):
        """
        Create ev42 fields in the given group if advanced options are specified.
        :param stream_group: The group to apply fields to.
        """
        if self.advanced_options_enabled:
            stream_group.create_dataset(
                self.ev42_adc_pulse_debug_label.text(),
                dtype=bool,
                data=self.ev42_adc_pulse_debug_checkbox.isChecked(),
            )
            stream_group.create_dataset(
                self.ev42_nexus_indices_index_every_mb_label.text(),
                dtype=int,
                data=self.ev42_nexus_indices_index_every_mb_spinbox.value(),
            )
            stream_group.create_dataset(
                self.ev42_nexus_indices_index_every_kb_label.text(),
                dtype=int,
                data=self.ev42_nexus_indices_index_every_kb_spinbox.value(),
            )
            stream_group.create_dataset(
                self.ev42_nexus_chunk_chunk_mb_label.text(),
                dtype=int,
                data=self.ev42_nexus_chunk_chunk_mb_spinbox.value(),
            )
            stream_group.create_dataset(
                self.ev42_nexus_chunk_chunk_kb_label.text(),
                dtype=int,
                data=self.ev42_nexus_chunk_chunk_kb_spinbox.value(),
            )
            stream_group.create_dataset(
                self.ev42_nexus_buffer_size_mb_label.text(),
                dtype=int,
                data=self.ev42_nexus_buffer_size_mb_spinbox.value(),
            )
            stream_group.create_dataset(
                self.ev42_nexus_buffer_size_kb_label.text(),
                dtype=int,
                data=self.ev42_nexus_buffer_size_kb_spinbox.value(),
            )
            stream_group.create_dataset(
                self.ev42_nexus_buffer_packet_max_kb_label.text(),
                dtype=int,
                data=self.ev42_nexus_buffer_packet_max_kb_spinbox.value(),
            )

    def _create_f142_fields(self, stream_group: h5py.Group):
        """
        Create f142 fields in the given group if advanced options are specified.
        :param stream_group: The group to apply fields to.
        """
        stream_group.create_dataset(
            "type", dtype=STRING_DTYPE, data=self.type_combo.currentText()
        )
        if self.array_radio.isChecked():
            stream_group.create_dataset(
                "array_size", data=self.array_size_spinbox.value()
            )
        if self.advanced_options_enabled:
            # Use strings for names, we don't care if it's byte-encoded as it will output to JSON anyway.
            stream_group.create_dataset(
                self.f142_nexus_indices_index_every_mb_label.text(),
                dtype=int,
                data=self.f142_nexus_indices_index_every_mb_spinbox.value(),
            )
            stream_group.create_dataset(
                self.nexus_chunk_mb_label.text(),
                dtype=int,
                data=self.nexus_chunk_mb_spinbox.value(),
            )
            stream_group.create_dataset(
                self.f142_nexus_indices_index_every_kb_label.text(),
                dtype=int,
                data=self.f142_nexus_indices_index_every_kb_spinbox.value(),
            )
            stream_group.create_dataset(
                self.f142_nexus_store_latest_into_label.text(),
                dtype=int,
                data=self.f142_nexus_store_latest_into_spinbox.value(),
            )