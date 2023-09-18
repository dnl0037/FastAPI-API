from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_username: str
    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    secret_key: str
    algorithm: str
    token_expiration_time: int

    class Config:
        env_file = ".env"


Settings = Settings()
