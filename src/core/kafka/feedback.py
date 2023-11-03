from asyncio import Queue

from src.core.config import settings

from .engine import AioKafkaEngine

feedback_queue = Queue()
feedback_engine = AioKafkaEngine(
    bootstrap_servers=[settings.KAFKA_HOST],
    topic="feedback",
    message_queue=feedback_queue,
)
