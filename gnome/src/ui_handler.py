from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QListView,
    QMenu,
    QMessageBox,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QPoint


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setup_ui()

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

        # Add Entities Widget
        self.entities_layout: QVBoxLayout = QVBoxLayout()
        self.entities_widget: QWidget = QWidget()
        self.entities_widget.setMaximumWidth(200)
        self.main_layout.addWidget(self.entities_widget)
        self.entities_widget.setLayout(self.entities_layout)

        ## Add Entities Radio Buttons
        self.entities_radio_layout: QHBoxLayout = QHBoxLayout()
        self.entities_radio_widget: QWidget = QWidget()
        self.entities_layout.addWidget(self.entities_radio_widget)
        self.entities_radio_layout.setSpacing(0)
        self.entities_radio_widget.setLayout(self.entities_radio_layout)
        self.entities_radio_widget.setStyleSheet(
            """
            .QPushButton{ 
            background-color: rgb(50, 50, 50);
            color: rgb(200, 200, 200);
            }
            .QPushButton:hover{
            background-color: rgb(30, 30, 30);}"""
        )

        self.assets_radio_btn: QPushButton = QPushButton("Assets")
        self.entities_radio_layout.addWidget(self.assets_radio_btn)

        self.shots_radio_btn: QPushButton = QPushButton("Shots")
        self.entities_radio_layout.addWidget(self.shots_radio_btn)

        ## Add Entities List View
        self.entities_list: QListView = QListView()
        self.entities_layout.addWidget(self.entities_list)
        self.entities_list.setStyleSheet(
            """.QListView {
            background-color: rgb(50, 50, 50);
            border : 1px solid rgb(10, 10, 10);
            border-radius : 7px;
            }"""  # Set background color
        )
        self.entities_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.entities_list.customContextMenuRequested.connect(
            self.show_entities_list_context_menu
        )

    def show_entities_list_context_menu(self, position: QPoint):
        # Check if an item is clicked
        index = self.entities_list.indexAt(position)
        if not index.isValid():  # If no item is clicked
            menu: QMenu = QMenu(self)
            menu.setStyleSheet(
                """.QMenu { 
                    background-color: rgb(100, 100, 100);
                    color : rgb(200, 200, 200);
                    padding: 0;
                }
                .QMenu::item{
                    padding-left: 20px;
                    padding-right: 20px;
                    padding-top: 3px;
                    padding-bottom: 3px;
                }
                .QMenu::item:selected { 
                    border: 1px solid rgb(200, 200, 200);
                }"""
            )
            create_entity = menu.addAction("Create Entity")
            open_in_explorer = menu.addAction("Open in Explorer")

            # Connect menu actions
            create_entity.triggered.connect(
                lambda: QMessageBox.information(
                    self, "Option Selected", "Create Entity"
                )
            )
            open_in_explorer.triggered.connect(
                lambda: QMessageBox.information(
                    self, "Option Selected", "Open in Explorer"
                )
            )

            # Display the menu at the mouse position
            menu.exec(self.entities_list.mapToGlobal(position))
