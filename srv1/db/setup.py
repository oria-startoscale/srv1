import logging
import subprocess

from strato_kv.clustermanagement import clustermanagementapi
from strato_kv.consulutils.lockclient import LockClient
from strato_kv.consulutils import resourcelock

from strato_common.service_utils.db.mysql.setup import Setup as DBSetup
from srv1 import config


SERVICE_NAME = "srv1"


def setup_and_get_engine():
    """
    Generate the DB schema and migration scripts using alembic.

    * Create version dir if it doesnt exists.
    * Remove old migration scripts to start the process fresh.
    * Generate migration revision file.
    * Run a script to fix the generated migration file.
    * Upgrade alembic head:
        - update the DB tables according to the generated migration scripts.
        - update a record in the alembic generated DB table stating the current revision.
    """
    dbsetup = DBSetup(service_name=SERVICE_NAME,
                      db_name=config.DB_NAME,
                      sql_service_hostname=config.DB_SERVICE_ADDRESS,
                      password_length=config.DB_PASSWORD_LENGTH)

    cmapi = clustermanagementapi.ClusterManagementAPI()
    lock_client = LockClient(cmapi)
    with resourcelock.ResourceLock(lock_client, SERVICE_NAME + "db_lock", 'setup_db',
                                   resourcelock.ResourceLockedException, wait=True):
        dbsetup.setup()
        db_engine = dbsetup.create_engine()
        logging.info("Generating the DB schema and migration scripts using alembic. "
                     "Database name: %s", config.DB_NAME)
        db_engine.execute("drop table if exists alembic_version")

        for command in ["mkdir -p versions",
                        "rm -rf versions/*",
                        "alembic revision --autogenerate",
                        "alembic upgrade head"]:
            subprocess.check_output(command, shell=True, cwd=config.ALEMBIC_DIR)

    return db_engine


def get_engine():
    dbsetup = DBSetup(service_name=SERVICE_NAME,
                      db_name=config.DB_NAME,
                      sql_service_hostname=config.DB_SERVICE_ADDRESS,
                      password_length=config.DB_PASSWORD_LENGTH)
    return dbsetup.create_engine()
