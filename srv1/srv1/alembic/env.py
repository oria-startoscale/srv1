"""
Alembic provides for the creation, management, and invocation of change management
scripts for a relational database, using SQLAlchemy as the underlying engine.

This is a Python script that is run whenever the alembic migration tool is invoked.
It contains instructions to configure and generate a SQLAlchemy engine, procure a connection from that engine along
with a transaction, and then invoke the migration engine, using the connection as a source of database connectivity.
"""
from __future__ import absolute_import
from __future__ import with_statement

import os
from logging.config import fileConfig


from alembic import context
import logging
from strato_common.service_utils.db.mysql.setup import Setup as DBSetup
from strato_common.service_utils.db.mysql.model_base import Base as ModelBase


def run_migrations_offline(config, target_metadata):
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine,
    though an Engine is acceptable here as well.
    By skipping the Engine creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(target_metadata, service_name, db_name):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection with the context.
    """
    db_setup = DBSetup(service_name=service_name, db_name=db_name, sql_service_hostname="mysql.strato.service")
    engine = db_setup.create_engine()
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

from srv1.db.models import *

service_name = "srv1"
db_name = "srv1"
logging.info("Running alembic for service %s, database %s", service_name, db_name)
try:

    # Model's MetaData object, for 'autogenerate' support
    # the object has 'tables' property, which automatically populated when the sqlalchemy
    # models inheriting from sqlalchemy model base are imported
    TARGET_METADATA = ModelBase.metadata

    # Alembic Config object, which provides access to the values within the .ini file in use.
    CONFIG = context.config

    # Interpret the config file for Python logging. This line sets up loggers basically.
    fileConfig(CONFIG.config_file_name)
except Exception as e:
    logging.exception("Alembic failed: %s", e.message)


if context.is_offline_mode():
    run_migrations_offline(CONFIG, TARGET_METADATA)
else:
    run_migrations_online(TARGET_METADATA, service_name, db_name)
