# https://www.tutorialspoint.com/converting-tkinter-program-to-exe-file
# https://www.tutorialspoint.com/python/tk_labelframe.htm

import json
import time

from threading import Thread
from bluetooth.bluetooth import Bluetooth
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

ble = None
stop_app = False

def clean_res(res_str):
  return res_str.replace('OK', '').replace('\x04', '').replace('>', '')

def update_status():
  ble.send_bytes_data = b'print(get_monocle_status())\x04' # this is a function flashed on monocle eg. main.py see monocle_main.py
  time.sleep(2)
  
  status = json.loads(clean_res(ble.res.decode('utf-8')))

  firmware_text.config(text="Firmware: " + status['firmware'])
  ram_text.config(text="RAM: " + str(status['ram']) + ' kb')
  storage_text.config(text="Storage: " + str(status['storage']) + ' kb')
  charging_text.config(text="Charging: " + ('yes' if status['charging'] else 'no'), fg=('#AAFF00' if status['charging'] else '#D22B2B'))
  batt_level_text.config(text="Battery: " + str(status['batt']) + " %")

def monocle_not_found():
  connected_text.config(text = 'Searching for monocole...')

def run_app():
  global ble

  if (ble.connected):
    connected_text.config(text='Connected')
    connection_button.config(text='Disconnect')

    ble.send_bytes_data = b'\x03\x01'
    time.sleep(2)

    ble.send_bytes_data = b'import device\x04' # have to reimport this for some reason
    time.sleep(2)

    update_status()

    time.sleep(5)

    while (stop_app != True):
      update_status()
      time.sleep(5)

def start_ble():
  global ble

  ble = Bluetooth(monocle_not_found, run_app)
  Thread(target=ble.start).start()
  
  time.sleep(3)
  run_app()

def handle_connection():
  if (ble.connected):
    ble.disconnect = True
    connected_text.config(text='Disconnecting...')
    connection_button.config(text='Disconnecting...')
    time.sleep(2)
    connected_text.config(text='Disconnected')
    connection_button.config(text='Connect')
  else:
    start_ble()

# handle closing Monocle Dock
def on_close():
  global ble, stop_app

  ble.disconnect = True # stops connection loop
  stop_app = True
  win.destroy()

win = Tk()
win.title('Monocle Dock')
win.geometry("300x400")
win.bg = 'white'
win.iconbitmap('monocle_24.ico')

canvas = Canvas(win, width=300, height=280, bg='white') # related height
canvas.pack()

img = Image.open('monocle_200.jpg')
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

# manual connect/disconnect button
connection_button = ttk.Button(frame, text= 'Disconnect' if ble and ble.connected else 'Connecting...', command=handle_connection)
connection_button.place(x=110, y=65)

Thread(target=start_ble).start()

win.protocol("WM_DELETE_WINDOW", on_close)

# render UI
win.mainloop()
