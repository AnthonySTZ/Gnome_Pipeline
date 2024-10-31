import os
import sys
from maya import OpenMayaUI as omui
import maya.cmds as cmds


def run() -> None:
    plugin_path = os.path.join(os.environ["GNOME_PATH"], "maya")

    sys.path.insert(0, plugin_path)

    from importlib import reload
    import src.plugin_handler as plugin_handler
    import src.project_handler as project_handler
    import src.ui_handler as ui_handler
    import src.dialogs as dialogs

    reload(project_handler)
    reload(ui_handler)
    reload(plugin_handler)
    reload(dialogs)
    plugin_handler.openWindow("Pipeline")


run()
