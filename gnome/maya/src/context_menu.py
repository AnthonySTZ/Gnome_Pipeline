from PySide2.QtWidgets import QWidget, QMenu
from PySide2.QtCore import QPoint


def create_list_context_menu(
    list_view: QWidget, dict_function: dict[str, callable], parent, position: QPoint
) -> None:
    index = list_view.indexAt(position)
    if not index.isValid():  # If no item is clicked
        menu: QMenu = QMenu(parent)
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
        for key, value in dict_function.items():
            menu.addAction(key).triggered.connect(value)

        # Display the menu at the mouse position
        menu.exec_(list_view.mapToGlobal(position))
