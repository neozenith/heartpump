# Standard Library
import logging
from collections import namedtuple
from dataclasses import KW_ONLY, dataclass

# Third Party
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

logger = logging.getLogger(__name__)

TICKRX_DEVICE_UUID = "7EABC224-2836-5894-4F9A-1B583050849E"
TICKRX_DEVICE_NAME = "TICKR X 6CDA"

# 0000180f-0000-1000-8000-00805f9b34fb (Handle: 12): Battery Service
# 0000180a-0000-1000-8000-00805f9b34fb (Handle: 16): Device Information
# a026ee01-0a7d-4ab3-97fa-f1500f9feb8b (Handle: 23): Unknown
# a026ee03-0a7d-4ab3-97fa-f1500f9feb8b (Handle: 30): Unknown
# 0000180d-0000-1000-8000-00805f9b34fb (Handle: 34): Heart Rate
# 00001814-0000-1000-8000-00805f9b34fb (Handle: 46): Running Speed and Cadence
# 00001816-0000-1000-8000-00805f9b34fb (Handle: 52): Cycling Speed and Cadence
# a026ee04-0a7d-4ab3-97fa-f1500f9feb8b (Handle: 58): Unknown

TICKRX_SERVICE_UUIDS = [
    '0000180d-0000-1000-8000-00805f9b34fb', # (Handle: 34): Heart Rate
    '00001814-0000-1000-8000-00805f9b34fb', # (Handle: 46): Running Speed and Cadence
    '00001816-0000-1000-8000-00805f9b34fb', # (Handle: 52): Cycling Speed and Cadence
    'a026ee04-0a7d-4ab3-97fa-f1500f9feb8b'  # (Handle: 58): Unknown
]


TICKX_HEARTRATE_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
TICKRX_HEART_RATE_SERVICE_CHARACTERISTIC = "00002a37-0000-1000-8000-00805f9b34fb" # 00002a37-0000-1000-8000-00805f9b34fb (Handle: 35): Heart Rate Measurement (notify)

async def notification_handler(characteristic, data):
    logger.info(f"{characteristic.description}: {data}")
    logger.info(f"{characteristic.description}: {interpret_hrm_characteristic(data)}")


def interpret_hrm_characteristic(data):
    """
    data is a list of integers corresponding to readings from the BLE HR monitor
    """

    byte0 = data[0]
    res = {}
    res["hrv_uint8"] = (byte0 & 1) == 0
    sensor_contact = (byte0 >> 1) & 3
    if sensor_contact == 2:
        res["sensor_contact"] = "No contact detected"
    elif sensor_contact == 3:
        res["sensor_contact"] = "Contact detected"
    else:
        res["sensor_contact"] = "Sensor contact not supported"
    res["ee_status"] = ((byte0 >> 3) & 1) == 1
    res["rr_interval"] = ((byte0 >> 4) & 1) == 1

    if res["hrv_uint8"]:
        res["hr"] = data[1]
        i = 2
    else:
        res["hr"] = (data[2] << 8) | data[1]
        i = 3

    if res["ee_status"]:
        res["ee"] = (data[i + 1] << 8) | data[i]
        i += 2

    if res["rr_interval"]:
        res["rr"] = []
        while i < len(data):
            # Note: Need to divide the value by 1024 to get in seconds
            res["rr"].append((data[i + 1] << 8) | data[i])
            i += 2

    return res

