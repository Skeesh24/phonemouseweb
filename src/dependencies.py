import logging

from classes import RabbitMQBroker

BROKER_HOST = "broker"
BROKER_PORT = 5672
BROKER_QUEUE = "queue1"


async def get_broker():
    broker = RabbitMQBroker(BROKER_HOST, BROKER_PORT, BROKER_QUEUE)
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
