import functools

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

origins = [
    "http://127.0.0.1:8000/",
]


class Settings(BaseSettings):
    # Back-end settings
    DEBUG: bool = Field(default=False, exclude=True)
    SHOW_SETTINGS: bool = Field(default=False, exclude=True)
    HOST: str = Field(default="127.0.0.1", exclude=True)
    PORT: str = Field(default="8000", exclude=True)
    SERVER_URL: str = Field(default="http://127.0.0.1:8000", exclude=True)
    TRUSTED_HOSTS: list[str] = Field(default=["*"], exclude=True)
    # CORS settings
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, exclude=True)
    CORS_ALLOW_HEADERS: list[str] = Field(
        default=[
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
        ],
        exclude=True,
    )
    CORS_ALLOW_METHODS: list[str] = Field(
        default=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"], exclude=True
    )
    CORS_ALLOW_ORIGINS: list[str] = Field(default=origins, exclude=True)
    # Database settings
    DATABASE_URL: str = Field(exclude=True)
    TEST_DATABASE_URL: str = Field(exclude=True)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="UTF-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()


Settings: Settings = get_settings()
