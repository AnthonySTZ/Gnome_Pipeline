import os
import maya.cmds as cmds


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


def save_maya_file(path: str, filename: str) -> None:
    file_path = os.path.join(path, "scenes", filename + "v0001")
    filename = cmds.file(q=True, sn=True)
    if not filename:
        create_maya_project(path)
        cmds.file(rename=file_path)
        cmds.file(save=True)
