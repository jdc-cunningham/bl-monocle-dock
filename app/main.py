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

#Define a function to show a message
# def myclick():
#    message= "Hello "+ entry.get()
#    label= Label(frame, text= message, font= ('Times New Roman', 14, 'italic'))
#    entry.delete(0, 'end')
#    label.pack(pady=30)

#Creates a Frame
frame = LabelFrame(win, width= 300, height= 50, bd=1, text='Monocle status:')
frame.pack(fill='both', expand='yes')
frame.pack_propagate(True) # False keeps width

status_text = Label(frame, text='Disconnected...')
status_text.pack()

#Create an Entry widget in the Frame
# entry = ttk.Entry(frame, width= 40)
# entry.insert(INSERT, "Enter Your Name")
# entry.pack()
#Create a Button
# ttk.Button(win, text= "Click", command= myclick).pack(pady=20)

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
    status_text.config(text = ble.res.decode('utf-8').replace('OK', '').replace('\x04', '').replace('>', ''))
    win.update()
    print('sent all')

def on_close():
  global ble

  ble.disconnect = True # stops connection loop
  win.destroy()

win.after(1000, app_logic)
win.protocol("WM_DELETE_WINDOW", on_close)

# render UI
win.mainloop()
