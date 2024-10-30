import os


class ProjectHandler:
    def __init__(self, project_path):
        self.project_path: str = project_path

        self.init_project_folders()

    def init_project_folders(self) -> None:
        os.makedirs(self.project_path, exist_ok=True)

    def create_entity_folders(self, entity_name: str) -> None:
        entity_path = os.path.join(self.project_path, entity_name)
        os.makedirs(entity_path, exist_ok=True)

    def create_department_folder(self, entity_name: str, department_name: str) -> None:
        department_path = os.path.join(self.project_path, entity_name, department_name)
        os.makedirs(department_path, exist_ok=True)
