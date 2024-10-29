from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QListView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setup_ui()

    def setup_ui(self) -> None:
        # Set window properties
        self.setWindowTitle("Gnome Pipeline")
        self.resize(1400, 900)

        # Set central widget
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_widget: QWidget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet(
            """.QWidget { background-color: rgb(35, 35, 35);}"""  # Set background color
        )

        # Add ListView
        self.entities_list: QListView = QListView()
        self.entities_list.setMaximumWidth(200)
        self.entities_list.setStyleSheet(
            """.QListView { 
            background-color: rgb(50, 50, 50);
            border : 1px solid rgb(10, 10, 10);
            border-radius : 7px;
            }"""  # Set background color
        )
        self.main_layout.addWidget(self.entities_list)
