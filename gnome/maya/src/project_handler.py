import os
from src.maya_file_handler import save_maya_file, open_maya_scene, get_scene
import time
import json


class ProjectHandler:
    def __init__(self, project_path):
        self.project_path: str = project_path
        self.software_path: dict = {"maya": "scenes"}
        self.init_project_folders()

    def init_project_folders(self) -> None:
        os.makedirs(self.project_path, exist_ok=True)

    def create_entity_folders(self, entity_type: str, entity_name: str) -> None:
        entity_path = os.path.join(self.project_path, entity_type, entity_name)
        os.makedirs(entity_path, exist_ok=True)

    def create_department_folder(
        self, entity_type: str, entity_name: str, department_name: str
    ) -> None:
        department_path = os.path.join(
            self.project_path, entity_type, entity_name, department_name
        )
        os.makedirs(department_path, exist_ok=True)

    def get_entities(self, entities_type: str) -> list[str]:
        entities_path = os.path.join(self.project_path, entities_type)
        if not os.path.exists(entities_path):
            return []
        entities = [f for f in os.listdir(entities_path)]
        return entities

    def get_departments(self, entity_type: str, entity_name: str) -> list[str]:
        department_path = os.path.join(self.project_path, entity_type, entity_name)
        if not os.path.exists(department_path):
            return []
        departments = [f for f in os.listdir(department_path)]
        return departments

    def create_new_version(
        self, entity_type: str, entity_name: str, department: str, comment: str
    ) -> None:
        department_path = os.path.join(
            self.project_path, entity_type, entity_name, department
        )
        maya_path = os.path.join(department_path, "maya")
        os.makedirs(maya_path, exist_ok=True)
        files_infos_path: str = os.path.join(maya_path, "infos.json")
        if not os.path.exists(files_infos_path):
            with open(files_infos_path, "w") as f:
                f.write(r"{}")
        save_maya_file(maya_path, entity_name, comment)

    def get_files(
        self, entity_type: str, entity_name: str, department: str
    ) -> list[dict[str, str]]:
        files_path = os.path.join(
            self.project_path, entity_type, entity_name, department
        )

        files: list[dict[str, str]] = []
        for dir in os.listdir(files_path):
            if not os.path.isdir(os.path.join(files_path, dir)):
                continue
            scenes_path = os.path.join(files_path, dir, self.software_path[dir])
            if not os.path.exists(scenes_path):
                continue
            for file in os.listdir(scenes_path):
                file_path: str = os.path.join(scenes_path, file)
                if os.path.isdir(file_path):
                    continue
                if not (file_path.endswith(".ma") or file_path.endswith(".mb")):
                    continue
                file_date: str = time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.strptime(time.ctime(os.path.getctime(file_path))),
                )
                file_version: str = file[
                    -6 - file[::-1].index(".") : -file[::-1].index(".") - 1
                ]
                infos_path = os.path.join(scenes_path, "infos.json")
                comment = ""
                if os.path.exists(infos_path):
                    with open(infos_path, "r") as f:
                        comments = json.load(f)
                        version = str(int(file_version[1:]))
                        if version in comments:
                            comment = comments[version]["comment"]
                file_infos: dict[str, str] = {
                    "software": dir,
                    "version": file_version,
                    "comment": comment,
                    "date": file_date,
                    "path": file_path,
                }
                files.append(file_infos)
        return files

    def open_file(self, file: dict[str, str]):
        software: str = file["software"]
        if software == "maya":
            open_maya_scene(file["path"])

    def export_event(self) -> str:
        scene_path: str = get_scene().replace("/", "\\")
        if not scene_path:
            return "scene_not_saved_in_project"
        infos: dict[str, str] = self.get_file_project_infos(scene_path)
        if infos == {}:
            return "scene_not_saved_in_project"

        print(infos)
        return "success"

    def get_file_project_infos(self, file_path: str) -> dict[str, str]:
        infos: dict[str, str] = {}
        if not file_path.startswith(self.project_path):
            return infos
        parts = file_path[len(self.project_path) :].split(os.sep)
        infos["entity_type"] = parts[1]
        infos["entity_name"] = parts[2]
        infos["department"] = parts[3]
        infos["software"] = parts[4]
        return infos
