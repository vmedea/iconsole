import struct, sys, hashlib
from time import sleep, time
from binascii import hexlify,unhexlify
import threading
import pygatt
import logging

DEBUG = False
logger = logging.getLogger("bleconn")

CONNECT_TRIES = 5

class _BLEConn:
    '''
    Very limited UART abstraction for WH-BLE 102, using pygatt.
    '''
    def __init__(self, macaddr, reset_on_start=False):
        self.condition = threading.Condition()
        self.recvbuf = bytearray()

        self.adapter = pygatt.GATTToolBackend()
        logger.debug('Starting adapter')
        self.adapter.start(reset_on_start=reset_on_start)
        logger.debug('Started adapter, connecting')

        timeouts = 0
        while True:
            try:
                self.dev = self.adapter.connect(macaddr, timeout=1)
                break
            except pygatt.exceptions.NotConnectedError:
                if timeouts < CONNECT_TRIES:
                    pass
            timeouts += 1

        logger.debug('Connected to device')
        self.rx_handle = self.dev.get_handle(self.UART_RX)
        logger.debug(f'RX handle: {self.rx_handle}')

        self.dev.subscribe(self.UART_TX, callback=self.handle_data)
        logger.debug('Subscribed to UART TX')


    def sendall(self, v):
        '''
        Send data to UART.
        '''
        if DEBUG:
            logger.debug('UART sending %s' % hexlify(v))
        # TODO what is the max size? divide into parts if needed
        # 20 bytes I think
        self.dev.char_write_handle(self.rx_handle, v, True)

    def handle_data(self, handle, value):
        '''
        Handle incoming subscribed data.
        '''
        if DEBUG:
            logger.debug("UART received data: %s" % hexlify(value))
        with self.condition:
            self.recvbuf += value
            self.condition.notify()

    def recv(self, rsize, timeout=None):
        '''
        Blocking read from receive buffer.
        '''
        with self.condition:
            if not self.recvbuf:
                # wait if there is nothing in the receive buffer at all
                if not self.condition.wait(timeout=timeout):
                    return bytes()

            rv = self.recvbuf[0:rsize]
            self.recvbuf = self.recvbuf[rsize:]

        if DEBUG:
            log.debug("recv returning: %s" % hexlify(rv))
        return rv

class MicrochipBLEConn(_BLEConn):
    '''Microchip BLE module.
      The chip is described here:
        http://ww1.microchip.com/downloads/en/DeviceDoc/RN4870-71-Bluetooth-Low-Energy-Module-Data-Sheet-DS50002489D.pdf
        http://ww1.microchip.com/downloads/en/DeviceDoc/RN4870-71-Bluetooth-Low-Energy-Module-User-Guide-DS50002466C.pdf (see Appendix B.1)
    '''
    UART_TX = '49535343-1e4d-4bd9-ba61-23c647249616'
    UART_RX = '49535343-8841-43f4-a8d4-ecbe34729bb3'

class USRIOTBLEConn(_BLEConn):
    '''USR IOT WH-BLE 102 module.
      See WH-BLE102-User-Manual_V1.0.2.01.pdf
    '''
    UART_TX = '0003cdd1-0000-1000-8000-00805f9b0131'
    UART_RX = '0003cdd2-0000-1000-8000-00805f9b0131'
