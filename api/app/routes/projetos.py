from fastapi import APIRouter
from app.services.github import fetch_pinned_repos

router = APIRouter()


@router.get("/projetos")
def projetos():
    return fetch_pinned_repos()
