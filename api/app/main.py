from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.status import router as status_router
from app.routes.projetos import router as projetos_router


app = FastAPI(title="Homelab API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://guibarbosa.me"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(status_router)
app.include_router(projetos_router)

@app.get("/")
def root():
    return {"message": "Homelab API is running"}
