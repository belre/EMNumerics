import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

_phi = np.linspace(0, 2*np.pi, 100)
_theta = np.linspace(0, np.pi, 100)
phi, theta = np.meshgrid(_phi, _theta)

r = np.abs((5*np.cos(theta)**2 - 1)*np.sin(theta)*np.cos(phi)) 
x = r*np.cos(phi)*np.sin(theta)
y = r*np.sin(phi)*np.sin(theta)
z = r*np.cos(theta)

fig = plt.figure()
ax = fig.add_subplot(111,projection="3d")
ax.plot_surface(x, y, z)
ax.set_zlim(-1,1)
plt.show()