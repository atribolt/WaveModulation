import numpy as np
from math import sin, cos, fabs
import matplotlib.pyplot as plt
#import cv2

#img = cv2.imread('./test.png')
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

freq = 12.50

ax = np.arange(0, 5, 0.0001)
base1 = [sin(x * freq) for x in ax]
base1 = np.array(base1)

base2 = [sin(x * 4400) for x in ax]
base2 = np.array(base2)

data1 = np.array([sin(x) for x in ax])
data2 = np.array([cos(x) for x in ax])

af1 = base1 * data1  # np.array([fabs(n) for n in data1])
af2 = base2 * data2  # np.array([fabs(n) for n in data2])

fm1 = [sin(x * freq + data1[i]) for i,x in enumerate(ax)]

a = plt.plot(data1, label='data1')
# b = plt.plot(data2, label='data2')
#c = plt.plot(af1, label='AF1')
fm = plt.plot(fm1, label='FM1')
# d = plt.plot(af2, label='AF2')

tbase1 = [sin(x * freq) for x in ax]
#ddata1 = af1 / tbase1
ddata1 = []

e = plt.plot(ddata1, label='ddata1')

fig = e[0].figure


def mouse_scroll(event):
  step = event.step / 100.0
  
  global freq, tbase1, ddata1
  freq += step
  tbase1 = [sin(x * freq) for x in ax]
  ddata1 = af1 / tbase1
  
  e[0].set_ydata(ddata1)
  fig.canvas.draw()


fig.canvas.mpl_connect('scroll_event', mouse_scroll)

plt.legend()
plt.show()
