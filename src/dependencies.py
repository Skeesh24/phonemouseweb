import logging
from os import getenv

from classes import RedisBroker

BROKER_HOST = getenv("BROKER_HOST")
BROKER_PORT = getenv("BROKER_PORT")
BROKER_QUEUE = getenv("BROKER_QUEUE", "queue1")


async def get_broker():
    broker = RedisBroker(BROKER_HOST, BROKER_PORT, BROKER_QUEUE)
    broker.open()
    try:
        yield broker
    except Exception as e:
        logging.error(e)
        raise e
    finally:
        # if not broker.conn.is_closed:
        #     broker.close()
        pass
