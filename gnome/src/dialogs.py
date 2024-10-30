from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)


class CreateEntityDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.cancel = False
        self.infos = {}

    def setup_ui(self) -> None:
        self.setWindowTitle("Create Entity")
        self.resize(300, 100)

        self.setAutoFillBackground(True)
        self.setStyleSheet(
            """background-color: rgb(35, 35, 35);
                color: rgb(200, 200, 200);
                """  # Set background color
        )

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        first_layout: QHBoxLayout = QHBoxLayout()
        first_widget: QWidget = QWidget()
        first_widget.setLayout(first_layout)
        main_layout.addWidget(first_widget)

        self.entity_name_label: QLabel = QLabel("Name:")
        self.entity_name_line_edit: QLineEdit = QLineEdit()
        self.entity_name_line_edit.setStyleSheet(
            """
                .QLineEdit{
                    background-color: rgb(80, 80, 80);
                    border: 1px solid rgb(10, 10, 10);
                    border-radius: 5px;
                    padding: 3px;
                    padding-left: 2px;
                }"""
        )
        first_layout.addWidget(self.entity_name_label)
        first_layout.addWidget(self.entity_name_line_edit)

        second_layout: QHBoxLayout = QHBoxLayout()
        second_widget: QWidget = QWidget()
        second_widget.setStyleSheet(
            """
            .QPushButton{background-color: rgb(80, 80, 80);
                        border: 2px solide rgb(10, 10, 10);
                        border-radius: 5px;
                        padding: 5px;}
            .QPushButton::pressed{background-color: rgb(50, 50, 50);}
            """
        )
        second_widget.setLayout(second_layout)
        main_layout.addWidget(second_widget)

        create_btn: QPushButton = QPushButton("Create")
        cancel_btn: QPushButton = QPushButton("Cancel")
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        second_layout.addItem(spacer)
        second_layout.addWidget(create_btn)
        second_layout.addWidget(cancel_btn)

        create_btn.clicked.connect(self.create_entity)
        cancel_btn.clicked.connect(self.cancel_dialog)

    def create_entity(self) -> None:
        if self.entity_name_line_edit.text() == "":
            return
        self.infos["name"] = self.entity_name_line_edit.text()
        self.accept()

    def cancel_dialog(self) -> None:
        self.cancel = True
        self.reject()
