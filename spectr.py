# import cv2
import matplotlib
import pyaudio
import numpy as np
import threading
from matplotlib import pyplot as plt
import scipy.signal
import time


CHUNK = 960
QUALITY = 44100

plot = plt.plot([0], [0], label='data', clip_on=False, fillstyle='none')
# plot[0].axes.set_ylabel('Frequence [Hz]')
# plot[0].axes.set_xlabel('Time [sec]')
figure = plot[0].figure

fps = 1000 / 5

f = np.array([])
t = np.array([])
data = np.array([])


def prepare_input(input_data):
	global plot, figure, t, f, data
	#
	# f, t, ddata = scipy.signal.spectrogram(input_data, QUALITY)
	#
	# if data.size == 0:
	# 	data = ddata
	# else:
	# 	data = np.hstack((data, ddata))
	# 	dt = len(data[0]) / 4 * 0.5
	#
	# 	if len(data[0]) > 4 * 10:
	# 		data = data[0:,4:]
	
	if data.size == 0:
		data = input_data
	else:
		data = np.append(data, input_data)
		if data.size > 960 * 10:
			data = data[960:]
	
	# t = t + dt
	# f = np.append(f, df)
	# data = np.vstack((data, ddata))
	
	# np.arange(0, data.shape[1]), np.arange(0, QUALITY, QUALITY / data.shape[0]),
	# plot[0].axes.pcolormesh(data, shading='nearest', rasterized=True)
	
	 #data)


def draw():
	global figure
	while plot is not None:
		plot[0].axes.specgram(data, Fs=QUALITY)
		
		# cv2.imshow('w', a)
		figure.canvas.draw()
		figure.canvas.flush_events()
		time.sleep(fps / 1000)

def audio_input():
	p = pyaudio.PyAudio()
	stream = p.open(QUALITY, 1, pyaudio.paInt16, True, frames_per_buffer=CHUNK)
	
	while plot is not None:
		data = stream.read(CHUNK)
		prepare_input(np.frombuffer(data, np.int16))
	
	stream.stop_stream()
	stream.close()
	p.terminate()
	
	
if __name__ == '__main__':
	threading.Thread(target=audio_input).start()
	threading.Thread(target=draw).start()
	
	# matplotlib.rcParams.clear()
	# plot[0].figure.callbacks.blocked()
	
	plt.show()
	plot = None
	