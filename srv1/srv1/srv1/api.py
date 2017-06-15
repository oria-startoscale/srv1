import gevent.monkey
gevent.monkey.patch_all()

import hammock
from strato_common.log import configurelogging
import strato_common.credentials as credentials

from srv1 import resources
from srv1.db.setup import setup_and_get_engine

configurelogging.configureLogging("srv1")


from srv1.utils import events


def setup_service():
    db_engine = setup_and_get_engine()
    events.register_events()
    return hammock.Hammock(hammock.FALCON, resources,
                           credentials_class=credentials.StratoCredentials,
                           policy_file='/usr/share/srv1/etc/policy.json',
                           db_engine=db_engine).api


api = setup_service()
