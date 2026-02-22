from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException
from exceptions.project_exceptions import ProjectNotFoundException
from schemas.project_schema import CreateProjectRequest, ProjectResponse
from services.project_service import ProjectService
from utils.auth import auth_dependency, Claims
from utils.db import get_db_session

router = APIRouter(prefix="/project", tags=["projects"])


@router.post("/create", response_model=ProjectResponse, status_code=201)
def create_project(
    request: CreateProjectRequest,
    claims: Claims = Depends(auth_dependency),
    db_session: Session = Depends(get_db_session)
):
    user_id: str = claims["sub"]
    project_service = ProjectService(user_id=user_id, session=db_session)
    project = project_service.create_project(request)
    return project


@router.get("/list", response_model=list[ProjectResponse])
def get_projects(
    claims: Claims = Depends(auth_dependency),
    db_session: Session = Depends(get_db_session)
):
    user_id: str = claims["sub"]
    try:
        return ProjectService(user_id=user_id, session=db_session).get_projects()
    except ProjectNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))