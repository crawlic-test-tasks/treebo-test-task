import asyncio
from datetime import datetime, timedelta
import logging

from arq import create_pool
from arq.connections import RedisSettings

# fix for arq to work
try:
    from src.settings import settings
    from src.config import bot
except ImportError:
    from settings import settings
    from config import bot


_REMIND_BEFORE_MINUTES = 10
_HOURS_DELTA_FOR_MOSCOW = 3

r_settings = RedisSettings(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, database=1
)
logger = logging.getLogger("notifications")


async def get_pool():
    pool = await create_pool(r_settings)
    return pool


async def send_message(
    _,
    text: str,
    chat_id: int,
):
    await bot.send_message(chat_id, text)


async def create_notification(
    text: str,
    chat_id: int,
    notification_dt: datetime,
):
    pool = await get_pool()
    await pool.enqueue_job(
        "send_message",
        text,
        chat_id,
        _defer_until=notification_dt
        - timedelta(minutes=_REMIND_BEFORE_MINUTES)
        - timedelta(hours=_HOURS_DELTA_FOR_MOSCOW),
    )
    logger.info(
        f"created notification for {chat_id=} for {notification_dt=}, current_time={datetime.now()}"
    )


class WorkerSettings:
    functions = [send_message]
    redis_settings = r_settings


if __name__ == "__main__":
    asyncio.run(get_pool())
