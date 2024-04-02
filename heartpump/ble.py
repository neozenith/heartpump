import asyncio
import logging

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


logger = logging.getLogger(__name__)

async def discover(target_name, timeout=15):
    logger.info("Discovering...")
    devices = await BleakScanner.discover(
        timeout=timeout,
        return_adv=True, 
        cb=dict(use_bdaddr=True)
    )

    for k, v in devices.items():
        device, adv_data = v
        if discover_filter(target_name, device, adv_data):
            logger.info(f"Found: {k}, {v}")
            return device, adv_data

    return None, None

def discover_filter(target: str, device: BLEDevice, adv_data: AdvertisementData):
    if (
        (device.name and target.lower() == device.name.lower()) or 
        (adv_data.local_name and target.lower() == adv_data.local_name.lower())
        ):
        return True
    else:
        return False



async def connection(target_name: str, service: str, char_uuid: str, char_notify_handler):
    device, adv_data = await discover(target_name, timeout=10)
    if device is None:
        logger.error("Device not found")
        return
    
    async with BleakClient(device, services=[service]) as client:
        logger.info(client.address)
        logger.info(service)


        try:
            await client.start_notify(char_uuid, char_notify_handler)
            await asyncio.sleep(20.0)
        except KeyboardInterrupt as ki:
            logger.info("Stopping...")
        except Exception as e:
            logger.error(e)
        finally:
            await client.stop_notify(char_uuid)
        


    # # Device will disconnect when block exits.
    # ...

