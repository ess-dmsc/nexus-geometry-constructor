from PySide2.QtCore import QMetaObject, QObject, QRect, QSize
from PySide2.QtWidgets import (
    QAction,
    QGridLayout,
    QLayout,
    QMenu,
    QMenuBar,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QWidget,
)

from nexus_constructor.instrument_view.instrument_view import InstrumentView
from ui.treeview_tab import ComponentTreeViewTab


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1280, 720)
        self.central_widget = QWidget(MainWindow)

        self.splitter = QSplitter(self.central_widget)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setOpaqueResize(True)

        self.main_grid_layout = QGridLayout(self.central_widget)
        self.main_grid_layout.addWidget(self.splitter)
        self.main_grid_layout.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setMinimumSize(QSize(500, 0))
        self._set_up_component_tree_view()
        self.splitter.addWidget(self.tab_widget)

        self._set_up_3d_view()

        MainWindow.setCentralWidget(self.central_widget)

        self._set_up_menus(MainWindow)
        self.tab_widget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

    def _set_up_3d_view(self):
        self.sceneWidget.setMinimumSize(QSize(600, 0))
        self.splitter.addWidget(self.sceneWidget)

    def _set_up_component_tree_view(self):
        self.sceneWidget = InstrumentView(self.splitter)
        self.component_tree_view_tab = ComponentTreeViewTab(
            scene_widget=self.sceneWidget, parent=self
        )
        self.tab_widget.addTab(self.component_tree_view_tab, "")

    def _set_up_menus(self, MainWindow: QObject):
        self.menu_bar = QMenuBar()
        self.menu_bar.setGeometry(QRect(0, 0, 1280, 720))
        self.file_menu = QMenu(self.menu_bar)
        MainWindow.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.status_bar)
        self.open_nexus_file_action = QAction(MainWindow)
        self.open_json_file_action = QAction(MainWindow)
        self.open_idf_file_action = QAction(MainWindow)
        self.export_to_nexus_file_action = QAction(MainWindow)
        self.export_to_filewriter_JSON_action = QAction(MainWindow)
        self.export_to_forwarder_config_action = QAction(MainWindow)
        self.file_menu.addAction(self.open_json_file_action)
        self.file_menu.addAction(self.export_to_filewriter_JSON_action)
        self.file_menu.addAction(self.export_to_forwarder_config_action)

        self.view_menu = QMenu(self.menu_bar)
        self.show_action_labels = QAction(MainWindow)
        self.show_action_labels.setCheckable(True)
        self.about_window = QAction(MainWindow)
        self.view_menu.addAction(self.about_window)
        self.view_menu.addAction(self.show_action_labels)

        self.menu_bar.addAction(self.file_menu.menuAction())
        self.menu_bar.addAction(self.view_menu.menuAction())
        self._set_up_titles(MainWindow)

    def _set_up_titles(self, MainWindow):
        MainWindow.setWindowTitle("NeXus Constructor")
        self.tab_widget.setTabText(
            self.tab_widget.indexOf(self.component_tree_view_tab), "Components"
        )
        self.file_menu.setTitle("File")
        self.open_nexus_file_action.setText("Open NeXus file")
        self.open_json_file_action.setText("Open Filewriter JSON file")

        self.open_idf_file_action.setText("Open Mantid IDF file")
        self.export_to_nexus_file_action.setText("Export to NeXus file")
        self.export_to_filewriter_JSON_action.setText("Export to Filewriter JSON")
        self.export_to_forwarder_config_action.setText("Export to Forwarder FlatBuffer")
        self.view_menu.setTitle("View")
        self.show_action_labels.setText("Show Button Labels")
        self.about_window.setText("About")
