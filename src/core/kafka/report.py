from asyncio import Queue
from .engine import AioKafkaEngine
from src.core.config import settings

report_queue = Queue()
report_engine = AioKafkaEngine(
    bootstrap_servers=[settings.KAFKA_HOST], topic="reports", message_queue=report_queue
)
