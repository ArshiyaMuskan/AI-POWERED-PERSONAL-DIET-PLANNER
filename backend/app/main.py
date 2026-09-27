from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .database import Base, engine
from .routes import auth_routes, profile_routes, plan_routes, file_routes

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Educational cloud computing project for personalized wellness meal-plan examples.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(profile_routes.router)
app.include_router(plan_routes.router)
app.include_router(file_routes.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": settings.app_name}
