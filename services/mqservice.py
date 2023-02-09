import json
import logging

import pika

from system.libs.baseservice import BaseService


class MqService(BaseService):
    auto_load = False
    conn = None
    channel = None

    def init(self, cfg = None):
        self.conn = pika.BlockingConnection(pika.connection.URLParameters(self.ctx.cfg.rabbitmq.url))
        self.channel = self.conn.channel()
        logging.debug('msq service init')

    def listen_on_queue(self, queue_name, callback):
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
        self.channel.start_consuming()

    def send(self, queue_name, msg):
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(msg))
