import kombu
import logging


def rabbit_health_check():
    """Returns True if the rabbit is responsive, False otherwise."""
    conn = kombu.Connection('pyamqp://guest@rabbitmq-server.service.strato', connect_timeout=1)
    try:
        conn.connect()
        logging.debug('Service rabbitmq ready: True')
        return True
    except:
        logging.debug('Service rabbitmq ready: False')
        return False
    finally:
        conn.release()
