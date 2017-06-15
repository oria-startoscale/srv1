from celery import Celery
import pkgutil
import os.path
import srv1.managers

import gevent.monkey  # NOQA
gevent.monkey.patch_all()


RABBITMQ_ADDRESS = "rabbitmq-server.service.strato"
REDIS_ADDRESS = "master.redis.service.strato"
TASK_TIME_LIMIT = 5 * 60


def _get_modules():
    pkgpath = os.path.dirname(srv1.managers.__file__)
    files = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
    modules = ["srv1.managers.{}".format(file_name) for file_name in files]
    return modules


app = Celery('srv1')
app.conf.update(
    broker_url='pyamqp://guest@{server}//'.format(server=RABBITMQ_ADDRESS),
    result_backend='redis://{server}/'.format(server=REDIS_ADDRESS),
    task_default_queue="srv1",
    imports=_get_modules(),
    task_track_started=True,
    task_soft_time_limit=TASK_TIME_LIMIT
)
