import os
import sys
import asyncio
import kasa
import logging

device_ip = '192.168.0.192'
ping_timeout = 5
attempts = 4

def main(argv):
    logging.basicConfig(filename='/opt/watchdog-ping/output.log', 
                        format='%(asctime)s %(message)s', 
                        level=logging.INFO)
    logging.info('Watchdog on: {}'.format(argv[1]))

    failed_attempts = 0
    for i in range(attempts):
        result = os.system('/bin/ping -c 1 -w {0} {1} > /dev/null 2>&1'.format(ping_timeout, argv[1]))
        if result != 0:
            failed_attempts += 1

    if failed_attempts == attempts:
        # Device appears to be offline, restart it using smart switch
        logging.info('Device offline, restarting')
        dev = kasa.SmartDevice('192.168.0.206')
        asyncio.run(dev.update())
        asyncio.run(dev.turn_off())
        asyncio.run(dev.turn_on())
        asyncio.run(dev.update())
        try:
            assert dev.is_on
        except Exception as e:
            logging.warning('Device did not come back online!')


if __name__ == '__main__':
    main([sys.argv[0], device_ip])
