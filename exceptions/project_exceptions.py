from typing import Any

class ProjectNotFoundException(Exception):
    def __init__(self, project_id: Any):
        self.project_id = project_id
        super().__init__(f"Project with id {project_id} not found")
