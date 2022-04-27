import socket, signal, numpy as np, time
import threading

import matplotlib.pyplot as plt


listenIp = '0.0.0.0'
listenPort = 20001

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

chunk_size = 2048
frequesncy = 42 * 1000 * 1000

buffer_max = 5000
buffer = [-30000, 30000] * (buffer_max // 2)

def listen_forewer():
  global buffer, plot
  
  server.bind((listenIp, listenPort))
  last_draw = time.time_ns()
  while True:
    msg, address = server.recvfrom(chunk_size)
    
    buffer += list(np.frombuffer(msg, np.int16))
    buffer = buffer[len(buffer) - buffer_max:] if len(buffer) >= buffer_max else buffer
    
    plot[0].set_ydata(buffer)
    
    if time.time_ns() - last_draw > 200_000_000:
      plot[0].figure.canvas.draw()
      last_draw = time.time_ns()
  
  
def set_freq(ev):
  pass
  
plot = plt.plot(buffer, label='AM', lw=0.1)

thread = threading.Thread(target=listen_forewer, name='UDPServer')
thread.start()

plt.legend()
plt.show()
