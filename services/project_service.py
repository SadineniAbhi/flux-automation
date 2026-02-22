from sqlmodel import Session
from exceptions.project_exceptions import ProjectNotFoundException
from models.project import Project
from repositories.project_repository import ProjectRepository
from schemas.project_schema import CreateProjectRequest


class ProjectService:
    def __init__(self, session: Session, user_id: str):
        self.user_id = user_id
        self.session = session
        self.project_repository = ProjectRepository(user_id, session)

    def create_project(self, request: CreateProjectRequest) -> Project:
        project = Project(
            user_id=self.user_id,
            name=request.name,
            description=request.description,
            helm_chart_github_url=request.helm_chart_github_url,
            chart_path=request.chart_path,
        )
        return self.project_repository.create_project(project)

    def get_projects(self) -> list[Project]:
        projects = self.project_repository.get_projects_by_user_id()
        if len(projects) == 0:
            raise ProjectNotFoundException(f"No projects found for user_id: {self.user_id}")
        return projects
