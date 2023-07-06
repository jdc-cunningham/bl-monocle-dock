import time
import touch
import microphone
import display
import json

red_rect = display.Rectangle(0, 0, 639, 400, 0xFF0000)

def record_audio():
  display.show(red_rect)
  microphone.record(seconds=4.0, bit_depth=8, sample_rate=8000)
  time.sleep(0.5)

  samples = 2

  chunk1 = microphone.read(samples)
  chunk2 = microphone.read(samples)

  display.show()

  res = {}

  if chunk1 == None:
    res = {}
  elif chunk2 == None:
    res = {
      "a": str(chunk1)
    }
  else:
    res = {
      "a": str(chunk1),
      "b": str(chunk2)
    }

  return json.dumps(res)
