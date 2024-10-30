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
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QStyle,
)

from PySide6 import QtGui, QtCore


class CreateEntityDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.infos: dict[str, str] = {}

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
        spacer: QSpacerItem = QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
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
        self.reject()


class NoFocusDelegate(QStyledItemDelegate):
    def paint(
        self,
        painter: QtGui.QPainter,
        option: QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        itemOption = QStyleOptionViewItem(option)
        if option.state & QStyle.State_HasFocus:
            itemOption.state = itemOption.state ^ QStyle.State_HasFocus
        super().paint(painter, itemOption, index)


class CreateDepartmentDialog(QDialog):
    def __init__(self, entity_type: str, parent=None):
        super().__init__(parent)
        self.entity_type = entity_type
        self.departments: dict[str, str] = {
            "assets": {
                "Concept": "cpt",
                "Modeling": "mod",
                "Surfacing": "surf",
                "Rigging": "rig",
                "Layout": "lay",
                "Animation": "anim",
                "Fx": "fx",
                "CharacterFx": "cfx",
                "Lighting": "light",
            },
            "shots": {"Layout": "lay", "Lighting": "light", "SetDressing": "dress"},
        }

        self.setup_ui()
        self.infos: dict[str, str] = {}

    def setup_ui(self) -> None:
        self.setWindowTitle("Create Entity")
        self.resize(300, 600)

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

        self.files_table_widget: QTableWidget = QTableWidget()
        first_layout.addWidget(self.files_table_widget)
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
            .QTableWidget::item:focus {border : 0;}
            """
        )
        headers: list[str] = ["Department", "Abbreviation"]
        self.files_table_widget.setColumnCount(len(headers))
        self.files_table_widget.setHorizontalHeaderLabels(headers)
        self.files_table_widget.horizontalHeader().setStretchLastSection(True)
        self.files_table_widget.verticalHeader().setVisible(False)
        self.files_table_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.files_table_widget.setItemDelegate(NoFocusDelegate())
        self.files_table_widget.setRowCount(len(self.departments[self.entity_type]))
        for i, (department, abbreviation) in enumerate(
            self.departments[self.entity_type].items()
        ):
            self.files_table_widget.setItem(i, 0, QTableWidgetItem(department))
            self.files_table_widget.setItem(i, 1, QTableWidgetItem(abbreviation))

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
        spacer: QSpacerItem = QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        second_layout.addItem(spacer)
        second_layout.addWidget(create_btn)
        second_layout.addWidget(cancel_btn)

        create_btn.clicked.connect(self.create_entity)
        cancel_btn.clicked.connect(self.cancel_dialog)

    def create_entity(self) -> None:
        selection = self.files_table_widget.selectionModel()
        if not selection.hasSelection():
            return
        department = self.files_table_widget.item(
            selection.selectedRows()[0].row(), 1
        ).text()
        self.infos["department"] = department
        self.accept()

    def cancel_dialog(self) -> None:
        self.reject()
