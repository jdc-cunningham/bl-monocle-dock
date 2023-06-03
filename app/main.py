# https://www.tutorialspoint.com/converting-tkinter-program-to-exe-file
# https://www.tutorialspoint.com/python/tk_labelframe.htm

import time

from threading import Thread
from bluetooth.bluetooth import Bluetooth
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

ble = None

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
frame = LabelFrame(win, width= 300, height= 50, bd=1, text='Monocle status:', bg='#282828', fg='#AAFF00')
frame.pack(fill='both', expand='yes')
frame.pack_propagate() # False keeps width

status_text = Label(frame, text='Connecting...', anchor='sw')
status_text.place(relx=0, rely=50, anchor='sw') # lol NW
status_text.pack()

def clean_res(res_str):
  return res_str.replace('OK', '').replace('\x04', '').replace('>', '')

def app_logic():
  global ble

  ble = Bluetooth()
  Thread(target=ble.start).start()
  
  time.sleep(3)

  if (ble.connected):
    ble.send_bytes_data = b'\x03\x01'
    time.sleep(2)
    ble.send_bytes_data = b'import device;print(device.VERSION)\x04'
    time.sleep(2)
    status_text.config(text = clean_res(ble.res.decode('utf-8')))
    win.update()
    print('sent all')

# handle closing Monocle Dock
def on_close():
  global ble

  ble.disconnect = True # stops connection loop
  win.destroy()

win.after(1000, app_logic) # run app logic after desktop app renders
win.protocol("WM_DELETE_WINDOW", on_close)

# render UI
win.mainloop()
