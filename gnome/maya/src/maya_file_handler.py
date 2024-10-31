import os
import maya.cmds as cmds
import json


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
