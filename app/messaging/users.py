import json
import logging
from datetime import datetime, UTC
from aio_pika import Message
from app.messaging.rabbitmq import get_connection


logger = logging.getLogger(__name__)

"""  PUBLISHERS  """
async def publish_user_created(user_name: str, email: str, role: str, user_id: int):
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("user.created", durable=True)

    payload = json.dumps({
        "event": "user.created",
        "version": "v1",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {
            "user_id": user_id,
            "user": user_name,
            "email": email,
            "role": role
        }
    }).encode()

    await channel.default_exchange.publish(
        Message(payload),
        routing_key=queue.name
    )

    await connection.close()

async def publish_user_updated(user_id: int, updated_fields: dict):
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("user.updated", durable=True)

    payload = json.dumps({
        "event": "user.updated",
        "version": "v1",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {
            "user_id": user_id,
            "updated_fields": updated_fields
        }
    }).encode()

    await channel.default_exchange.publish(
        Message(payload),
        routing_key=queue.name
    )

    await connection.close()

async def publish_user_deleted(user_name: str, email: str, role: str, user_id: int):
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("user.deleted", durable=True)

    payload = json.dumps({
        "event": "user.deleted",
        "version": "v1",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {
            "user_id": user_id,
            "user": user_name,
            "email": email,
            "role": role
        }
    }).encode()

    await channel.default_exchange.publish(
        Message(payload),
        routing_key=queue.name
    )

    await connection.close()


"""  CONSUMERS  """
async def consume_user_created():
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("user.created", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:

            async with message.process():

                data = json.loads(message.body)['data']

                logger.info(
                    "[EVENT] user.created\nName: %s\nEmail: %s\nRole: %s\nID: %s",
                    data["user"],
                    data["email"],
                    data["role"],
                    data["user_id"]
                )

async def consume_user_updated():
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("user.updated", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:

            async with message.process():

                data = json.loads(message.body)['data']
                updated_fields = data["updated_fields"]
                if "password" in updated_fields:
                    updated_fields["password"] = "***hidden***"

                changes = "\n".join(
                    [f"{" " * 6}{field:<9}: {value}" for field, value in updated_fields.items()]
                )

                logger.info(
                    "[EVENT] user.updated\nID: %s\nChanges: \n%s",
                    data["user_id"],
                    f"{changes}"
                )

async def consume_user_deleted():
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("user.deleted", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:

            async with message.process():

                data = json.loads(message.body)['data']

                logger.info(
                    "[EVENT] user.deleted\nName: %s\nEmail: %s\nRole: %s\nID: %s",
                    data["user"],
                    data["email"],
                    data["role"],
                    data["user_id"]
                )