import time
import wave
import numpy as np

from bluetooth.bluetooth import Bluetooth
from threading import Thread

loop_counter = 0
res_counter = 0 # lazy way to avoid first response from raw mode
ble = None

# https://stackoverflow.com/a/75026723/2710227
num_channels    = 1
sample_width    = 8
sample_rate     = 8000
frequency       = 440
duration        = 4

def monocle_not_found():
  print('searching for monocle...')

def run_app():
  global ble, loop_counter, res_counter

  if (ble.connected):
    print('monocle connected')
    ble.send_bytes_data = b'\x03\x01' # raw mode

  while True:
    loop_counter += 1

    if (ble.res != None and res_counter == 0):
      res_counter += 1
      continue

    if (ble.res != None or res_counter != 0):
      print('data received')

      n = round(sample_rate/frequency)
      t = np.linspace(0, 1/frequency, n)
      data = (127*np.sin(2*np.pi*frequency*t)).astype(np.int8)
      periods = round(frequency*duration)

      with wave.open('test.wav', 'w') as wavfile:
        wavfile.setnchannels(num_channels)
        wavfile.setsampwidth(sample_width)
        wavfile.setframerate(sample_rate)

        for _ in range(periods):
          wavfile.writeframes(data)

        print('file written')

    print('waiting for data ' + str(loop_counter))
    time.sleep(1)

def start_ble():
  global ble

  ble = Bluetooth(monocle_not_found, run_app)
  Thread(target=ble.start).start()
  
  time.sleep(3)
  run_app()

# this loop is hard to terminate by ctrl+c
# didn't add a way to stop the thread easily
start_ble()
