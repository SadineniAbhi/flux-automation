from datetime import datetime
from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=500)
    helm_chart_github_url: str = Field(min_length=1, max_length=300)
    chart_path: str = Field(min_length=1, max_length=100)


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    helm_chart_github_url: str
    chart_path: str
    created_at: datetime
    updated_at: datetime
