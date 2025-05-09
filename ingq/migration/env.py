import importlib
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

import db.database as database
from core.setting.load_env import DATABASE_URL_ALEMBIC

DB_URL = DATABASE_URL_ALEMBIC


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

if DB_URL:
    config.set_main_option("sqlalchemy.url", DB_URL)


def load_all_models():
    importlib.import_module("user.infra.db_models.user")
    importlib.import_module("book.infra.db_models.book")
    importlib.import_module("bookmark.infra.db_models.bookmark")
    importlib.import_module("story.infra.db_models.story")
    importlib.import_module("illust.infra.db_models.illust")
    importlib.import_module("choice.infra.db_models.choice")


# 모델 로드 실행
load_all_models()

# set target metadata
target_metadata = database.Base.metadata

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
