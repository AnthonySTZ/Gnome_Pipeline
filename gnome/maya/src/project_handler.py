import os
from src.maya_file_handler import save_maya_file


class ProjectHandler:
    def __init__(self, project_path):
        self.project_path: str = project_path

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
        self, entity_type: str, entity_name: str, department: str, version_name: str
    ) -> None:
        department_path = os.path.join(
            self.project_path, entity_type, entity_name, department
        )
        maya_path = os.path.join(department_path, "maya")
        os.makedirs(maya_path, exist_ok=True)
        save_maya_file(maya_path, version_name)
