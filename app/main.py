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

win = Tk()
win.title('Monocle Dock')
win.geometry("300x400")
win.bg = 'white'
win.iconbitmap('monocle_24.ico')

canvas = Canvas(win, width=300, height=300, bg='white')
canvas.pack()

img = Image.open('monocle_200.jpg')
img = ImageTk.PhotoImage(img)
canvas.create_image(50, 50, anchor=NW, image=img)

#Creates a Frame
frame = LabelFrame(win, width= 300, height= 50, bd=1, text='Monocle status:', bg='#282828', fg='#0096FF')
frame.pack(fill='both', expand='yes')
frame.pack_propagate() # False keeps width

connected_text = Label(frame, text='Connecting...', bg='#282828', fg='#AAFF00')
connected_text.place(x=0, y=0)

charging_text = Label(frame, text="Charging:", bg='#282828', fg='#AAFF00')
charging_text.place(x=0, y=20)

firmware_text = Label(frame, text="Firmware:", bg='#282828', fg='#AAFF00', anchor="e")
firmware_text.place(x=150, y=0)

ram_text = Label(frame, text="RAM:", bg='#282828', fg='#AAFF00', anchor="e")
ram_text.place(x=150, y=20)

storage_text = Label(frame, text="Storage:", bg='#282828', fg='#AAFF00', anchor="e")
storage_text.place(x=150, y=40)

def clean_res(res_str):
  return res_str.replace('OK', '').replace('\x04', '').replace('>', '')

def update_status():
  ble.send_bytes_data = b'print(get_monocle_status())\x04' # this is a function flashed on monocle eg. main.py see monocle_main.py
  time.sleep(2)
  
  status = json.loads(clean_res(ble.res.decode('utf-8')))

  firmware_text.config(text = "Firmware: " + status['firmware'])
  ram_text.config(text = "RAM: " + str(status['ram']) + ' kb')
  storage_text.config(text = "Storage: " + str(status['storage']) + ' kb')
  charging_text.config(text = "Charging: " + ('yes' if status['charging'] else 'no'))

def monocle_not_found():
  connected_text.config(text = 'Searching for monocole...')
  win.update()

def run_app():
  global ble

  if (ble.connected):
    connected_text.config(text = 'Connected')
    ble.send_bytes_data = b'\x03\x01'
    time.sleep(2)
    ble.send_bytes_data = b'import device\x04' # have to reimport this for some reason
    time.sleep(2)
    update_status()
    win.update()

    time.sleep(5)

    while (stop_app != True):
      update_status()
      win.update()
      time.sleep(5)

def start_ble():
  global ble

  ble = Bluetooth(monocle_not_found, run_app)
  Thread(target=ble.start).start()
  
  time.sleep(3)
  run_app()

# handle closing Monocle Dock
def on_close():
  global ble, stop_app

  ble.disconnect = True # stops connection loop
  stop_app = True
  win.destroy()

Thread(target=start_ble).start()

win.protocol("WM_DELETE_WINDOW", on_close)

# render UI
win.mainloop()
