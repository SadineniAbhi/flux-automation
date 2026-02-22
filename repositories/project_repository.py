from datetime import datetime, UTC
from sqlmodel import Session, select
from models.project import Project


class ProjectRepository:

    def __init__(self, user_id: str, session: Session):
        self.user_id = user_id
        self.session = session

    def create_project(self, project: Project) -> Project:
        project = Project.model_validate(project)
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def get_project_by_id(self, project_id: int) -> Project | None:
        project = self.session.get(Project, project_id)
        if project is None or project.user_id != self.user_id:
            return None
        return project

    def get_projects_by_user_id(self) -> list[Project]:
        statement = select(Project).where(Project.user_id == self.user_id)
        return list(self.session.exec(statement).all())

    def update_project(self, project_id: int, data: Project) -> Project | None:
        data = Project.model_validate(data)
        project = self.session.get(Project, project_id)
        if project is None or project.user_id != self.user_id:
            return None
        project.name = data.name.strip()
        project.description = data.description.strip()
        project.helm_chart_github_url = data.helm_chart_github_url.strip()
        project.chart_path = data.chart_path.strip()
        project.updated_at = datetime.now(UTC)
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def delete_project(self, project_id: int) -> bool:
        project = self.session.get(Project, project_id)
        if project is None or project.user_id != self.user_id:
            return False
        self.session.delete(project)
        self.session.commit()
        return True