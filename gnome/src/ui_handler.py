from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QListView,
    QMenu,
    QMessageBox,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QHeaderView,
    QDialog,
)
from PySide6.QtCore import Qt, QPoint
from dialogs import CreateEntityDialog, CreateDepartmentDialog
from context_menu import create_list_context_menu
from project_handler import ProjectHandler


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
    def __init__(self, project_handler: ProjectHandler) -> None:
        super().__init__()
        self.project: ProjectHandler = project_handler

        self.setup_ui()
        self.setup_functional()

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
        self.entities_list: QListView = QListView()
        self.entities_layout.addWidget(self.entities_list)
        self.entities_list.setStyleSheet(
            """.QListView {
            background-color: rgb(50, 50, 50);
            border : 1px solid rgb(10, 10, 10);
            border-radius : 5px;
            }"""  # Set background color
        )
        self.entities_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        context_function: dict[str, callable] = {
            "Create Entity": self.create_entity_dialog,
            "Open in explorer": lambda: print("open in explorer"),
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

        # Add Files Table Widget
        self.departments_list: QListView = QListView()
        self.departments_layout.addWidget(self.departments_list)
        self.departments_list.setStyleSheet(
            """.QListView {
            background-color: rgb(50, 50, 50);
            border : 1px solid rgb(10, 10, 10);
            border-radius : 5px;
            }"""  # Set background color
        )
        self.departments_list.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        context_function: dict[str, callable] = {
            "Create Department": lambda: print("create department"),
            "Open in explorer": lambda: print("open in explorer"),
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
            "Open in explorer": lambda: print("open in explorer"),
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

    def handle_assets_radio_btn_clicked(self) -> None:
        self.shots_radio_btn.setChecked(False)

    def handle_shots_radio_btn_clicked(self) -> None:
        self.assets_radio_btn.setChecked(False)

    def create_entity_dialog(self) -> None:
        dialog = CreateEntityDialog(self)

        dialog.exec()
        if dialog.result() != QDialog.DialogCode.Accepted:
            return

        entity_name: str = dialog.infos["name"]
        self.project.create_entity_folders(entity_name)

    def create_department_dialog(self, type: str) -> None:
        dialog = CreateDepartmentDialog(type, self)
        dialog.exec()
        if dialog.result() != QDialog.DialogCode.Accepted:
            return

        department_name: str = dialog.infos["name"]
        print(department_name)
