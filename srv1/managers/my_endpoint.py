import logging
import time
import munch

from srv1 import celery_app
from sqlalchemy.orm import exc
import hammock.exceptions as hammock_exceptions
from strato_common.log.logdecorator import log_call
from strato_common.service_utils.db.manager_base import ManagerBase, db_session
from srv1.db import setup as db_setup
from srv1.db import models
from srv1.consts import my_endpoint_status, event_types
from srv1.utils import events as events_util
from events_agent_client.client import EventsAgentClient


class MyEndpointManager(ManagerBase):

    def __init__(self, db_engine, credentials):
        super(MyEndpointManager, self).__init__(db_engine, credentials)
        self._events_client = EventsAgentClient(
            hostname=events_util.get_events_service_address(),
            port=events_util.EVENTS_SERVICE_PORT,
            headers=credentials.headers,
            suppress_errors=True
            ).api.v2.events

    @db_session
    @log_call()
    def create(self, name):
        """Create a new my_endpoint resource.

        :param str name: name of the new my_endpoint.

        :return MyEndpointModel: The requested my_endpoint object.
        """
        record = models.my_endpoint.MyEndpointModel(name=name, status=my_endpoint_status.PENDING)
        self.db_accessor.session.add(record)
        self.db_accessor.commit()

        _provision_my_endpoint_task.delay(record.id, dict(self._credentials.headers))

        return record

    @db_session
    @log_call()
    def provision(self, my_endpoint_id):
        logging.info("Provisioning started for My Endpoint %(id)s",
                     dict(id=my_endpoint_id))

        try:
            record = self.get(my_endpoint_id)
            record.status = my_endpoint_status.STARTED
            self.db_accessor.commit()

            # Do some long provisioning
            time.sleep(5)

            result = "provisioning_result"
            record.status = my_endpoint_status.FINISHED
            record.result = result
            self.db_accessor.commit()
            self._events_client.submit(type_id=event_types.my_endpoint_CREATE_SUCCESS, entity_id=my_endpoint_id)
            return result

        except Exception as ex:  # pylint: disable=broad-except
            logging.exception("Failed to provision My Endpoint %(id)s",
                              dict(id=my_endpoint_id))
            record = self.get(my_endpoint_id)
            record.status = my_endpoint_status.FAILED
            record.result = ex.message
            self.db_accessor.commit()
            self._events_client.submit(type_id=event_types.my_endpoint_CREATE_FAIL, entity_id=my_endpoint_id)
            raise

    @db_session
    @log_call()
    def get(self, my_endpoint_id):
        """Get the details of the requested my_endpoint object.

        :param str my_endpoint_id: Requested my_endpoint object ID.
        :return MyEndpointModel: The requested my_endpoint object.
        """
        # Define the filters
        filters = {"id": my_endpoint_id}

        try:
            return self.db_accessor.session.query(
                models.my_endpoint.MyEndpointModel).filter_by(**filters).one()
        except exc.NoResultFound:
            raise hammock_exceptions.NotFound("Requested 'My Endpoint' object %(id)s doesn't exist"
                                              % dict(id=my_endpoint_id))

    @db_session
    @log_call()
    def list(self):
        """Get a list of the my_endpoints.

        :return list: List of my_endpoint objects details.
        """
        # Define the filters
        filters = {}

        return [record for record in self.db_accessor.session.query(
            models.my_endpoint.MyEndpointModel).filter_by(**filters)]

    @db_session
    @log_call()
    def delete(self, my_endpoint_id):
        """Delete the requested my_endpoint.

        :param str my_endpoint_id: Requested my_endpoint object ID.
        """
        record = self.get(my_endpoint_id)

        logging.info('Removing my_endpoint object %(name)s', dict(name=record.name))
        self.db_accessor.session.delete(record)
        self.db_accessor.commit()
        self._events_client.submit(type_id=event_types.my_endpoint_DELETE_SUCCESS, entity_id=my_endpoint_id)


@celery_app.app.task
def _provision_my_endpoint_task(my_endpoint_id, credentials_headers):
    credentials = munch.Munch(headers=credentials_headers)
    manager = MyEndpointManager(db_engine=db_setup.get_engine(), credentials=credentials)
    manager.provision(my_endpoint_id)
