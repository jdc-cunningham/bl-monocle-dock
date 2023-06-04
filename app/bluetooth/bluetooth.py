"""
UART Service
-------------

An example showing how to write a simple program using the Nordic Semiconductor
(nRF) UART service.

https://github.com/hbldh/bleak/blob/develop/examples/uart_service.py

"""

import time
import asyncio
import sys
from itertools import count, takewhile
from typing import Iterator

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

class Bluetooth():
  def __init__(self, monocle_not_found, run_app):
    self.UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    self.UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    self.UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
    self.client = None
    self.connected = False
    self.rx_char = None
    self.res = None
    self.disconnect = False
    self.send_bytes_data = None # eg. b'string'
    self.monocle_not_found = monocle_not_found
    self.first_conn_failed = False
    self.run_app = run_app

  async def repl_api(self):
    def match_nus_uuid(device: BLEDevice, adv: AdvertisementData):
      # This assumes that the device includes the UART service UUID in the
      # advertising data. This test may need to be adjusted depending on the
      # actual advertising data supplied by the device.
      if self.UART_SERVICE_UUID.lower() in adv.service_uuids:
        return True

      return False

    device = await BleakScanner.find_device_by_filter(match_nus_uuid)

    if device is None:
      print("no matching device found, you may need to edit match_nus_uuid().")
      self.first_conn_failed = True
      self.monocle_not_found()
      time.sleep(1)
      await self.repl_api() # keep trying to connect
    else:
      def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        self.connected = False

        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
          task.cancel()

      def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
        self.res = data
        print("received:", data)

      async with BleakClient(device, disconnected_callback=handle_disconnect) as client:
        await client.start_notify(self.UART_TX_CHAR_UUID, handle_rx)

        self.connected = True

        nus = client.services.get_service(self.UART_SERVICE_UUID)
        self.rx_char = nus.get_characteristic(self.UART_RX_CHAR_UUID)

        while self.disconnect != True:
          if (self.send_bytes_data):
            await client.write_gatt_char(self.rx_char, self.send_bytes_data)
            await asyncio.sleep(0.5)
            self.send_bytes_data = None

          if (self.first_conn_failed):
            self.first_conn_failed = False
            self.run_app()

          time.sleep(1) # slow this loop down, does mean longer response time
        else:
          self.connected = False

  def start(self):
    try:
      asyncio.run(self.repl_api())
    except asyncio.CancelledError:
      pass
