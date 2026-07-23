from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    API_VERSION: str
    DEBUG: bool
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    AWS_SECRET_ACCESS_KEY: str
    AWS_ACCESS_KEY_ID: str
    AWS_REGION_NAME: str
    AWS_DEMO_MODE: bool
    BEDROCK_MODEL_ID: str
    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()