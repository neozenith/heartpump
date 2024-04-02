import logging
import asyncio
import datetime
import contextlib

from heartpump.rpi4 import MotorDriver
from heartpump.ble import connection
from heartpump.tickrx import (
    TICKX_HEARTRATE_SERVICE_UUID, 
    TICKRX_DEVICE_NAME, 
    TICKRX_HEART_RATE_SERVICE_CHARACTERISTIC,
    
    interpret_hrm_characteristic
)

logger = logging.getLogger(__name__)

hr = 72

async def notification_handler(characteristic, data):
    logger.info(f"{characteristic.description}: {data}")
    d = interpret_hrm_characteristic(data)
    logger.info(f"{characteristic.description}: {d}")

async def main():

    async with MotorDriver() as m:
        try:

            await connection(
                TICKRX_DEVICE_NAME, 
                TICKX_HEARTRATE_SERVICE_UUID, 
                TICKRX_HEART_RATE_SERVICE_CHARACTERISTIC,
                notification_handler
            )

            
            logger.info(f"{hr=}")
            t = datetime.datetime.now().timestamp()
            while datetime.datetime.now().timestamp() - t < 60:
                m.set_heart_rate(hr)
                await asyncio.sleep(0.001)


        except KeyboardInterrupt:
            ...

if __name__ == "__main__":
    log_level = logging.INFO
    logging.basicConfig(level=log_level)
    logger.info("Starting")
    with contextlib.suppress(asyncio.CancelledError):
        asyncio.run(main())
