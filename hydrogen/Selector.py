
import numpy as np

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from functools import partial
from Function import SphericalSurface, GraphView

# https://stackoverflow.com/questions/49888623/tkinter-hovering-over-button-color-change
class MarkerButton(tk.Button):
    def __init__(self, master, **kwargs):
        tk.Button.__init__(self,master=master,**kwargs)
        self.turn_off()

    def turn_on(self):
        self['highlightbackground'] = "yellow" 
        self['fg'] = "black"
        
    def turn_off(self):
        self['highlightbackground'] = "gray"
        self['fg'] = "black"

    

class Application(tk.Frame):
    _before_action_button = None

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self._graph_object = None

    def R_1s(self, r):
        return 2 * np.exp(-r)

    def R_2s(self, r):
        return (1/np.sqrt(2)) * (1-r/2) * np.exp(-r/2)

    def R_2p(self, r):
        return (1/(2*np.sqrt(6))) * r * np.exp(-r/2)

    def R_3s(self, r):
        return (2/(3*np.sqrt(3))) * (1-2*r/3+2*r*r/27) * np.exp(-r/3)

    def R_3p(self, r):
        return (8 / (27 * np.sqrt(6))) * r * (1 - r / 6) * np.exp(-r/3)

    def R_3d(self, r):
        return (4 / (81 * np.sqrt(30))) * (r**2) * np.exp(-r/3)

    def R_4s(self, r):
        return (1 / 4) * (1 - 3 * r / 4 + r ** 2 / 8 - r ** 3 / 192) * np.exp(-r/4)

    def R_4p(self, r):
        return (np.sqrt(5) / (16 * np.sqrt(3))) * r * (1 -  r / 4 + r ** 2 / 80) * np.exp(-r/4)

    def R_4d(self, r):
        return (1 / (64 * np.sqrt(5))) * (r ** 2) * (1 -  r / 12) * np.exp(-r/4)

    def R_4f(self, r):
        return (1 / (768 * np.sqrt(35))) * (r ** 3) * np.exp(-r/4)


    def Y_0_0(self, theta, phi):
        return 1 / np.sqrt(4 * np.pi)

    def Y_1_0(self, theta, phi):
        return np.sqrt(3 / (4*np.pi)) * np.cos(theta)

    def Y_1_1(self, theta, phi, pm):
        return - pm * np.sqrt(3 / (8*np.pi)) * np.sin(theta) * np.exp(pm * 1j * phi)

    def Yc_100(self, theta, phi):
        return (-self.Y_1_1(theta, phi, 1) + self.Y_1_1(theta, phi, -1))  / np.sqrt(2)

    def Yc_010(self, theta, phi):
        return 1j * (self.Y_1_1(theta, phi, 1) + self.Y_1_1(theta, phi, -1))  / np.sqrt(2)


    def Y_2_0(self, theta, phi):
        return np.sqrt(5 / (16*np.pi)) * (3 * np.cos(theta) ** 2 - 1)

    def Y_2_1(self, theta, phi, pm):
        return - pm * np.sqrt(15 / (8*np.pi)) * (np.sin(theta) * np.cos(theta)) * np.exp(pm * 1j * phi)

    def Y_2_2(self, theta, phi, pm):
        return - pm * np.sqrt(15 / (32*np.pi)) * (np.sin(theta) ** 2) * np.exp(pm * 2j * phi)

    def Y_3_0(self, theta, phi):
        return np.sqrt(7 / (16 * np.pi)) * (5 * np.cos(theta) ** 3 - 3 * np.cos(theta))

    def Y_3_1(self, theta, phi, pm):
        return - pm * np.sqrt(21 / (64 * np.pi)) * (5 * np.cos(theta) ** 2 - 1) * np.sin(theta) * np.exp(pm * 1j * phi)

    def Y_3_2(self, theta, phi, pm):
        return np.sqrt(105 / (32 * np.pi)) * (np.cos(theta) * np.sin(theta) ** 2) * np.exp(pm * 2j * phi)

    def Y_3_3(self, theta, phi, pm):
        return - pm * np.sqrt(35 / (64 * np.pi)) * (np.sin(theta) ** 3) * np.exp(pm * 3j * phi)

    def create_widgets(self):
        my_font = font.Font(root,family="System",size=16,weight="bold")

        self.parent_panel = ttk.Frame(root, padding=5)
        self.parent_panel.pack(anchor=tk.NW, side=tk.LEFT)

        label = tk.Label(self.parent_panel)
        label["text"] = "×"
        label.grid(row=0, column=1)
        label.configure(font=my_font)

        label = tk.Label(self.parent_panel)
        label["text"] = "球面調和関数"
        label.grid(row=0, column=2)
        label.configure(font=my_font)
        cnt = 1

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "s軌道(l0,m0)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs( self.Y_0_0(theta, phi) )))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1             
        cnt = cnt + 1


        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "p軌道(l1,m0)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi : np.abs(np.real(self.Y_1_0(theta, phi)))))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        cnt = cnt + 1

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "p軌道(l1,m1)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs(np.real(self.Y_1_1(theta, phi, 1) ))))
        tk_btn.configure(font=my_font)    
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        cnt = cnt + 1

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "調和振動子-x合成"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs( np.real( self.Yc_100(theta, phi)))))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        cnt = cnt + 1

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "調和振動子-y合成"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs( np.real( 1j * (self.Y_1_1(theta, phi, 1) + self.Y_1_1(theta, phi, -1)) / np.sqrt(2) ))))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)    
        cnt = cnt + 1

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "調和振動子-z合成"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs( np.real( self.Y_1_0(theta, phi)))))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)  
        cnt = cnt + 1
        cnt += 3

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "d軌道(l2,m0)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs( np.real( self.Y_2_0(theta, phi)))))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        cnt = cnt + 1

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "d軌道(l2,m1)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs( np.real( self.Y_2_1(theta, phi, 1)))))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        cnt = cnt + 1

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "d軌道(l2,m2)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs( np.real( self.Y_2_2(theta, phi, 1)))))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        cnt = cnt + 1
        cnt += 6

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "f軌道(l3,m0)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs( np.real(self.Y_3_0(theta, phi)) )))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1             

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "f軌道(l3,m1)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs( np.real(self.Y_3_1(theta, phi, 1) ))))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1             

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "f軌道(l3,m2)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs( np.real(self.Y_3_2(theta, phi, 1) ))))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1             


        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "f軌道(l3,m3)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d', 
            lambda theta, phi: np.abs( np.real(self.Y_3_3(theta, phi, 1) ))))
        tk_btn.grid(row=cnt, column=2, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1             



        label = tk.Label(self.parent_panel)
        label["text"] = "="
        label.grid(row=0, column=3)
        label.configure(font=my_font)

        label = tk.Label(self.parent_panel)
        label["text"] = "電子分布\nφnlm"
        label.grid(row=0, column=4)
        label.configure(font=my_font)
        cnt = 1

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ100"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: ( self.R_1s(r) * self.Y_0_0(theta, phi) )],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ200"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: ( self.R_2s(r) * self.Y_0_0(theta, phi) )]))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ210"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_2p(r) * self.Y_1_0(theta, phi)]))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ211"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_2p(r) * self.Y_1_1(theta, phi, 1)]))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φx"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_2p(r) * self.Yc_100(theta, phi)]))      
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φy"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_2p(r) * self.Yc_010(theta, phi)],
            lambda axes, fig: axes.view_init(elev=0,azim=0)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   


        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φz"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_2p(r) * self.Y_1_0(theta, phi)]))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1  

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ300"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi:  self.R_3s(r) * self.Y_0_0(theta, phi) ],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ310"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_3p(r) * self.Y_1_0(theta, phi) ],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   


        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ311"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_3p(r) * self.Y_1_1(theta, phi, 1) ],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ320"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_3d(r) * self.Y_2_0(theta, phi)],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   


        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ321"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_3d(r) * self.Y_2_1(theta, phi, 1) ],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1 

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ322"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_3d(r) * self.Y_2_2(theta, phi, 1)],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1 


        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ400"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi:  self.R_4s(r) * self.Y_0_0(theta, phi)],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ410"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_4p(r) * self.Y_1_0(theta, phi)],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   


        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ411"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_4p(r) * self.Y_1_1(theta, phi, 1)],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ420"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_4d(r)* self.Y_2_0(theta, phi) ],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ421"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_4d(r)* self.Y_2_1(theta, phi, 1) ],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ422"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_4d(r)* self.Y_2_2(theta, phi, 1) ],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1   



        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ430"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_4f(r) * self.Y_3_0(theta, phi)  ],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1  

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ431"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_4f(r) * self.Y_3_1(theta, phi, 1) ],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1  

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ432"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_4f(r) * self.Y_3_2(theta, phi, 1) ],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1  

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "φ433"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('3d_field', 
            [lambda r, theta, phi: self.R_4f(r) * self.Y_3_3(theta, phi, 1)  ],
            lambda axes, fig: axes.view_init(elev=0,azim=90)))
        tk_btn.grid(row=cnt, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)        
        cnt = cnt + 1  


        label = tk.Label(self.parent_panel)
        label["text"] = "動径関数"
        label.grid(row=0, column=0)

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "1s(n1,l0)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('2d', 
            lambda r : ((r * self.R_1s(r)) ** 2)))
        tk_btn.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "2s(n2,l0)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('2d', 
            lambda r: np.abs((r * self.R_2s(r)) ** 2)) )
        tk_btn.grid(row=2, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        tk_btn = MarkerButton(self.parent_panel)

        tk_btn["text"] = "2p(n2,l0)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('2d', 
            lambda r: np.abs((r * self.R_2p(r)) ** 2)) )
        tk_btn.grid(row=3, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "3s(n3,l0)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('2d', 
            lambda r: np.abs((r * self.R_3s(r)) ** 2)) )
        tk_btn.grid(row=8, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        tk_btn = MarkerButton(self.parent_panel)

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "3p(n3,l1)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('2d', 
            lambda r: np.abs((r * self.R_3p(r)) ** 2)) )
        tk_btn.grid(row=9, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        tk_btn = MarkerButton(self.parent_panel)


        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "3d(n3, l2)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('2d', 
            lambda r: np.abs((r * self.R_3d(r)) ** 2)) )
        tk_btn.grid(row=10, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        tk_btn = MarkerButton(self.parent_panel)

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "4s(n4, l0)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('2d', 
            lambda r: np.abs((r * self.R_4s(r)) ** 2)) )
        tk_btn.grid(row=14, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        tk_btn = MarkerButton(self.parent_panel)

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "4p(n4, l1)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('2d', 
            lambda r: np.abs((r * self.R_4p(r)) ** 2)) )
        tk_btn.grid(row=15, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        tk_btn = MarkerButton(self.parent_panel)

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "4d(n4, l2)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('2d', 
            lambda r: np.abs((r * self.R_4d(r)) ** 2)) )
        tk_btn.grid(row=16, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        tk_btn = MarkerButton(self.parent_panel)

        tk_btn = MarkerButton(self.parent_panel)
        tk_btn["text"] = "4f(n4, l3)"
        tk_btn["command"] = partial(self.press_for_graph, tk_btn, GraphView('2d', 
            lambda r: np.abs((r * self.R_4f(r)) ** 2)) )
        tk_btn.grid(row=17, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        tk_btn.configure(font=my_font)     
        tk_btn = MarkerButton(self.parent_panel)





    def select(self, sender):
        if self._before_action_button != None:
            self._before_action_button.turn_off()
        sender.turn_on()

        self._before_action_button = sender

    def press_for_graph(self, sender, graph_func, graph_object=None):
        self.select(sender)

        #graph_obj = GraphView('3d', lambda : "")

        if self._graph_object == None:
            self._graph_object = SphericalSurface(self.master)

        self._graph_object.plot(graph_func, graph_object)
        

root = tk.Tk()
root.title("Spherical Surface Demonstration")
root.attributes('-fullscreen', True)
app = Application(master=root)
app.mainloop()
