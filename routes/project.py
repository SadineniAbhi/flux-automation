from fastapi import APIRouter, Depends

from schemas.project_schema import CreateProjectRequest, ProjectResponse
from services.project_service import ProjectService
from utils.auth import auth_dependency, Claims

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(
    request: CreateProjectRequest,
    claims: Claims = Depends(auth_dependency),
):
    user_id: str = claims["sub"]
    project = ProjectService.create_project(user_id, request)
    return project