import os
from typing import Any

from pydantic import PostgresDsn, RedisDsn, model_validator, ValidationError
from pydantic_settings import BaseSettings

from src.constants import Environment


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    SITE_DOMAIN: str = "myapp.com"
    ENVIRONMENT: Environment = Environment.PRODUCTION
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    CORS_HEADERS: list[str] = ["*"]
    APP_VERSION: str = "1"

    # @model_validator(mode="after")
    # def validate_sentry_non_local(self) -> "Config":
    #     if self.ENVIRONMENT.is_deployed and not self.SENTRY_DSN:
    #         raise ValueError("Sentry is not set")

    #     return self


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


app_configs: dict[str, Any] = {"title": "App API", "debug": True}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
