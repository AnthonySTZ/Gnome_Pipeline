import os
import sys
from maya import OpenMayaUI as omui


def run() -> None:
    plugin_path = os.path.join(os.environ["GNOME_PATH"], "maya")

    sys.path.insert(0, plugin_path)

    from importlib import reload
    import src.plugin_handler as plugin_handler
    import src.project_handler as project_handler
    import src.ui_handler as ui_handler
    import src.dialogs as dialogs
    import src.maya_file_handler as maya_file_handler
    import src.usd_handler as usd_handler

    reload(usd_handler)
    reload(maya_file_handler)
    reload(dialogs)
    reload(project_handler)
    reload(ui_handler)
    reload(plugin_handler)
    plugin_handler.openWindow("Pipeline")


run()
