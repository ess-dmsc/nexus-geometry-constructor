import uuid
from functools import partial
from typing import Callable, Dict, Union, Tuple, Type

from nexus_constructor.kafka.kafka_interface import KafkaInterface, FileWriter, File
from nexus_constructor.ui_utils import validate_line_edit
from nexus_constructor.validators import BrokerAndTopicValidator
from ui.led import Led
from ui.filewriter_ctrl_frame import Ui_FilewriterCtrl
from PySide2.QtWidgets import QMainWindow, QLineEdit
from PySide2.QtCore import QTimer, QAbstractItemModel
from PySide2.QtGui import QStandardItemModel, QCloseEvent
from PySide2 import QtCore
from nexus_constructor.instrument import Instrument
from nexus_constructor.kafka.status_consumer import StatusConsumer
from nexus_constructor.kafka.command_producer import CommandProducer
import time
from nexus_constructor.json.filewriter_json_writer import (
    NexusToDictConverter,
    generate_nexus_string,
)
from streaming_data_types import run_start_pl72, run_stop_6s4t


class FileWriterCtrl(Ui_FilewriterCtrl, QMainWindow):
    def __init__(self, instrument: Instrument):
        super().__init__()
        self.instrument = instrument
        self.setupUi()
        self.known_writers = {}
        self.known_files = {}
        self.status_consumer = None
        self.command_producer = None

    def setupUi(self):
        super().setupUi(self)

        self.status_consumer = None
        self.status_broker_led = Led(self)
        self.status_topic_layout.addWidget(self.status_broker_led)
        self.status_broker_change_timer = QTimer()
        self._set_up_broker_fields(
            self.status_broker_led,
            self.status_broker_edit,
            self.status_broker_change_timer,
            self.status_broker_timer_changed,
            StatusConsumer,
        )

        self.command_producer = None

        self.command_broker_led = Led(self)
        self.command_broker_layout.addWidget(self.command_broker_led)
        self.command_broker_change_timer = QTimer()
        self._set_up_broker_fields(
            self.command_broker_led,
            self.command_broker_edit,
            self.command_broker_change_timer,
            self.command_broker_timer_changed,
            CommandProducer,
        )

        self.command_widget.ok_button.clicked.connect(self.send_command)
        self.update_status_timer = QTimer()
        self.update_status_timer.timeout.connect(self._check_connection_status)
        self.update_status_timer.start(500)

        self.files_list.clicked.connect(self.file_list_clicked)
        self.stop_file_writing_button.clicked.connect(self.stop_file_writing_clicked)

        self.model = QStandardItemModel(0, 2, self)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "File writer")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Last seen")
        self.file_writers_list.setModel(self.model)
        self.file_writers_list.setColumnWidth(0, 320)

        self.file_list_model = QStandardItemModel(0, 5, self)
        self.file_list_model.setHeaderData(0, QtCore.Qt.Horizontal, "File name")
        self.file_list_model.setHeaderData(1, QtCore.Qt.Horizontal, "Job ID")
        self.file_list_model.setHeaderData(2, QtCore.Qt.Horizontal, "Start Time")
        self.file_list_model.setHeaderData(3, QtCore.Qt.Horizontal, "Stop Time")
        self.file_list_model.setHeaderData(4, QtCore.Qt.Horizontal, "File writer")
        self.files_list.setModel(self.file_list_model)

    @staticmethod
    def _set_up_broker_fields(
        led: Led,
        edit: QLineEdit,
        timer: QTimer,
        timer_callback: Callable,
        kafka_obj_type: Type[KafkaInterface],
    ):
        led.turn_off()
        validator = BrokerAndTopicValidator()
        edit.setValidator(validator)
        validator.is_valid.connect(partial(validate_line_edit, edit))
        edit.textChanged.connect(lambda: timer.start(1000))
        timer.setSingleShot(True)
        timer.timeout.connect(partial(timer_callback, kafka_obj_type))

    def _check_connection_status(self):
        if self.status_consumer is None:
            self.status_broker_led.turn_off()
        else:
            connection_ok = self.status_consumer.connected
            self.status_broker_led.set_status(connection_ok)
            if connection_ok:
                current_writers = self.status_consumer.file_writers
                self._update_writer_list(current_writers)
                self._update_files_list(self.status_consumer.files)

        if self.command_producer is None:
            self.command_broker_led.turn_off()
        else:
            self.command_broker_led.set_status(self.command_producer.connected)

    def status_broker_timer_changed(self, kafka_obj_type: KafkaInterface):
        result = BrokerAndTopicValidator.extract_addr_and_topic(
            self.status_broker_edit.text()
        )
        if result is not None:
            if self.status_consumer is not None:
                self.status_consumer.close()
            self.status_consumer = kafka_obj_type(*result)

    def command_broker_timer_changed(self, kafka_obj_type: KafkaInterface):
        result = BrokerAndTopicValidator.extract_addr_and_topic(
            self.command_broker_edit.text()
        )
        if result is not None:
            if self.command_producer is not None:
                self.command_producer.close()
            self.command_producer = kafka_obj_type(*result)

    def _update_writer_list(self, updated_list: Dict[str, FileWriter]):
        for file_writer_id, file_writer in updated_list:
            current_time, time_str = self.get_time(file_writer)
            if file_writer_id not in self.known_writers:
                number_of_filewriter_rows = self.model.rowCount(QtCore.QModelIndex())
                self.model.insertRow(number_of_filewriter_rows)
                self.model.setData(
                    self.model.index(number_of_filewriter_rows, 0), file_writer_id
                )
                self.model.setData(
                    self.model.index(number_of_filewriter_rows, 1),
                    file_writer.last_time,
                )
            if current_time != file_writer.last_time:
                self._set_time(self.model, file_writer, current_time, time_str)

    def _update_files_list(self, updated_list: Dict[str, File]):
        for file_name, file_obj in updated_list.items():
            current_time, time_str = self.get_time(file_obj)
            if file_name not in self.known_files:
                number_of_file_rows = self.file_list_model.rowCount(
                    QtCore.QModelIndex()
                )
                self.file_list_model.insertRow(number_of_file_rows)
                self.file_list_model.setData(
                    self.file_list_model.index(number_of_file_rows, 0), file_obj.name
                )
                self.file_list_model.setData(
                    self.file_list_model.index(number_of_file_rows, 1), file_obj.job_id
                )
                self.file_list_model.setData(
                    self.file_list_model.index(number_of_file_rows, 2),
                    file_obj.start_time,
                )
                self.file_list_model.setData(
                    self.file_list_model.index(number_of_file_rows, 3),
                    file_obj.stop_time,
                )
                self.file_list_model.setData(
                    self.file_list_model.index(number_of_file_rows, 3),
                    file_obj.writer_id,
                )

            if current_time != file_obj.last_time:
                self._set_time(self.file_list_model, file_obj, current_time, time_str)

    @staticmethod
    def get_time(file: Union[File, FileWriter]) -> Tuple[str, str]:
        current_time = file.last_time
        time_struct = time.localtime(current_time / 1000)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S%Z", time_struct)
        return current_time, time_str

    @staticmethod
    def _set_time(
        model: QAbstractItemModel,
        current_index: Union[File, FileWriter],
        current_time: str,
        time_str: str,
    ):
        model.setData(model.index(current_index.row, 1), time_str)
        current_index.last_time = current_time

    def send_command(self):
        if self.command_producer is not None:
            (
                nexus_file_name,
                broker,
                start_time,
                stop_time,
                service_id,
                abort_on_uninitialised_stream,
                use_swmr,
            ) = self.command_widget.get_arguments()
            self.command_producer.send_command(
                bytes(
                    run_start_pl72.serialise_pl72(
                        job_id=str(uuid.uuid4()),
                        filename=nexus_file_name,
                        start_time=start_time,
                        stop_time=stop_time,
                        broker=broker,
                        nexus_structure=generate_nexus_string(
                            NexusToDictConverter(), self.instrument
                        ),
                        service_id=service_id,
                    )
                )
            )
            self.command_widget.ok_button.setEnabled(False)

    def file_list_clicked(self):
        if len(self.files_list.selectedIndexes()) > 0:
            self.stop_file_writing_button.setEnabled(True)
        else:
            self.stop_file_writing_button.setEnabled(False)

    def stop_file_writing_clicked(self):
        selected_files = self.files_list.selectedIndexes()
        for index in selected_files:
            current_file = index.internalData()
            self.command_producer.send_command(
                bytes(
                    run_stop_6s4t.serialise_6s4t(
                        job_id=current_file.job_id, service_id=current_file.writer_id,
                    )
                )
            )

    def closeEvent(self, event: QCloseEvent):
        if self.status_consumer is not None:
            self.status_consumer.close()
        if self.command_producer is not None:
            self.command_producer.close()
