import functools

from pydantic import BaseSettings, Extra, Field

origins = [
    "http://127.0.0.1:8000/",
]


class Settings(BaseSettings):
    # Back-end settings
    DEBUG: bool = Field(default=False)
    SHOW_SETTINGS: bool = Field(default=False)
    HOST: str = Field(default="127.0.0.1")
    PORT: str = Field(default="8000")
    SERVER_URL: str = Field(default="http://127.0.0.1:8000")
    TRUSTED_HOSTS: list[str] = Field(default=["*"])
    # CORS settings
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_HEADERS: list[str] = Field(
        default=[
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
        ]
    )
    CORS_ALLOW_METHODS: list[str] = Field(
        default=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"]
    )
    CORS_ALLOW_ORIGINS: list[str] = Field(default=origins)
    # Database settings
    DATABASE_URL: str = Field()

    class Config(BaseSettings.Config):
        extra = Extra.ignore
        env_file = ".env"
        env_file_encoding = "UTF-8"
        env_nested_delimiter = "__"


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()


Settings: Settings = get_settings()
