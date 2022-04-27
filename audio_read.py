import math
import sys

import speech_recognition as sr
import wave
import numpy as np
import matplotlib.pyplot as plt
from playsound import playsound


# rec = sr.Recognizer()
# with sr.Microphone() as mic:
#   audio = rec.listen(mic, 10, 5)
#
# print(audio.sample_rate, audio.sample_width)
#
# with wave.open('test1.wav', 'wb') as wav:
#   wav.setnchannels(1)
#   wav.setsampwidth(audio.sample_width)
#   wav.setframerate(audio.sample_rate)
#   wav.writeframesraw(audio.frame_data)
#
# sys.exit(0)

wav = wave.open('test.wav', 'rb')
wav2 = wave.open('test1.wav', 'rb')

_, _, _, nframes, _, _ = wav.getparams()


class audio:
  frame_data = wav.readframes(nframes)
  sample_width = 2
  sample_rate = 44100


cut_front = 4000
array = np.frombuffer(audio.frame_data, dtype=np.int16)
array = np.array(array, np.float_)
array = array[cut_front:]

array1 = np.frombuffer(wav2.readframes(wav2.getparams()[3]), dtype=np.int16)
array1 = np.array(array1, np.float_)
array1 = array1[cut_front:]

freq = 47 * 1_000_000
freq1 = 10 * 1_000_000

ax = np.arange(0, len(array), 0.001)
ax = ax[:len(array)]

base = np.array([math.sin(x * freq) for x in ax])
base1 = np.array([math.sin(x * freq1) for x in ax])

AM = base * array
AM1 = base1 * array1

finded = np.array([math.sin(x * freq) for x in ax])
AM = AM  # * AM1

decode = AM / finded
decode1 = AM1 / np.array([math.sin(x * freq1) for x in ax])

#plt.plot(base, label='base')
#a = plt.plot(array, label='audio')

limit = 1000

b = plt.plot(AM[:limit], label='AM')
b1 = plt.plot(AM1[:limit], label='AM1')
c = plt.plot(decode[:limit], label='decode')
d = plt.plot(decode1[:limit], label='decode1')

n = freq
def set_freq(ev):
  global finded, decode, n
  
  if ev.step > 0:
    n = freq
  else:
    n = freq1
  
  finded = np.array([math.sin(x * n) for x in ax])
  decode = AM / finded

  c[0].set_ydata(decode[:limit])
  c[0].figure.canvas.draw()

  with wave.open('demodule.wav', 'wb') as dwav:
     dwav.setnchannels(1)
     dwav.setsampwidth(audio.sample_width)
     dwav.setframerate(audio.sample_rate)
     
     dwav.writeframesraw(np.array(decode, np.int16))

def play(ev):
  playsound('demodule.wav')

c[0].figure.canvas.mpl_connect('scroll_event', set_freq)
c[0].figure.canvas.mpl_connect('button_release_event', play)

plt.legend()
plt.show()
