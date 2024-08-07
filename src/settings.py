from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_PORT: int
    REDIS_HOST: str


settings = Settings()
