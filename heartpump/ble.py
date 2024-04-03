import asyncio
import logging

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


logger = logging.getLogger(__name__)

async def discover(target_name, timeout=15):
    """Discover by device name"""
    logger.info("Discovering...")

    # Spend some time scanning for advertised devices.
    devices = await BleakScanner.discover(
        timeout=timeout,
        return_adv=True, 
        # cb=dict(use_bdaddr=True) # Use only on macos
    )

    # Filter for the type we need and return it or None.
    for k, v in devices.items():
        device, adv_data = v
        if discover_filter(target_name, device, adv_data):
            logger.info(f"Found: {k}, {v}")
            return device, adv_data

    return None, None

def discover_filter(target: str, device: BLEDevice, adv_data: AdvertisementData):
    """Filter discovered BLE Device based on name or local_name in Advertised Data."""
    if (
        (device.name and target.lower() == device.name.lower()) or 
        (adv_data.local_name and target.lower() == adv_data.local_name.lower())
        ):
        return True
    else:
        return False



async def listen_notifications(device: BLEDevice, service: str, char_uuid: str, char_notify_handler, timeout=20):
    """Listen for HRM data events."""
    logger.info("Start listening...")
    async with BleakClient(device, timeout=30) as client:
        logger.info(client.address)
        logger.info(service)

        try:
            await client.start_notify(char_uuid, char_notify_handler)
            await asyncio.sleep(timeout)
        except KeyboardInterrupt as ki:
            logger.info("Stopping...")
        except Exception as e:
            logger.error(e)
        finally:
            await client.stop_notify(char_uuid)
    
    # Device will disconnect when block exits.    

