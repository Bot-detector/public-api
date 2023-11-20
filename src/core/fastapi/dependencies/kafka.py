import asyncio
import json
import logging
from asyncio import Queue
from time import time

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from src.core.config import settings

logger = logging.getLogger(__name__)


async def kafka_producer(producer: AIOKafkaProducer):
    await producer.start()
    return producer


async def kafka_player_consumer(topic: str, group: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=[settings.KAFKA_HOST],
        group_id=group,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset="earliest",
    )
    await consumer.start()
    return consumer


async def receive_messages(consumer: AIOKafkaConsumer, receive_queue: Queue):
    logger.info("start receiving messages")
    async for message in consumer:
        value = message.value
        await receive_queue.put(value)


async def send_messages(topic: str, producer: AIOKafkaProducer, send_queue: Queue):
    logger.info("start sending messages")
    last_interval = time()
    messages_sent = 0

    while True:
        if send_queue.empty():
            await asyncio.sleep(1)
        message = await send_queue.get()
        await producer.send(topic, value=message)
        send_queue.task_done()

        messages_sent += 1

        if messages_sent >= 100:
            current_time = time()
            elapsed_time = current_time - last_interval
            speed = messages_sent / elapsed_time
            logger.info(
                f"processed {messages_sent} in {elapsed_time:.2f} seconds, {speed:.2f} msg/sec"
            )

            last_interval = time()
            messages_sent = 0


report_send_queue = Queue(maxsize=500)
producer = AIOKafkaProducer(
    bootstrap_servers=[settings.KAFKA_HOST],
    value_serializer=lambda v: json.dumps(v).encode(),
)
