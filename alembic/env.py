# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from sqlalchemy.engine.url import URL
from app.config import get_settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.core.db.base import Base
from app.core.db.models import (
    User,
    League,
    BigGoals,
    Goals,
    BadHabits,
    BadHabitStats,
    Meds,
    Tasks,
    Roadmap,
    Classes,
    Notes,
    Information,
)

target_metadata = Base.metadata


def get_database_url():
    """Получаем URL для Alembic (синхронный драйвер)"""
    settings = get_settings()

    if settings.DEV_MODE:
        # Для SQLite используем синхронный драйвер
        return "sqlite:///./dev.db"
    else:
        # Для PostgreSQL используем синхронный драйвер psycopg2
        return f"postgresql+psycopg2://{settings.PROD_DB_USER}:{settings.PROD_DB_PASSWORD}@{settings.PROD_DB_HOST}:{settings.PROD_DB_PORT}/{settings.PROD_DB_NAME}"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Получаем URL БД
    db_url = get_database_url()

    # Создаем конфигурацию для engine
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = db_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Для лучшего сравнения типов
            compare_server_default=True  # Для сравнения дефолтных значений
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
