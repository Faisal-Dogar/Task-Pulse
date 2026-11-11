from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Alembic Config object (alembic.ini file se settings load karta hai)
config = context.config

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- TaskPulse Setup ---
# Apne app ke settings aur models import karo taake:
# 1. DATABASE_URL .env file se milega
# 2. target_metadata se Alembic ko pata chalega ke kaunsi tables manage karni hain
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.db.base import Base

# Tamam models import karna zaroori hai taake Alembic unhe detect kar sake
import app.models  # noqa: F401

# Database URL ko alembic.ini ki URL se override karo (using our .env settings)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Yeh batata hai ke kaunse models se migration generate karni hai
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Offline mode: Database connection ke baghair sirf SQL script generate karta hai.
    Useful jab aap SQL file export karna chahein.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Online mode: Database se seedha connect ho kar migrations apply karta hai.
    Yeh normal use case hai.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
