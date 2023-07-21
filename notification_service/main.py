import asyncio
import json

from aio_pika import IncomingMessage
import aio_pika
import enum


class MessageMethod(enum.Enum):
    SCHEDULE = "schedule"
    CANCEL = "cancel"
    RESCHEDULE = "reschedule"


async def callback(
        message: IncomingMessage
):
    txt = message.body.decode("utf-8")
    print(json.loads(txt))
    return True


async def schedule_message(
        message
):
    print(message)


async def reschedule_message(
        message
):
    print(message)


async def cancel_message(
        message
):
    print(message)


async def main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://rmuser:rmpassword@127.0.0.1/",
    )

    channel = await connection.channel()

    schedule_queue = await channel.declare_queue(MessageMethod.SCHEDULE.value)
    reschedule_queue = await channel.declare_queue(MessageMethod.RESCHEDULE.value)
    cancel_queue = await channel.declare_queue(MessageMethod.CANCEL.value)

    await schedule_queue.consume(schedule_message, no_ack=True)
    await reschedule_queue.consume(reschedule_message, no_ack=True)
    await cancel_queue.consume(cancel_message, no_ack=True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    loop.run_forever()
