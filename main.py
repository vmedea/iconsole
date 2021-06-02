#!/usr/bin/env python3
# based on https://github.com/haraldh/iconsole from Harald Hoyer
# SPDX-License-Identifier: MIT

import sys
from time import sleep, time, monotonic
from binascii import hexlify,unhexlify
import logging

import logsetup
import iconsole
from packets import *
import bleconn

DEBUG = False
logger = logging.getLogger("main")

if  __name__ =='__main__':
    if len(sys.argv) < 3:
        print('Usage: {} <macaddr> <sessionlog>'.format(sys.argv[0]))
        print()
        print('You can get the macaddr of the iconsole device using')
        print('    hcitool -i hci0 lescan')
        sys.exit(1)

    logsetup.init_logging()
    bleconn.DEBUG = DEBUG
    if not DEBUG:
        logging.getLogger('pygatt').setLevel(logging.ERROR)

    f = open(sys.argv[2], 'xb')

    sock = bleconn.MicrochipBLEConn(sys.argv[1])

    iconsole.init(sock)

    got = iconsole.send_level(sock, 32)
    logger.debug("SET_LEVEL done %s" % (hexlify(got).decode()))

    interval = 1.0 # interval between readouts
    ts_next = monotonic() + interval
    while True:
        got = iconsole.send_recv(sock, READ, plen=21)
        ic = ReadResponse(got)
        logger.info("%s", str(ic))
        f.write(b"%f %s\n" % (time(), hexlify(got)))
        f.flush()

        ts = monotonic()
        if ts < ts_next:
            sleep(ts_next - ts)
        ts_next += interval

    iconsole.send_recv(STOP)
    iconsole.send_recv(PING)
    sock.close()
