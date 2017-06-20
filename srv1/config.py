import os
import sys

BASE_CONFIG = os.path.join(sys.prefix, 'share/srv1')
ALEMBIC_DIR = os.path.join(BASE_CONFIG, 'alembic')
SYSTEMD_DIR = '/usr/lib/systemd/system'
DB_CONNECTION_STRING_REGISTRY = 'srv1/sql_connection_string'
DB_NAME = 'srv1'
DB_PASSWORD_LENGTH = 16
DB_SERVICE_ADDRESS = 'mysql.service.strato'
