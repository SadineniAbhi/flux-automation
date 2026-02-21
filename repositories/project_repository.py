from datetime import datetime, UTC

from sqlmodel import Session, select

from models.project import Project
from utils.db import engine


class ProjectRepository:

    @staticmethod
    def create_project(project: Project) -> Project:
        with Session(engine) as session:
            session.add(project)
            session.commit()
            session.refresh(project)
            return project

    @staticmethod
    def get_project_by_id(project_id: int) -> Project | None:
        with Session(engine) as session:
            return session.get(Project, project_id)

    @staticmethod
    def get_projects_by_user_id(user_id: str) -> list[Project]:
        with Session(engine) as session:
            statement = select(Project).where(Project.user_id == user_id)
            return list(session.exec(statement).all())

    @staticmethod
    def update_name(project_id: int, name: str) -> Project | None:
        with Session(engine) as session:
            project = session.get(Project, project_id)
            if project is None:
                return None
            project.name = name
            project.updated_at = datetime.now(UTC)
            session.add(project)
            session.commit()
            session.refresh(project)
            return project

    @staticmethod
    def update_description(project_id: int, description: str) -> Project | None:
        with Session(engine) as session:
            project = session.get(Project, project_id)
            if project is None:
                return None
            project.description = description
            project.updated_at = datetime.now(UTC)
            session.add(project)
            session.commit()
            session.refresh(project)
            return project

    @staticmethod
    def update_helm_chart_github_url(project_id: int, helm_chart_github_url: str) -> Project | None:
        with Session(engine) as session:
            project = session.get(Project, project_id)
            if project is None:
                return None
            project.helm_chart_github_url = helm_chart_github_url
            project.updated_at = datetime.now(UTC)
            session.add(project)
            session.commit()
            session.refresh(project)
            return project

    @staticmethod
    def update_chart_path(project_id: int, chart_path: str) -> Project | None:
        with Session(engine) as session:
            project = session.get(Project, project_id)
            if project is None:
                return None
            project.chart_path = chart_path
            project.updated_at = datetime.now(UTC)
            session.add(project)
            session.commit()
            session.refresh(project)
            return project

    @staticmethod
    def delete_project(project_id: int) -> bool:
        with Session(engine) as session:
            project = session.get(Project, project_id)
            if project is None:
                return False
            session.delete(project)
            session.commit()
            return True
