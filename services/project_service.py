from models.project import Project
from repositories.project_repository import ProjectRepository
from schemas.project_schema import CreateProjectRequest


class ProjectService:

    @staticmethod
    def create_project(user_id: str, request: CreateProjectRequest) -> Project:
        project = Project(
            user_id=user_id,
            name=request.name,
            description=request.description,
            helm_chart_github_url=request.helm_chart_github_url,
            chart_path=request.chart_path,
        )
        return ProjectRepository.create_project(project)
