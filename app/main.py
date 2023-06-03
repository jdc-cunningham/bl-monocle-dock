import time

from threading import Thread
from bluetooth.bluetooth import Bluetooth

ble = Bluetooth()

Thread(target=ble.start).start()

ble.send_bytes_data = b'\x03\x01'

time.sleep(5)

ble.disconnect = True