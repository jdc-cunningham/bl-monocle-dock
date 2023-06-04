import os
import gc
import json
import display
import device

gc.collect()
display.clear()
device.prevent_sleep(True)

def get_storage():
  fs_stat = os.statvfs("/")
  return str(fs_stat[0] * fs_stat[3])

def get_monocle_status():
  gc.collect()
  charging = device.is_charging()
  ram = gc.mem_free()
  storage = get_storage()
  ver = device.VERSION
  batt = device.battery_level()

  obj = {
    "charging": charging,
    "ram": ram,
    "storage": storage,
    "firmware": ver,
    "batt": batt
  }

  return json.dumps(obj)
