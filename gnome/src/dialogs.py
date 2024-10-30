from PySide6.QtWidgets import QDialog, QLabel, QLineEdit


class CreateEntityDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle("Create Entity")
        self.resize(300, 200)

        self.entity_name_label = QLabel("Entity Name:")
        self.entity_name_line_edit = QLineEdit()
