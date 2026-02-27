from fastapi import APIRouter
from app.services.docker import get_containers_status

router = APIRouter()


@router.get("/status")
def status():
    return get_containers_status()
