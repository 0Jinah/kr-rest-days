import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DATA_GO_API_KEY: str = os.getenv("DATA_GO_API_KEY", "")
    API_ENDPOINT: str = "https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"

    class Config:
        env_file = ".env"

settings = Settings()
