from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from mangum import Mangum

from src.config import app_configs, settings
from src.resume_parser.router import router as jury_router

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)


@app.get("/api/v1/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/ping")
async def root():
    return {"message": "Ping successful"}


app.include_router(jury_router, prefix="/api/v1/resume-parser", tags=["Process Resume Calls"])
handler = Mangum(app=app)
