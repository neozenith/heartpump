import logging
from heartpump.rpi4 import MotorDriver
from time import sleep
import datetime
logger = logging.getLogger(__name__)


def main():
    ...

if __name__ == "__main__":
    log_level = logging.INFO
    logging.basicConfig(level=log_level)
    logger.info("Starting")

    with MotorDriver() as m:
        try:
            for hr in range(60,240, 30):
                logger.info(f"{hr=}")
                t = datetime.datetime.now().timestamp()
                while datetime.datetime.now().timestamp() - t < 5:
                    m.set_heart_rate(hr)
                    sleep(0.001)


        except KeyboardInterrupt:
            ...
