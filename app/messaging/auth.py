import json
import logging
from datetime import datetime, UTC
from aio_pika import Message
from app.messaging.rabbitmq import get_connection


logger = logging.getLogger(__name__)

"""  PUBLISHERS  """
async def publish_user_login(user_id: int, email: str):
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("user.logged_in", durable=True)

    payload = json.dumps({
        "event": "user.logged_in",
        "version": "v1",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {
            "user_id": user_id,
            "email": email
        }
    }).encode()

    await channel.default_exchange.publish(
        Message(payload),
        routing_key=queue.name
    )

    await connection.close()


"""  CONSUMERS  """
async def consume_user_login():
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("user.logged_in", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:

            async with message.process():

                data = json.loads(message.body)['data']

                logger.info(
                    "[EVENT] user.logged_in\nEmail: %s\nID: %s",
                    data["email"],
                    data["user_id"]
                )