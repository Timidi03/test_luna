import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URL = os.getenv("DB_URL")
    INIT_DB_FILE = os.getenv("INIT_DB_FILE")
    API_KEY = os.getenv("API_KEY")


config = Config()
