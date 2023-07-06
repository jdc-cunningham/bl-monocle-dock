import time
import wave
import json
import numpy as np

from bluetooth.bluetooth import Bluetooth
from threading import Thread

file_counter = 1
res_counter = 0 # lazy way to avoid first response from raw mode
ble = None

# https://stackoverflow.com/a/75026723/2710227
num_channels    = 1
sample_width    = 8
sample_rate     = 8000
frequency       = 440
duration        = 4

def clean_res(res_str):
  return res_str.replace('OK', '').replace('\x04', '').replace('>', '')

def monocle_not_found():
  print('searching for monocle...')

def run_app():
  global ble, file_counter, res_counter

  if (ble.connected):
    print('monocle connected')
    ble.send_bytes_data = b'\x03\x01' # raw repl mode
    time.sleep(2) # or this
    print(ble.res.decode('utf-8')) # should see raw REPL; in terminal
    ble.res = None

  # record sound
  while True:
    print('loop')
    print(ble.res)

    if (ble.res == None or ble.res == b'OK'):
      print('no data')
      
      # trigger recording to start on monocle side
      ble.send_bytes_data = b'print(record_audio())\x04'
    else:
      res = json.loads(clean_res(ble.res.decode('utf-8')))

      print('res>')
      print(res)
      
      # # dumb
      # res_a1 = res['a'].split("b'")[1]
      # res_a2 = bytes(res_a1.split("'")[0], 'utf-8')

      # res_b1 = res['b'].split("b'")[1]
      # res_b2 = bytes(res_b1.split("'")[0], 'utf-8')

      with wave.open("audio_file" + str(file_counter) + ".wav", "wb") as audiofile:
        audiofile.setsampwidth(2)
        audiofile.setnchannels(1)
        audiofile.setframerate(44100)
        audiofile.writeframes(b''.join(res))

      print('file written')
      file_counter += 1

    ble.res = None
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
