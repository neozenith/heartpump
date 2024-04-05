import logging
import asyncio
import datetime
import contextlib
import time

from bleak.backends.device import BLEDevice

from heartpump.rpi4 import MotorDriver
from heartpump.ble import listen_notifications, discover
from heartpump.tickrx import (
    TICKX_HEARTRATE_SERVICE_UUID, 
    TICKRX_DEVICE_ID, 
    TICKRX_DEVICE_NAME,
    TICKRX_HEART_RATE_SERVICE_CHARACTERISTIC,
    interpret_hrm_characteristic
)

logger = logging.getLogger(__name__)


async def hrm_listener(queue: asyncio.Queue, device: BLEDevice):
        """Find BLE HRM device, listen to notifications and enqueue data."""

        async def notification_handler(characteristic, data):
            """BLE Notification Handler for HRM Notify Read Event."""
            logger.info(f"{characteristic.description}: {data}")
            d = interpret_hrm_characteristic(data)
            logger.info(f"{characteristic.description}: {d}")
            await queue.put((time.time(), d))

        await listen_notifications(
                device, 
                TICKX_HEARTRATE_SERVICE_UUID, 
                TICKRX_HEART_RATE_SERVICE_CHARACTERISTIC,
                notification_handler,
                timeout=120
            )
        
        # Send producer stop message.
        # await queue.put((time.time(), None))



async def motor_controller(queue: asyncio.Queue):
    """Consumer of HRM data to simluate motor like a heart beat."""
    hr = 72
    producer_working = True
    _ts, _hr = await queue.get()
    _delta = datetime.datetime.now().timestamp() - _ts
    logger.info(f"{_ts=} {_delta=}")
    logger.info(f"{_hr=}")
    if _hr is None:
        return
    
    async with MotorDriver() as m:
        try:            
            
            t = datetime.datetime.now().timestamp()

            while producer_working or datetime.datetime.now().timestamp() - t > 30:
                # logger.info(f"{hr=}")
                m.set_heart_rate(hr)
                # await asyncio.sleep(0.001)

                try:
                    _ts, _hr = await asyncio.wait_for(queue.get(), timeout=0.001)
                    _delta = datetime.datetime.now().timestamp() - _ts
                    logger.info(f"{_ts=} {_delta=}")
                    logger.info(f"{_hr=}")
                    if _hr is None:
                        producer_working = False
                except TimeoutError:
                    # logger.warn("Timeout fetching next HR measurement.")
                    ...


        except KeyboardInterrupt:
            ...

async def main():
    queue = asyncio.Queue()

    device, adv_data = await discover(TICKRX_DEVICE_NAME, timeout=10)
    if device is None:
        logger.error("Device not found")
        return
    
    logger.info(f"{device=}")
    hrm_task = hrm_listener(queue, device)
    motor_task = motor_controller(queue)

    await asyncio.gather(hrm_task, motor_task)

if __name__ == "__main__":
    log_level = logging.INFO
    logging.basicConfig(level=log_level)
    logger.info("Starting")
    
    with contextlib.suppress(asyncio.CancelledError):
        asyncio.run(main())
