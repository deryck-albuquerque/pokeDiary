import json
import logging
from binascii import a2b_qp
from datetime import datetime, UTC
from aio_pika import Message
from app.messaging.rabbitmq import get_connection


logger = logging.getLogger(__name__)

"""  PUBLISHERS  """
async def publish_diary_created(user_id: int, user_name: str):
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("diary.created", durable=True)

    payload = json.dumps({
        "event": "diary.created",
        "version": "v1",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {
            "user_id": user_id,
            "user": user_name,
        }
    }).encode()

    await channel.default_exchange.publish(
        Message(payload),
        routing_key=queue.name
    )

    await connection.close()

async def publish_diary_updated(user_id: int, updated_fields: dict):
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("diary.updated", durable=True)

    payload = json.dumps({
        "event": "diary.updated",
        "version": "v1",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {
            "user_id": user_id,
            "updated_fields": updated_fields,
        }
    }).encode()

    await channel.default_exchange.publish(
        Message(payload),
        routing_key=queue.name
    )

    await connection.close()

async def publish_diary_deleted(user_id: int, diary_id: int):
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("diary.deleted", durable=True)

    payload = json.dumps({
        "event": "diary.deleted",
        "version": "v1",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {
            "user_id": user_id,
            "diary_id": diary_id
        }
    }).encode()

    await channel.default_exchange.publish(
        Message(payload),
        routing_key=queue.name
    )

    await connection.close()


"""  CONSUMERS  """
async def consume_diary_created():
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("diary.created", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:

            async with message.process():

                data = json.loads(message.body)['data']

                logger.info(
                    "[EVENT] diary.created\nName: %s\nID: %s",
                    data["user"],
                    data["user_id"]
                )

async def consume_diary_updated():
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("diary.updated", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:

            async with message.process():

                data = json.loads(message.body)['data']
                updated_fields = data["updated_fields"]

                changes = "\n".join(
                    [f"{" " * 6}{field:<9}: {value}" for field, value in updated_fields.items()]
                )

                logger.info(
                    "[EVENT] diary.updated\nID: %s\nChanges: \n%s",
                    data["user_id"],
                    f"{changes}"
                )

async def consume_diary_deleted():
    connection = await get_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("diary.deleted", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:

            async with message.process():

                data = json.loads(message.body)['data']

                logger.info(
                    "[EVENT] diary.deleted\nUser ID: %s\nDiary ID: %s",
                    data["user_id"],
                    data["diary_id"]
                )