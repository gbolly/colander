import os
import json
from typing import Any, Union, List

from pydantic import PostgresDsn, ValidationError, Field, validator, AnyHttpUrl
from pydantic_settings import BaseSettings

from src.constants import Environment

cors_origin = os.environ.get("CORS_ORIGINS", "").split(",")
env_name = os.environ.get("ENV_NAME", "PRODUCTION")

class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    SITE_DOMAIN: str = "myapp.com"
    ENVIRONMENT: Environment = Environment[env_name]
    CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = Field(..., env="CORS_ORIGINS")
    CORS_HEADERS: list[str] = ["*"]
    APP_VERSION: str = "1"

    @validator("CORS_ORIGINS", pre=True)
    def _assemble_cors_origins(cls, cors_origins):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins

# database = PostgresDsn(
#     scheme="postgresql",
#     username=os.environ.get("DB_NAME"),
#     password=os.environ.get("PASSWORD"),
#     host=os.environ.get("HOST"),
#     # path=cls.db,
# )
try:
    settings = Config(
        DATABASE_URL='postgres://os.environ.get("DB_NAME"):os.environ.get("PASSWORD")@os.environ.get("HOST"):5432'
    )
except ValidationError as e:
    print(e)


app_configs: dict[str, Any] = {"title": "Twinkle API", "debug": True}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
