from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import text

from alembic import context
import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add the root of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Base from your database module
from api.dependencies.database import Base  # ✅ This is where Base is defined
from api.models import (
    orders,
    order_details,
    menu_item,
    sandwiches,
    review,
    recipes,
    customer,
    ingredient,
    promo_code,
)

# ✅ Import all models so Alembic can detect them


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

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

    def cleanup_resources_leftovers(connection):
        try:
            # Check if resources table exists
            result = connection.exec_driver_sql(
                text(
                    "SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'resources'"
                )
            )
            exists = result.scalar()
            if not exists:
                return
        except Exception:
            return

        try:
            # Find foreign key constraints from recipes referencing resources
            result = connection.exec_driver_sql(
                text(
                    """
                    SELECT CONSTRAINT_NAME
                    FROM information_schema.KEY_COLUMN_USAGE
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME = 'recipes'
                      AND REFERENCED_TABLE_NAME = 'resources'
                    """
                )
            )
            fkeys = [row[0] for row in result]
        except Exception:
            fkeys = []

        for fk in fkeys:
            try:
                connection.exec_driver_sql(
                    text(f"ALTER TABLE recipes DROP FOREIGN KEY {fk}")
                )
            except Exception:
                pass

        try:
            # Check if resource_id column exists in recipes
            result = connection.exec_driver_sql(
                text(
                    "SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'recipes' AND COLUMN_NAME = 'resource_id'"
                )
            )
            col_exists = result.scalar()
            if col_exists:
                try:
                    connection.exec_driver_sql(
                        text("ALTER TABLE recipes DROP COLUMN resource_id")
                    )
                except Exception:
                    pass
        except Exception:
            pass

        try:
            # Drop resources table
            connection.exec_driver_sql(
                text("DROP TABLE resources")
            )
        except Exception:
            pass

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
        cleanup_resources_leftovers(connection)
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
