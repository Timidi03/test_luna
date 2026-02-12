from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from src.models.organization import Organization
from src.models.phone import Phone
from src.models.activity import Activity
from src.models.base import Base
from src.models.building import Building
from src.models.assosiation_tables import OrganizationActivity

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

load_dotenv()
DATABASE_URL = os.getenv("DB_URL")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Миграции в режиме offline (без подключения к БД)"""
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Миграции в режиме online (с async движком)"""

    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(run_migrations_sync)
        await connectable.dispose()

    asyncio.run(do_run_migrations())


def run_migrations_sync(connection: Connection):
    """Функция для sync Alembic API"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # отслеживает изменение типов колонок
    )
    with context.begin_transaction():
        context.run_migrations()


# -------------------------------
# Выбор режима
# -------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()