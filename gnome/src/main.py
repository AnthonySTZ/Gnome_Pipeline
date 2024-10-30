import sys
import os
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication
from ui_handler import MainWindow
from project_handler import ProjectHandler


def run() -> None:
    load_dotenv()
    project_path: str = os.getenv("PROJECT_PATH")
    project: ProjectHandler = ProjectHandler(project_path)
    app: QApplication = QApplication([])
    window: MainWindow = MainWindow(project)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
