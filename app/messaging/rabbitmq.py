import aio_pika
import os

RABBIT_URL = f"amqp://{os.getenv("RABBITMQ_USER")}:{os.getenv("RABBITMQ_PASSWORD")}@{os.getenv('RABBITMQ_HOST')}:5672/"

async def get_connection():
    """
    Connect w RabbitMQ
    :return: connection
    """
    connection = await aio_pika.connect_robust(RABBIT_URL)
    return connection