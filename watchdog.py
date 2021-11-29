import os
import sys
import datetime

ping_timeout = 5
attempts = 4

def main(argv):
    print('Watchdog on:', argv[1])

    for i in range(attempts):
        result = os.system('/bin/ping -c 1 -w {0} {1} > /dev/null 2>&1'.format(ping_timeout, argv[1]))
        if result != 0:
            failed_attempts += 1

    if failed_attempts == attempts:
        pass


if __name__ == '__main__':
    main(sys.argv)
