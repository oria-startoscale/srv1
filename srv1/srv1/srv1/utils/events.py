import os
import logging

from datalayer_lib import severity
from events_agent_client.client import EventsAgentClient

from srv1.consts import event_types


EVENTS_SERVICE_PORT = 7086


class EntityType(object):
    my_endpoint = "my_endpoint"


def get_events_service_address():
    return os.environ.get("EVENTS_SERVICE_ADDRESS", "127.0.0.1")


def register_events():
    logging.info("Registering events")
    events_client = EventsAgentClient(hostname=get_events_service_address(), port=EVENTS_SERVICE_PORT).api.v2.events

    events_client.register(
        type_id=event_types.my_endpoint_CREATE_SUCCESS,
        entity_type=EntityType.my_endpoint,
        severity=severity.INFO,
        name="my_endpoint created successfully",
        description_template="my_endpoint created successfully"
    )

    events_client.register(
        type_id=event_types.my_endpoint_CREATE_FAIL,
        entity_type=EntityType.my_endpoint,
        severity=severity.ERROR,
        name="my_endpoint creation failed",
        description_template="my_endpoint creation failed"
    )

    events_client.register(
        type_id=event_types.my_endpoint_DELETE_SUCCESS,
        entity_type=EntityType.my_endpoint,
        severity=severity.INFO,
        name="my_endpoint deleted successfully",
        description_template="my_endpoint deleted successfully"
    )
