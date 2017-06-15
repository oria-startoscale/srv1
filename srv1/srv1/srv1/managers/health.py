import logging
import urllib2

import kombu
from strato_common.log.logdecorator import log_call
from strato_common.service_utils.db.manager_base import ManagerBase


class HealthManager(ManagerBase):
    """Health manager."""
    SERVICES_PERIPHERALS_URLS = {
        'mysql.service.strato': 'http://mysql.service.strato:3306',
        'consul.service.strato': 'http://consul.service.strato:8500',
        'master.redis.service.strato': 'http://master.redis.service.strato:6379',
    }

    CONNECTED, DISCONNECTED = 'connected', 'disconnected'

    @log_call()
    def get(self, extended, check_timeout):
        """Returns the health status.

        Note:
            This method will be used continuously by cluster manager in order to
            determine if the service is up and running and ready to serve requests.

        :arg bool extended: if set an extended health check will initiate.
        :arg int check_timeout: timeout in seconds for each of the connection tests.
        :return dict: health status.
        """
        if not extended:
            return {'status': 'healthy'}

        return self.get_extended(check_timeout)

    @log_call()
    def get_extended(self, check_timeout):
        """Returns the service extended health status.

        Probe services peripherals and return their connection status:
         - mysql, rabbit, consul and redis connection statues are tested via REST requests.
         - rabbit is tested via kombu client.

        :arg int check_timeout: timeout in seconds for each of the connection tests.
        :return dict: extended health status.
        """
        logging.info('Getting peripherals services connection status')
        peripherals_status = {service_name: self._get_connection_state(service_url, timeout=check_timeout)
                              for service_name, service_url in self.SERVICES_PERIPHERALS_URLS.iteritems()}

        peripherals_status['rabbitmq-server.service.strato'] = self._get_rabbit_connection_state(timeout=check_timeout)

        return peripherals_status

    def _get_connection_state(self, service_url, timeout):
        """Returns 'connected' if the given service_url is responsive, 'disconnected' otherwise."""
        try:
            urllib2.urlopen(service_url, timeout=timeout)
            return self.CONNECTED
        except:
            logging.exception('Failed getting response from %s', service_url)
            return self.DISCONNECTED

    def _get_rabbit_connection_state(self, timeout):
        """Returns 'connected' if the rabbit is responsive, 'disconnected' otherwise."""
        conn = kombu.Connection('pyamqp://guest@rabbitmq-server.service.strato', connect_timeout=timeout)
        try:
            conn.connect()
            return self.CONNECTED
        except:
            logging.exception('Failed getting response from rabbitmq-server.service.strato')
            return self.DISCONNECTED
        finally:
            conn.release()
