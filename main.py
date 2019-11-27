"""
Entry script for the nexus constructor application.
Requires Python 3.6+
"""
import logging
import sys
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtCore
from nexus_constructor.main_window import MainWindow
from nexus_constructor.nexus.nexus_wrapper import NexusWrapper
from nexus_constructor.instrument import Instrument
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nexus Constructor")
    if "help" in parser.parse_args():
        exit(0)
    logging.basicConfig(level=logging.INFO)
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join("ui", "icon.png")))
    window = QMainWindow()
    nexus_wrapper = NexusWrapper()
    definitions_dir = os.path.abspath(os.path.join(os.getcwd(), "definitions"))
    instrument = Instrument(nexus_wrapper, definitions_dir)
    ui = MainWindow(instrument, definitions_dir)
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
