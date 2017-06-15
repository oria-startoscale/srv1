import hammock

from srv1.managers import health as health_manager
from strato_common.service_utils.db.resource_base import ResourceBase


class Health(ResourceBase):
    """Health resource APIs."""

    DEFAULT_CHECK_TIMEOUT = 1

    @hammock.get()
    def get(self, _credentials, extended=False, check_timeout=DEFAULT_CHECK_TIMEOUT):
        """Returns the health status.

        Note:
            This endpoint will be used continuously by cluster manager in order to
            determine if the service is up and running and ready to serve requests.

        :param bool[False] extended: If set an extended health check will initiate
        :param int check_timeout: Timeout in seconds for each of the connection tests
        :return dict: Health status
        """
        return health_manager.HealthManager(db_engine=self.db_engine, credentials=_credentials).get(extended,
                                                                                                    check_timeout)
