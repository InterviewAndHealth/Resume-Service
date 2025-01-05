import asyncio
import logging

from app import ENV, SERVICE_QUEUE
from app.services.broker import EventService, RPCService
from app.services.events import EventsService

logging.basicConfig(level=logging.INFO, format="%(levelname)s:\t  %(message)s")


async def main():
    logging.info(f"Serving in {ENV} environment")

    tasks = [
        asyncio.create_task(EventService.subscribe(SERVICE_QUEUE, EventsService)),
        asyncio.create_task(RPCService.respond(EventsService)),
    ]

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        logging.info("Tasks cancelled. Proceeding to shutdown...")
    except Exception as e:
        logging.error(f"Unexpected error during execution: {e}")
    finally:
        # Cancel remaining tasks
        for task in tasks:
            if not task.done():
                task.cancel()
                await task  # Ensure proper cancellation

        logging.info("Shutdown complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Application interrupted by user.")
