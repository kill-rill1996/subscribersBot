from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    channel_id: str


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8"
)

