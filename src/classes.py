import logging
import time

# from pika import BasicProperties, BlockingConnection, ConnectionParameters
from redis import Redis

from interfaces import IBroker


class RedisBroker(IBroker):
    def __init__(
        self,
        host: str,
        port: int,
        queue: str,
    ):
        self.host = host
        self.port = port
        self.queue = queue

    def open(self):
        while True:
            try:
                self.conn = Redis(host=self.host, port=self.port)
                break
            except:
                logging.error("Can't connect to broker")
                time.sleep(1)

    def close(self):
        self.conn.close()

    def send(self, body: str):
        self.conn.rpush(self.queue, body)

    def receive(self) -> str | None:
        return self.conn.lpop(self.queue)


class RabbitMQBroker(IBroker):
    def __init__(
        self,
        host: str,
        port: int,
        queue: str,
    ):
        self.host = host
        self.port = port
        self.queue = queue

    def open(self):
        while True:
            try:
                self.conn = BlockingConnection(
                    parameters=ConnectionParameters(host=self.host, port=self.port)
                )
                break
            except:
                logging.error("Can't connect to broker")
                time.sleep(1)
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue=self.queue)

    def close(self):
        self.channel.close()
        self.conn.close()

    def send(self, body: str):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=body,
            properties=BasicProperties(content_type="text/plain", delivery_mode=2),
        )

    def receive(self) -> str | None:
        method_frame, _, body = self.channel.basic_get(queue=self.queue, auto_ack=True)
        if method_frame:
            return body.decode()
