# pylint: disable=import-error
import uuid

import strato_consts.apiconfig as api_config
from docker_test_tools.base_test import BaseDockerTest
from docker_test_tools.utils import get_curl_health_check

from tests.subsystem.tools import rabbit_health_check

# Module will be introduced PYTHONPATH change
from srv1_client.client import Client


class SubsystemBaseTest(BaseDockerTest):
    """Basic subsystem test."""
    TOKEN = str(uuid.uuid4())
    USER_ID = str(uuid.uuid4())
    PROJECT_ID = str(uuid.uuid4())
    ROLES = api_config.OPENSTACK_ADMIN_ROLE_NAME

    HEADERS = {
        api_config.StratoHttpHeaders.TOKEN: TOKEN,
        api_config.StratoHttpHeaders.USER_ID: USER_ID,
        api_config.StratoHttpHeaders.USER_ROLES: ROLES,
        api_config.StratoHttpHeaders.PROJECT_ID: PROJECT_ID,
    }

    CLIENT_RETRIES = 2
    CLIENT_TIMEOUT = 600

    SERVICE_HEALTH_END_POINT = \
        'http://srv1-api.service.strato:1234/' \
        'api/v2/srv1/health'

    REQUIRED_HEALTH_CHECKS = [
        get_curl_health_check(service_name='mysql', url='http://mysql.service.strato:3306'),
        get_curl_health_check(service_name='consul', url='http://consul.service.strato:8500'),
        get_curl_health_check(service_name='redis', url='http://master.redis.service.strato:6379'),
        get_curl_health_check(service_name='srv1-api', url=SERVICE_HEALTH_END_POINT),
        rabbit_health_check,
    ]

    def setUp(self):
        """Wait for all services to respond and create a client for the service."""
        BaseDockerTest.setUp(self)

        self.srv1 = \
            Client(headers=self.HEADERS,
                   retries=self.CLIENT_RETRIES,
                   timeout=self.CLIENT_TIMEOUT).api.v2.srv1
