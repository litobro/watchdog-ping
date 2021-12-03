import os
import sys
import asyncio
import kasa
import logging
from logging.handlers import RotatingFileHandler

device_ip = '192.168.0.192'
kasa_ip = '192.168.0.206'
logfile = '/opt/watchdog-ping/output.log'
ping_timeout = 5
attempts = 4

def main(argv):
    logger = logging.getLogger('WATCHDOG-PING-LOG')
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler(logfile, maxBytes=5*1024*1024, backupCount=2)
    handler.setFormatter(log_format)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info('Watchdog on: {}'.format(argv[1]))
    logger.info('Using switch: {}'.format(argv[2]))

    failed_attempts = 0
    for i in range(attempts):
        result = os.system('/bin/ping -c 1 -w {0} {1} > /dev/null 2>&1'.format(ping_timeout, argv[1]))
        logger.debug('result: ' + str(result))
        if result != 0:
            failed_attempts += 1

    if failed_attempts == attempts or True:
        # Device appears to be offline, restart it using smart switch
        logger.info('Device offline, restarting')
        dev = kasa.SmartPlug(argv[2])
        asyncio.run(dev.update())
        asyncio.run(dev.turn_off())
        asyncio.run(dev.turn_on())
        asyncio.run(dev.update())
        try:
            assert dev.is_on
        except Exception as e:
            logger.warning('Device did not come back online!')
    else:
        logger.info('Device OK!')


if __name__ == '__main__':
    main([sys.argv[0], device_ip, kasa_ip])
