from fastapi import APIRouter

router = APIRouter(tags=["default"])

@router.get("/")
def root():
    return {"message": "healthy"}

