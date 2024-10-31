from PySide2.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QHeaderView,
    QDialog,
    QListWidget,
    QTableWidgetItem,
    QAbstractItemView,
)
from PySide2.QtCore import Qt, QPoint
from src.dialogs import (
    CreateEntityDialog,
    CreateDepartmentDialog,
    NoFocusDelegate,
    CreateNewVersion,
)
from src.context_menu import create_list_context_menu
from src.project_handler import ProjectHandler
import subprocess
import os


class NonUncheckingButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setCheckable(True)

    def mousePressEvent(self, event):
        # Ignore the click event if the button is already checked
        if self.isChecked():
            event.ignore()  # Prevent toggling off
        else:
            super().mousePressEvent(event)  # Allow toggling on


class MainWindow(QMainWindow):
    def __init__(self, project_handler: ProjectHandler, parent=None) -> None:
        super().__init__(parent)
        self.project: ProjectHandler = project_handler

        self.setup_ui()
        self.setup_functional()

        self.update_lists()

    def setup_ui(self) -> None:
        # Set window properties
        self.setWindowTitle("Gnome Pipeline")
        self.resize(1400, 900)

        # Set central widget
        self.main_layout: QHBoxLayout = QHBoxLayout()
        self.main_widget: QWidget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet(
            """.QWidget { background-color: rgb(35, 35, 35);}"""  # Set background color
        )

        # Setup entities UI
        self.setup_entities_ui()

        # ¶ Setup Departments UI
        self.setup_departments_ui()

        # Setup Files UI
        self.setup_files_ui()

    def setup_entities_ui(self) -> None:

        # Add Entities Widget
        self.entities_layout: QVBoxLayout = QVBoxLayout()
        self.entities_widget: QWidget = QWidget()
        self.entities_widget.setMaximumWidth(200)
        self.main_layout.addWidget(self.entities_widget)
        self.entities_widget.setLayout(self.entities_layout)

        ## Add Entities Radio Buttons
        self.entities_radio_layout: QHBoxLayout = QHBoxLayout()
        self.entities_radio_layout.setContentsMargins(20, 0, 20, 0)
        self.entities_radio_widget: QWidget = QWidget()
        self.entities_layout.addWidget(self.entities_radio_widget)
        self.entities_radio_layout.setSpacing(2)
        self.entities_radio_widget.setLayout(self.entities_radio_layout)
        self.entities_radio_widget.setStyleSheet(
            """
            .NonUncheckingButton{ 
                background-color: rgb(70, 70, 70);
                color: rgb(200, 200, 200);
                padding: 3px;
                border: 0;
            }
            .NonUncheckingButton:hover{
                background-color: rgb(50, 50, 50);}
            .NonUncheckingButton:checked { background-color: rgb(27, 130, 174);}
            """
        )

        self.assets_radio_btn: NonUncheckingButton = NonUncheckingButton("Assets")
        self.entities_radio_layout.addWidget(self.assets_radio_btn)
        self.assets_radio_btn.setStyleSheet(
            """
            .NonUncheckingButton{
                border-top-left-radius: 7px;
                border-bottom-left-radius: 7px;
            }"""
        )
        self.shots_radio_btn: NonUncheckingButton = NonUncheckingButton("Shots")
        self.entities_radio_layout.addWidget(self.shots_radio_btn)
        self.shots_radio_btn.setStyleSheet(
            """
            .NonUncheckingButton{
                border-top-right-radius: 7px;
                border-bottom-right-radius: 7px;
            }"""
        )

        ## Add Entities List View
        self.entities_list: QListWidget = QListWidget()
        self.entities_list.setItemDelegate(NoFocusDelegate())
        self.entities_layout.addWidget(self.entities_list)
        self.entities_list.setStyleSheet(
            """.QListWidget {
            background-color: rgb(50, 50, 50);
            border : 1px solid rgb(10, 10, 10);
            border-radius : 5px;
            }
            .QListWidget::item{
            background-color: rgb(80, 80, 80);
            color: rgb(200, 200, 200);
            padding: 3px;
            }
            .QListWidget::item:selected{
            background-color: rgb(27, 130, 174);
            }"""  # Set background color
        )
        self.entities_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        context_function: dict[str, callable] = {
            "Create Entity": self.create_entity_dialog,
            "Open in explorer": self.open_entities_in_explorer,
        }
        self.entities_list.customContextMenuRequested.connect(
            lambda position: create_list_context_menu(
                self.entities_list, context_function, self, position
            )
        )

    def setup_departments_ui(self) -> None:
        # Add Departments Widget
        self.departments_layout: QVBoxLayout = QVBoxLayout()
        self.departments_widget: QWidget = QWidget()
        self.main_layout.addWidget(self.departments_widget)
        self.departments_widget.setLayout(self.departments_layout)

        # Departments Title
        self.departments_title_label: QLabel = QLabel("Departments:")
        self.departments_layout.addWidget(self.departments_title_label)
        self.departments_title_label.setStyleSheet(
            """
            .QLabel {
                color: rgb(200, 200, 200);
            }"""
        )

        # Add Departments Table Widget
        self.departments_list: QListWidget = QListWidget()
        self.departments_list.setItemDelegate(NoFocusDelegate())
        self.departments_layout.addWidget(self.departments_list)
        self.departments_list.setStyleSheet(
            """.QListWidget {
            background-color: rgb(50, 50, 50);
            border : 1px solid rgb(10, 10, 10);
            border-radius : 5px;
            }.QListWidget::item{
            background-color: rgb(80, 80, 80);
            color: rgb(200, 200, 200);
            padding: 3px;
            }
            .QListWidget::item:selected{
            background-color: rgb(27, 130, 174);
            }"""  # Set background color
        )
        self.departments_list.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        context_function: dict[str, callable] = {
            "Create Department": self.create_department_dialog,
            "Open in explorer": self.open_departments_in_explorer,
        }
        self.departments_list.customContextMenuRequested.connect(
            lambda position: create_list_context_menu(
                self.departments_list, context_function, self, position
            )
        )

    def setup_files_ui(self) -> None:
        # Add Files Widget
        self.files_layout: QVBoxLayout = QVBoxLayout()
        self.files_widget: QWidget = QWidget()
        self.main_layout.addWidget(self.files_widget)
        self.files_widget.setLayout(self.files_layout)

        # Files Title
        self.files_title_label: QLabel = QLabel("Files:")
        self.files_layout.addWidget(self.files_title_label)
        self.files_title_label.setStyleSheet(
            """
            .QLabel {
                color: rgb(200, 200, 200);
            }"""
        )

        # Add Files Table Widget
        self.files_table_widget: QTableWidget = QTableWidget()
        self.files_table_widget.verticalHeader().setVisible(False)
        self.files_table_widget.setItemDelegate(NoFocusDelegate())
        self.files_table_widget.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.files_table_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.files_layout.addWidget(self.files_table_widget)
        self.files_table_widget.setStyleSheet(
            """
            .QTableWidget {
                background-color: rgb(50, 50, 50);
                color: rgb(200, 200, 200);
                border : 1px solid rgb(10, 10, 10);
                border-radius : 5px;
            }
            .QHeaderView::section {
                background-color: rgb(35, 35, 35);
                color: rgb(200, 200, 200);
                border: 0;
                border-left: 2px solid rgb(50, 50, 50);
                padding-top: 3px;
                padding-bottom: 3px;
            }
            .QHeaderView::section::first {            
                border: 0;
            }
            .QTableWidget::item{
                padding-left: 10px;
                padding-right: 10px;
                border: 0px;}
            """
        )
        headers: list[str] = ["Software", "Version", "Comment", "Date"]
        self.files_table_widget.setColumnCount(len(headers))
        self.files_table_widget.setHorizontalHeaderLabels(headers)
        self.files_table_widget.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )

        self.files_table_widget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        context_function: dict[str, callable] = {
            "Create new version from current": self.create_new_version,
            "Open in explorer": self.open_files_in_explorer,
        }
        self.files_table_widget.customContextMenuRequested.connect(
            lambda position: create_list_context_menu(
                self.files_table_widget, context_function, self, position
            )
        )

    def setup_functional(self) -> None:
        self.assets_radio_btn.setChecked(True)

        self.assets_radio_btn.clicked.connect(self.handle_assets_radio_btn_clicked)
        self.shots_radio_btn.clicked.connect(self.handle_shots_radio_btn_clicked)

        self.entities_list.itemClicked.connect(self.update_departments)
        self.departments_list.itemClicked.connect(self.update_files)

    def handle_assets_radio_btn_clicked(self) -> None:
        self.shots_radio_btn.setChecked(False)
        self.update_entities()

    def handle_shots_radio_btn_clicked(self) -> None:
        self.assets_radio_btn.setChecked(False)
        self.update_entities()

    def get_entity_type(self) -> str:
        return "assets" if self.assets_radio_btn.isChecked() else "shots"

    def create_entity_dialog(self) -> None:
        dialog = CreateEntityDialog(self)

        dialog.exec_()
        if dialog.result() != QDialog.DialogCode.Accepted:
            return

        entity_name: str = dialog.infos["name"]

        self.project.create_entity_folders(self.get_entity_type(), entity_name)
        self.update_entities()

    def create_department_dialog(self) -> None:
        entities_selected: list = self.entities_list.selectedItems()
        if not entities_selected:
            return

        selected_entity: str = entities_selected[0].text()
        dialog = CreateDepartmentDialog(self.get_entity_type(), self)
        dialog.exec_()
        if dialog.result() != QDialog.DialogCode.Accepted:
            return

        department_name: str = dialog.infos["department"]
        self.project.create_department_folder(
            self.get_entity_type(), selected_entity, department_name
        )
        self.update_departments()

    def update_entities(self) -> None:
        entities: list[str] = self.project.get_entities(self.get_entity_type())
        self.entities_list.clear()
        self.entities_list.addItems(entities)
        self.update_departments()

    def update_departments(self) -> None:
        entities_selected: list = self.entities_list.selectedItems()
        self.departments_list.clear()
        self.update_files()
        if not entities_selected:
            return
        selected_entity: str = entities_selected[0].text()
        departments: list[str] = self.project.get_departments(
            self.get_entity_type(), selected_entity
        )
        self.departments_list.addItems(departments)

    def update_files(self) -> None:
        self.files_table_widget.clearContents()
        self.files_table_widget.setRowCount(0)
        entity_type: str = self.get_entity_type()
        entities_selected: str = self.get_entity()
        if not entities_selected:
            return
        department_selected: str = self.get_department()
        if not department_selected:
            return
        files: list[dict[str, str]] = self.project.get_files(
            entity_type, entities_selected, department_selected
        )

        files = sorted(files, key=lambda file: file["version"])  # Sort files by version
        self.files_table_widget.setRowCount(len(files))
        for i, file_info in enumerate(files):
            software: str = file_info["software"]
            version: str = file_info["version"]
            comment: str = file_info["comment"]
            date: str = file_info["date"]
            self.files_table_widget.setItem(i, 0, QTableWidgetItem(software))
            self.files_table_widget.setItem(i, 1, QTableWidgetItem(version))
            self.files_table_widget.setItem(i, 2, QTableWidgetItem(comment))
            self.files_table_widget.setItem(i, 3, QTableWidgetItem(date))
        self.files_table_widget.resizeColumnToContents(0)
        self.files_table_widget.resizeColumnToContents(1)
        self.files_table_widget.resizeColumnToContents(3)

    def update_lists(self) -> None:
        self.update_entities()

    def get_entity(self) -> str:
        entities_selected: list = self.entities_list.selectedItems()
        if not entities_selected:
            return ""
        return entities_selected[0].text()

    def get_department(self) -> str:
        departments_selected: list = self.departments_list.selectedItems()
        if not departments_selected:
            return ""
        return departments_selected[0].text()

    def create_new_version(self) -> None:
        entity_type: str = self.get_entity_type()
        entity_name: str = self.get_entity()
        if not entity_name:
            return
        department_selected: str = self.get_department()
        if not department_selected:
            return

        self.project.create_new_version(entity_type, entity_name, department_selected)
        self.update_files()

    def open_entities_in_explorer(self) -> None:
        entity_type = self.get_entity_type()
        path = os.path.join(self.project.project_path, entity_type)
        subprocess.Popen('explorer "' + path + '"')

    def open_departments_in_explorer(self) -> None:
        entity_type: str = self.get_entity_type()
        entity_name: str = self.get_entity()
        if not entity_name:
            return
        path = os.path.join(self.project.project_path, entity_type, entity_name)
        subprocess.Popen('explorer "' + path + '"')

    def open_files_in_explorer(self) -> None:
        entity_type: str = self.get_entity_type()
        entity_name: str = self.get_entity()
        if not entity_name:
            return
        department_name: str = self.get_department()
        if not department_name:
            return
        path = os.path.join(
            self.project.project_path, entity_type, entity_name, department_name
        )
        subprocess.Popen('explorer "' + path + '"')
