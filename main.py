from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.config_loader import settings
from app.organization.routes import building_router, activity_router, organization_router

openapi_tags = [
    {"name": "Buildings", "description": "Building operations"},
    {"name": "Activities", "description": "Activity operations"},
    {"name": "Organizations", "description": "Organization operations"},
    {"name": "Health Checks", "description": "Application health checks"},
]

app = FastAPI(openapi_tags=openapi_tags)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(building_router, prefix="/api/v1")
app.include_router(activity_router, prefix="/api/v1")
app.include_router(organization_router, prefix="/api/v1")


@app.get("/health", tags=["Health Checks"])
async def health_check():
    return {"health": "true"}

