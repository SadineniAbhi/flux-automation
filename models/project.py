from datetime import datetime, UTC
from sqlmodel import Field, SQLModel

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=120)
    name: str = Field(index=True, max_length=120)
    description: str  = Field(max_length=500)
    helm_chart_github_url: str = Field(max_length=300)
    chart_path: str = Field(max_length=100)
    created_at: datetime = Field(default_factory= lambda: datetime.now(UTC), nullable=False)
    updated_at: datetime = Field(default_factory= lambda: datetime.now(UTC), nullable=False)