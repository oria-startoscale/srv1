import logging
import requests

from tests.subsystem.base import SubsystemBaseTest


class TestHealth(SubsystemBaseTest):
    """health endpoints tests."""

    DEPENDENCIES = [
        'mysql.service.strato',
        'consul.service.strato',
        'master.redis.service.strato',
        'rabbitmq-server.service.strato',
    ]

    def test_happy_flow(self):
        """Validate health api - happy flow."""
        logging.info('Validating health api response - service should be ready')
        health_response = self.srv1.health.get()
        self.assertEquals(health_response, {'status': 'healthy'})

        logging.info('Validating verbose health api response - peripherals services should be connected')
        health_verbose_response = self.srv1.health.get(extended=True)
        self.assertEquals(health_verbose_response, {service: 'connected' for service in self.DEPENDENCIES})

    def test_peripherals_services_down(self):
        """Validate health api - peripherals services down scenarios."""
        for paused_service in self.DEPENDENCIES:
            logging.info('Validating extended health response when %s is down', paused_service)
            with self.controller.container_paused(name=paused_service):
                health_verbose_response = self.srv1.health.get(extended=True)
                expected_result = {service: 'disconnected' if service == paused_service else 'connected'
                                   for service in self.DEPENDENCIES}
                self.assertEquals(health_verbose_response, expected_result)

    def test_service_down(self):
        """Validate health api - main service down scenario."""
        service_name = "srv1-api.service.strato"
        logging.info('Validating health response when %s is down', service_name)
        with self.controller.container_down(name=service_name):
            logging.info('Validating health api response - should fail')
            with self.assertRaises(requests.exceptions.ConnectionError):
                self.srv1.health.get()
