from src.ui_handler import MainWindow
from src.project_handler import ProjectHandler
from maya import OpenMayaUI as omui
import maya.cmds as cmds
import os
from shiboken2 import wrapInstance
from PySide2.QtWidgets import QApplication, QWidget, QDialog


def create_window(dialog: MainWindow):
    if QApplication.instance():
        # Id any current instances of tool and destroy
        for win in QApplication.allWindows():
            if "SaveAs" in win.objectName():  # update this name to match name below
                win.destroy()

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
    # TODO: Change the project path
    project_path: str = os.environ["PROJECT_PATH"]
    project: ProjectHandler = ProjectHandler(project_path)
    dialog.window = dialog(project, parent=mayaMainWindow)
    dialog.window.setObjectName(
        str(dialog.__name__)
    )  # code above uses this to ID any existing windows
    dialog.window.setWindowTitle("Gnome")
    dialog.window.show()


def openWindow(type: str):
    """
    ID Maya and attach tool window.
    """
    if type == "Pipeline":
        create_window(MainWindow)
