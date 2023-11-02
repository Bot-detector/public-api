from asyncio import Queue

from src.core.config import settings

from .engine import AioKafkaEngine

report_queue = Queue()
report_engine = AioKafkaEngine(
    bootstrap_servers=[settings.KAFKA_HOST], topic="reports", message_queue=report_queue
)
