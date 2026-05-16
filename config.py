from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DEBUG: bool
    TIMEZONE: str

    DJANGO_SECRET_KEY: str

    DJANGO_ALLOWED_HOSTS: list[str]
    CSRF_TRUSTED_ORIGINS: list[str]

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str


    model_config = SettingsConfigDict(env_file=".env")


config = Config()
