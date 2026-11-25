from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Импортируем наши настройки и модели
from app.core.config import settings
from app.db.base import Base

# Важно: импортируем ВСЕ модели, чтобы Alembic их видел (добавили Category)
import app.models.category
import app.models.product

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем URL базы данных (убираем +aiosqlite, так как Alembic работает синхронно)
config.set_main_option("sqlalchemy.url", settings.database_url.replace("+aiosqlite", ""))

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # <-- Добавили для поддержки SQLite
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True  # <-- Добавили для поддержки SQLite
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()