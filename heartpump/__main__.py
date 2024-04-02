import logging
import asyncio
from heartpump.rpi4 import MotorDriver
from time import sleep
import datetime
logger = logging.getLogger(__name__)


async def main():

    async with MotorDriver() as m:
        try:
            for hr in range(60,240, 30):
                logger.info(f"{hr=}")
                t = datetime.datetime.now().timestamp()
                while datetime.datetime.now().timestamp() - t < 5:
                    m.set_heart_rate(hr)
                    await asyncio.sleep(0.001)


        except KeyboardInterrupt:
            ...

if __name__ == "__main__":
    log_level = logging.INFO
    logging.basicConfig(level=log_level)
    logger.info("Starting")
    asyncio.run(main())
