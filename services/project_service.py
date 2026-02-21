from exceptions.project_exceptions import ProjectNotFoundException
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

    @staticmethod
    def get_projects(user_id: str) -> list[Project]:
        projects = ProjectRepository.get_projects_by_user_id(user_id)
        if len(projects) == 0:
            raise ProjectNotFoundException(f"No projects found for user_id: {user_id}")
        return projects
