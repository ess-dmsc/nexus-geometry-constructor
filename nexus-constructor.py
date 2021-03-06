"""
Entry script for the nexus constructor application.
Requires Python 3.6+
"""
import argparse
import logging
import os
import sys

from PySide2 import QtCore
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QMainWindow

from nexus_constructor.component_type import make_dictionary_of_class_definitions
from nexus_constructor.main_window import MainWindow
from nexus_constructor.model.model import Model

if getattr(sys, "frozen", False):
    # frozen
    root_dir = os.path.dirname(sys.executable)
else:
    root_dir = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nexus Constructor")
    if "help" in parser.parse_args():
        exit(0)
    logging.basicConfig(level=logging.INFO)
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join("ui", "icon.png")))
    window = QMainWindow()
    definitions_dir = os.path.abspath(os.path.join(root_dir, "definitions"))
    _, nx_component_classes = make_dictionary_of_class_definitions(definitions_dir)
    model = Model()
    ui = MainWindow(model, nx_component_classes)
    ui.setupUi(window)
    window.showMaximized()
    sys.exit(app.exec_())
