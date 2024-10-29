import sys
from PySide6.QtWidgets import QApplication
from ui_handler import MainWindow


def run() -> None:
    app: QApplication = QApplication([])
    window: MainWindow = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
