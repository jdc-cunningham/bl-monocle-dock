import time
import microphone
import display
import json

red_rect = display.Rectangle(0, 0, 639, 400, 0xFF0000)

def record_audio():
  display.show(red_rect)
  microphone.record(seconds=4.0, bit_depth=8, sample_rate=8000)
  time.sleep(0.5)

  samples = 2

  display.show()

  while True:
    audio_samples = []

    chunk1 = microphone.read(samples)
    chunk2 = microphone.read(samples)

    if chunk1 == None:
      break
    elif chunk2 == None:
      audio_samples.append(chunk1)
    else:
      audio_samples.append(chunk1)
      audio_samples.append(chunk2)
  
    return json.dumps(audio_samples)
