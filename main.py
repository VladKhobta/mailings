import asyncio
import aio_pika


async def main() -> None:
    connection = await aio_pika.connect_robust(
        "ampq://rmuser:rmpassword@127.0.0.1/",
    )

    queue
