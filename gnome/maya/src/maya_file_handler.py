import os
import maya.cmds as cmds
import json
from PySide2.QtWidgets import QMessageBox


def create_maya_project(project_path):

    default_folders = [
        "scenes",
        "images",
        "sourceimages",
        "renderData",
        "clips",
        "sound",
        "scripts",
        "assets",
        "autosave",
    ]

    # Create the main project directory if it doesn't exist
    if not os.path.exists(project_path):
        os.makedirs(project_path)

    # Set the project in Maya
    cmds.workspace(project_path, openWorkspace=True)

    # Create the default Maya project folders in both Maya and on the file system
    for folder in default_folders:
        # Set Maya workspace rule
        cmds.workspace(fileRule=[folder, folder])
        # Create folder on the filesystem if it doesn't exist
        folder_path = os.path.join(project_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Save the workspace settings to enforce the changes
    cmds.workspace(saveWorkspace=True)


def save_maya_file(path: str, filename: str, comment: str) -> None:
    version = 1
    file_path = os.path.join(path, "scenes")

    for file in os.listdir(file_path):
        if file.startswith(filename) and (file.endswith(".ma") or file.endswith(".mb")):
            version_number = int(file[len(filename) + 1 : -3])
            if version_number > version:
                version = version_number
    version += 1
    create_maya_project(path)
    filename += "v" + str(version).zfill(4)
    scene_path = os.path.join(file_path, filename)
    cmds.file(rename=scene_path)
    cmds.file(save=True)
    infos_path = os.path.join(file_path, "infos.json")
    add_comment_to_file(infos_path, version, comment)


def add_comment_to_file(file_path: str, version: int, comment: str) -> None:
    with open(file_path, "r") as f:
        data = json.load(f)
    data[version] = {"comment": comment}
    with open(file_path, "w") as f:
        json.dump(data, f)


def open_maya_scene(file_path: str):
    if cmds.file(q=True, modified=True):
        res: str = cmds.confirmDialog(
            title="Unsaved Changes",
            message="You have unsaved changes. Do you want to save them?",
            button=["Save", "Discard", "Cancel"],
            defaultButton="Save",
            cancelButton="Cancel",
            dismissString="Cancel",
        )
        if res == "Save":
            current_scene: str = cmds.file(q=True, sceneName=True)
            if current_scene:
                cmds.file(save=True)
            else:
                save_path = cmds.fileDialog2(
                    fileFilter="Maya Binary (*.mb);;Maya ASCII (*.ma)",
                    dialogStyle=2,
                    fileMode=0,
                )
                if save_path:
                    cmds.file(rename=save_path[0])
                    cmds.file(save=True, type="mayaBinary")
                else:
                    return  # User cancelled the save as dialog
        elif res == "Cancel":
            return
        elif res == "Discard":
            try:
                cmds.file(file_path, open=True, force=True)
                return
            except RuntimeError as e:
                QMessageBox.warning("Error", str(e))
                return

    try:
        cmds.file(file_path, open=True)
    except RuntimeError as e:
        QMessageBox.warning("Error", str(e))


def get_scene() -> str:
    file_path: str = cmds.file(query=True, sceneName=True)
    return file_path


def export(file_path: str, filename: str, format: str, export_selection: bool) -> str:
    if export_selection:
        # Get a list of selected objects
        selected_objects = cmds.ls(selection=True)

        if len(selected_objects) == 0:
            cmds.warning("Please select and object to export")
            return "No selected"
    else:
        selected_objects = cmds.ls(assemblies=True)

    # Check version
    version = 1
    for file in os.listdir(file_path):
        if file.startswith(filename):
            version_number = int(file[len(filename) + 1 : -3])
            if version_number > version:
                version = version_number
    full_path = os.path.join(
        file_path, filename + "v" + str(version).zfill(4) + format
    ).replace("\\", "/")
    if format == ".abc":
        export_cmd = "-frameRange 1 1"

        # Add each root object's path to the export command
        for obj in selected_objects:
            export_cmd += " -root " + obj

        # Specify the file output path
        export_cmd += " -file '" + full_path + "'"
        print(export_cmd)
        cmds.AbcExport(j=export_cmd)
    return "success"
