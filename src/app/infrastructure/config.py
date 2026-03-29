from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "post-trade-settlement-sim"
    environment: str = "dev"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/settlement"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="PTS_")


settings = Settings()
