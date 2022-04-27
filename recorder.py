import speech_recognition as sr
import socket, signal
import numpy as np
import time, math


is_stop = False
rec = sr.Recognizer()

def stop(*args):
  global is_stop
  is_stop = True

signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)

with sr.Microphone() as mic:
  server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  servers = [('localhost', 20001)]

  last_time = time.time_ns()
  frequesnce = 42 * 1000 * 1000  # MHz
  
  while not is_stop:
    buffer = mic.stream.read(mic.CHUNK)
    
    lt = last_time
    last_time = time.time_ns()

    dx = np.arange(lt, lt + len(buffer)/2)
    base_wave = np.array([math.sin(x * frequesnce) for x in dx])
    
    buffer = np.frombuffer(buffer, dtype=np.int16)
    buffer = np.array(buffer, dtype=np.float_)
    
    buffer *= base_wave

    [server.sendto(buffer, address) for address in servers]
