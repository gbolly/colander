from contextlib import asynccontextmanager
from typing import AsyncGenerator

# import redis.asyncio as aioredis
# import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# from src import redis
from src.config import app_configs, settings

# from src.external_service.router import router as external_service_router
from src.resume_parser.router import router as jury_router


# @asynccontextmanager
# async def lifespan(_application: FastAPI) -> AsyncGenerator:
#     # Startup
#     pool = aioredis.ConnectionPool.from_url(
#         str(settings.REDIS_URL), max_connections=10, decode_responses=True
#     )
#     redis.redis_client = aioredis.Redis(connection_pool=pool)

#     yield

#     if settings.ENVIRONMENT.is_testing:
#         return
#     # Shutdown
#     await pool.disconnect()


app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    # allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

# if settings.ENVIRONMENT.is_deployed:
#     sentry_sdk.init(
#         dsn=settings.SENTRY_DSN,
#         environment=settings.ENVIRONMENT,
#     )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(jury_router, prefix="/resume-parser", tags=["Process Resume Calls"])