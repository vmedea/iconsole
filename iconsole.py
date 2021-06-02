#!/usr/bin/env python3
# based on https://github.com/haraldh/iconsole from Harald Hoyer
# SPDX-License-Identifier: MIT
from binascii import hexlify
import logging

from packets import *

logger = logging.getLogger("iconsole")

def send_recv(sock, packet, expect=None, plen=0):
    packet = bytes(packet) + bytes([sum(packet) & 0xff]) # add checksum
    if expect == None:
        # if no expected response byte, expect it to be 0xbX where the request is 0xaX
        expect = 0xb0 | (packet[1] & 0xF)

    if plen == 0:
        # if no expected length, expect response to be the same length as request
        # (with checksum added)
        plen = len(packet)

    while True:
        sock.sendall(packet)
        got = b''
        while len(got) < plen:
            ret = sock.recv(plen - len(got), 1.0)
            if not ret:
                break
            got += ret

        if len(got) == plen and got[0] == packet[0] and got[1] == expect:
            # check and remove checksum
            if (sum(got[0:-1]) & 0xff) == got[-1]:
                return got[0:-1]
            logger.error("Checksum error")
        elif len(got) < plen:
            logger.error("Timed out")
        else:
            logger.error("Unexpected response %s" % hexlify(got))

        logger.info("Retransmit")

def send_level(sock, lvl):
    packet = bytearray(SET_LEVEL)
    packet[-1] = lvl + 1
    got = send_recv(sock, packet)
    return got

def init(sock):
    got = send_recv(sock, PING)
    logger.debug("ping done %s" % (hexlify(got).decode()))

    got = send_recv(sock, INIT_A0, expect=0xb7, plen=6)
    logger.debug("A0 done %s" % (hexlify(got).decode()))

    got = send_recv(sock, STATUS, plen=6)
    logger.debug("status done %s" % (hexlify(got).decode()))

    got = send_recv(sock, INIT_A3)
    logger.debug("A3 done %s" % (hexlify(got).decode()))

    got = send_recv(sock, INIT_A4)
    logger.debug("A4 done %s" % (hexlify(got).decode()))

    got = send_recv(sock, START)
    logger.debug("START done %s" % (hexlify(got).decode()))
