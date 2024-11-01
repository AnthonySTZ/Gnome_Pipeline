import os
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
        departments = []
        for f in os.listdir(department_path):
            if not os.path.isdir(os.path.join(department_path, f)):
                continue
            departments.append(f)
        return departments

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
            if dir not in self.software_path:
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
                }
                files.append(file_infos)
        return files
