import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from src.core.config import config
from src.core.database import AsyncSessionLocal
from src.core.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


async def init_db():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(text("SELECT 1 FROM organizations LIMIT 1;"))
            row = result.first()
            if row:
                logger.info("The database is already full")
                return
        except Exception:
            logger.info(
                "The database is empty or the organizations table does not exist. Filling it out..."
            )

        if os.path.exists(config.INIT_DB_FILE):
            with open(config.INIT_DB_FILE, "r", encoding="utf-8") as f:
                commands = f.read().split(";")
                for command in commands:
                    await session.execute(text(command))
            print("The database is full from init_db.sql")
        else:
            print(f"File {config.INIT_DB_FILE} not found")
