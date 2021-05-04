import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter

import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class GraphView:
    def __init__(self, datatype, func, fig_rule=None):
        self._datatype = datatype
        self._func = func
        self._fig_rule = fig_rule

    def plot(self, axes, figure):
        if self._datatype == '2d':
            self.plot2d(axes, figure)
        elif self._datatype == '3d':
            self.plot3d(axes, figure)
        elif self._datatype == '3d_field':
            self.plot3d_field(axes, figure)


    def plot2d(self, axes, figure):
        r = np.linspace( 0, 40, 2000)
        Rf = self._func(r)
        plt.clf()
        plt.rcParams["mathtext.fontset"] = 'cm'
        plt.rcParams['mathtext.default'] = 'it'
        plt.rcParams["font.size"] = 18
        axes = figure.add_subplot(111, xlabel='$ r / a_0 $', ylabel='$ [r \\times R(r)] ^2 $')
        plt.plot(r, Rf)
        axes.set_title('Radial Function : $ [r R(r)] ^2 $')
        axes.set_xlim(0, 40)
        axes.set_ylim(0, 0.6)
        axes.xaxis.set_ticks(np.arange(0, 40, 4))
        axes.grid()
        plt.draw()

    def plot3d(self, axes, figure):
        plt.clf()
        plt.rcParams["mathtext.fontset"] = 'cm'
        plt.rcParams['mathtext.default'] = 'it'
        plt.rcParams["font.size"] = 18

        _phi = np.linspace(0, 2*np.pi, 360)
        _theta = np.linspace(0, np.pi, 180)
        phi, theta = np.meshgrid(_phi, _theta)

        r = self._func(theta, phi) #5 * np.cos(theta) ** 3 - 3 * np.cos(theta) 
        x = r*np.cos(phi)*np.sin(theta)
        y = r*np.sin(phi)*np.sin(theta)
        z = r*np.cos(theta)

        axes = figure.add_subplot(111, projection='3d', title='Spherical Surface Function', xlabel='X', ylabel='Y', zlabel='Z')
        figure.add_axes(axes)
        
        axes.plot_surface(x,y,z)
        axes.set_title('Spherical Surface Function : $ Y_l(\\theta, \\phi) $')

        axes.set_xlim(-1,1)
        axes.set_ylim(-1,1)
        axes.set_zlim(-1,1)
        axes.set_box_aspect([1,1,1])
        plt.draw()

    def plot3d_field(self, axes, figure):
        plt.clf()
        plt.rcParams["mathtext.fontset"] = 'cm'
        plt.rcParams['mathtext.default'] = 'it'
        plt.rcParams["font.size"] = 18

        _r = np.linspace(1e-3, 40 ** 2, 301)
        _r = np.sqrt(_r)
        _phi = np.linspace(0, 2*np.pi, 5)
        _theta = np.linspace(0, np.pi, 31)
        r, phi, theta = np.meshgrid(_r, _phi, _theta)

        delta_r = 1e-3
        delta_theta = 1e-3
        delta_phi = 1e-3

        func_absolute = lambda r, theta, phi : self._func[0](r, theta, phi).conjugate() * self._func[0](r, theta, phi) * (r**2) * np.sin(theta)

        wave_abs_func_r = 1*(func_absolute(r + delta_r, theta, phi) - func_absolute(r, theta, phi)) / (delta_r)
        wave_abs_func_theta = 1*(func_absolute(r, theta + delta_theta, phi) - func_absolute(r, theta, phi)) / (delta_theta)
        wave_abs_func_phi = 1*(func_absolute(r, theta, phi + delta_phi) - func_absolute(r, theta, phi)) / (delta_phi)
        wave_abs_func = func_absolute(r, theta, phi)

        wave_flow_func = self._func[0](r, theta, phi)
        wave_flow_func_r = self._func[0](r + delta_r, theta, phi) - wave_flow_func
        wave_flow_func_theta = self._func[0](r, theta + delta_theta, phi) - wave_flow_func
        wave_flow_func_phi = self._func[0](r, theta, phi + delta_phi) - wave_flow_func

        x = r*np.cos(phi)*np.sin(theta)
        y = r*np.sin(phi)*np.sin(theta)
        z = r*np.cos(theta)

        x = x.flatten()
        y = y.flatten()
        z = z.flatten()
        r = r.flatten()
        phi = phi.flatten()
        theta = theta.flatten()

        wave_abs_func_r = wave_abs_func_r.flatten()
        wave_abs_func_theta = wave_abs_func_theta.flatten()
        wave_abs_func_phi = wave_abs_func_phi.flatten()

        u = wave_abs_func_r * np.sin(theta) * np.cos(phi)  + wave_abs_func_theta * np.cos(theta) * np.cos(phi) / r
        v = wave_abs_func_r * np.sin(theta) * np.sin(phi)  + wave_abs_func_theta * np.cos(theta) * np.sin(phi) / r
        w = wave_abs_func_r * np.cos(theta) - wave_abs_func_theta * np.sin(theta) / r
        wave_func_max = np.max(wave_abs_func.flatten())
        eval_f = wave_abs_func.flatten() >= wave_func_max * 1e-2

        for i in range(0, len(eval_f)):
            if eval_f[i] == False:
                x[i], y[i], z[i], u[i], v[i], w[i] = None, None, None, None, None, None
                

        

        axes = figure.add_subplot(111, projection='3d', xlabel='X', ylabel='Y', zlabel='Z')
        figure.add_axes(axes)
        
        axes.quiver(x,y,z,u,v,w, arrow_length_ratio=0.1,pivot='middle',length=10, linewidths=3)
        #axes.quiver([1e-16,0],[0,0],[1,1],[0,0],[0,0],[-1,-1], arrow_length_ratio=0.1,pivot='middle')
        
        axes.set_title('Wave Function : $ \\varphi(r,\\theta, \\phi) $')
        #axes.grid(False)
        axes.set_xlim(-40,40)
        axes.set_ylim(-40,40)
        axes.set_zlim(-40,40)
        #axes.grid(False)
        #axes.set_xticks([-40,0,40])
        #axes.set_yticks([-40,0,40])
        #axes.set_zticks([-40,0,40])
        axes.set_box_aspect([1,1,1])
        axes.view_init(elev=0,azim=90)

        if self._fig_rule != None:
            self._fig_rule(axes, figure)
        plt.draw()



class NavigationToolbarExt(NavigationToolbar2Tk):
    def __init__(self, canvas=None, master=None, figure=None):
        super().__init__(canvas, master)
        self.canvas = canvas
        self.master = master
        self.figure = figure



class SphericalSurface(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.master = root
        self._figure = plt.figure(figsize=(10,6))
        
        self._canvas = FigureCanvasTkAgg(self._figure, master=root)
        self._canvas.draw()
        self._canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self._toolbar = NavigationToolbarExt(self._canvas, self, self._figure)
        self._axes_now = None

        self.init_plot()


    def init_plot(self):
        plt.clf()
        self._figure.clf()
        ax = plt.subplot(111)

    def plot(self, graph_func, fig_rule):
        plt.clf()

        self._axes_now = self._figure.add_subplot(111, projection='3d', title='Spherical Surface Function', xlabel='X', ylabel='Y', zlabel='Z')
        self._figure.add_axes(self._axes_now)
        graph_func.plot(self._axes_now, self._figure)


"""
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Spherical Surface Demonstration")

    window = SphericalSurface(root)
    root.protocol("WM_DELETE_WINDOW", (lambda : [window.quit()]))

    window.mainloop()
"""

"""
_phi = np.linspace(0, 2*np.pi, 100)
_theta = np.linspace(0, np.pi, 100)
phi, theta = np.meshgrid(_phi, _theta)

r = np.abs( np.real(np.sin(theta) * np.exp(1j * phi))) #5 * np.cos(theta) ** 3 - 3 * np.cos(theta) 
x = r*np.cos(phi)*np.sin(theta)
y = r*np.sin(phi)*np.sin(theta)
z = r*np.cos(theta)




fig = plt.figure(figsize=(13,8))
ax = fig.add_subplot(111, projection='3d', title='Spherical Surface Function', xlabel='X', ylabel='Y', zlabel='Z')
ax.plot_surface(x,y,z)
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_zlim(-1,1)

plt.show()
"""
"""
r = np.linspace(0, 40, 2000)

fig, ax = plt.subplots()
ax.grid()
ax.xaxis.set_ticks(np.arange(0, 40, 4))
#Rf = (r ** 2) * np.exp(-2 * r)
#Rf = (r ** 2) * ((1 - 0.5 * r) * np.exp(-r/2)) ** 2
Rf = (r ** 2) * ((1 - (2/3) * r + (2/27) * (r**2)) * np.exp(-r/3)) ** 2

plt.plot(r, Rf)

plt.show()
"""
