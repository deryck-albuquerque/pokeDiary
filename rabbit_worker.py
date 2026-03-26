import asyncio
import logging
from app.messaging.users import consume_user_created, consume_user_updated, consume_user_deleted
from app.messaging.auth import consume_user_login
from app.messaging.diary import consume_diary_created, consume_diary_updated, consume_diary_deleted

logging.basicConfig(
    level=logging.INFO,
    format="\n%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

async def main():
    await asyncio.gather(
        consume_user_created(),
        consume_user_updated(),
        consume_user_deleted(),
        consume_user_login(),
        consume_diary_created(),
        consume_diary_updated(),
        consume_diary_deleted()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nWorker Stopped")