from AioKafkaEngine import ProducerEngine

from src.core.config import settings

producer = ProducerEngine(
    bootstrap_servers=[settings.KAFKA_HOST],
    report_interval=60,
    queue_size=500,
)
