# https://www.tutorialspoint.com/converting-tkinter-program-to-exe-file
# https://www.tutorialspoint.com/python/tk_labelframe.htm

import os
import json
import time
import math

from threading import Thread
from bluetooth.bluetooth import Bluetooth
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

ble = None
stop_app = False
uptime = 3

# https://stackoverflow.com/a/51266275/2710227
def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")

  return os.path.join(base_path, relative_path)

def clean_res(res_str):
  return res_str.replace('OK', '').replace('\x04', '').replace('>', '')

# this clock is not that accurate, there is some overlap
# with the 3s incrementer below and the 1 - 1.5 sec loop in bluetooth.py
def format_time(seconds):
  if (seconds < 60):
    return str(seconds) + 's'
  elif (seconds >= 60 and seconds < 3600):
    mins = math.floor(seconds / 60)
    seconds = math.floor(seconds % 60)

    return str(mins) + 'm ' + str(seconds) + 's'
  else:
    hours = math.floor(seconds / 3600)
    mins = math.floor((seconds - (hours * 3600))/60)
    seconds = seconds - ((hours * 3600) + (mins * 60))

    return str(hours) + 'h ' + str(mins) + 'm ' + str(seconds) + 's'

def update_status():
  ble.send_bytes_data = b'print(get_monocle_status())\x04' # this is a function flashed on monocle eg. main.py see monocle_main.py
  time.sleep(2)
  
  status = json.loads(clean_res(ble.res.decode('utf-8')))

  firmware_text.config(text="Firmware: " + status['firmware'])
  ram_text.config(text="RAM: " + str(status['ram']) + ' kb')
  storage_text.config(text="Storage: " + str(status['storage']) + ' kb')
  charging_text.config(text="Charging: " + ('yes' if status['charging'] else 'no'), fg=('#AAFF00' if status['charging'] else '#D22B2B'))
  batt_level_text.config(text="Battery: " + str(status['batt']) + " %")
  uptime_text.config(text="Uptime: " + format_time(uptime))

def monocle_not_found():
  connected_text.config(text = 'Searching for monocole...')

def run_app():
  global ble, uptime

  if (ble.connected):
    connected_text.config(text='Connected', fg='#AAFF00')
    connection_button.config(text='Disconnect')

    ble.send_bytes_data = b'\x03\x01'
    time.sleep(2)

    ble.send_bytes_data = b'import device\x04' # have to reimport this for some reason
    time.sleep(2)

    update_status()

    time.sleep(5)

    while (stop_app != True or ble.connected != False):
      uptime += 5
      update_status()
      time.sleep(5)

def start_ble():
  global ble

  ble = Bluetooth(monocle_not_found, run_app)
  Thread(target=ble.start).start()
  
  time.sleep(3)
  run_app()

def handle_connection():
  global stop_app, uptime

  if (ble.connected):
    ble.disconnect = True
    stop_app = True
    connected_text.config(text='Disconnecting...')
    connection_button.config(text='Disconnecting...')
    time.sleep(2)
    connected_text.config(text='Disconnected', fg="#D22B2B")
    connection_button.config(text='Connect')
  else:
    uptime = 0
    ble.disconnect = False
    stop_app = False
    Thread(target=start_ble).start()

# handle closing Monocle Dock
def on_close():
  global ble, stop_app

  ble.disconnect = True # stops connection loop
  stop_app = True
  win.destroy()

win = Tk()
win.title('Monocle Dock')
win.geometry("300x420")
win.bg = 'white'
win.iconbitmap(resource_path('monocle_24.ico'))

canvas = Canvas(win, width=300, height=280, bg='white') # related height
canvas.pack()

img = Image.open(resource_path('monocle_200.jpg'))
img = ImageTk.PhotoImage(img)
canvas.create_image(50, 40, anchor=NW, image=img) # related height

#Creates a Frame
frame = LabelFrame(win, width=300, height=50, bd=1, text='Monocle status:', bg='#282828', fg='#0096FF')
frame.pack(fill='both', expand='yes')
frame.pack_propagate() # False keeps width

# text
connected_text = Label(frame, text='Connecting...', bg='#282828', fg='#AAFF00')
connected_text.place(x=0, y=0)

charging_text = Label(frame, text="Charging:", bg='#282828', fg='#AAFF00')
charging_text.place(x=0, y=20)

batt_level_text = Label(frame, text="Battery:", bg='#282828', fg='#AAFF00')
batt_level_text.place(x=0, y=40)

firmware_text = Label(frame, text="Firmware:", bg='#282828', fg='#AAFF00', anchor="e")
firmware_text.place(x=150, y=0)

ram_text = Label(frame, text="RAM:", bg='#282828', fg='#AAFF00', anchor="e")
ram_text.place(x=150, y=20)

storage_text = Label(frame, text="Storage:", bg='#282828', fg='#AAFF00', anchor="e")
storage_text.place(x=150, y=40)

uptime_text = Label(frame, text="Uptime:", bg='#282828', fg='#AAFF00', anchor="e")
uptime_text.place(x=0, y=60)

# manual connect/disconnect button
connection_button = ttk.Button(frame, text= 'Disconnect' if ble and ble.connected else 'Connecting...', command=handle_connection)
connection_button.place(x=110, y=85)

Thread(target=start_ble).start()

win.protocol("WM_DELETE_WINDOW", on_close)

# render UI
win.mainloop()
