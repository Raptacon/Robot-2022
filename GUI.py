from cgitb import enable
from struct import pack
from telnetlib import X3PAD
from tkinter import CENTER, E, NW, Canvas,Tk
import tkinter as tk
from turtle import bgcolor, width
from networktables import NetworkTables as networktable
import math
limeTable = networktable.getTable("limelight")

class window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        myCanvas = tk.Frame(self, background= 'white')
        myCanvas.config(highlightthickness= 5, highlightbackground= "red")
        myCanvas.pack(fill = "both", expand = True)
        
        myCanvas.grid_rowconfigure(0, weight=1)
        myCanvas.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = Calc_circle(myCanvas, self)

        self.frames[Calc_circle] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Calc_circle)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
class Calc_circle(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Canvas(self)
        label.pack(pady=10,padx=10)
        print(controller)
        x = 0
        y = 0
        numball = 5
        ball = 0
        while(ball <= numball):
            ball += 1
            x += 20
            y += 20
            self.create_circle(x, y, 20, label)
    def create_circle(self,x, y, r, canvasName): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        canvasName.create_oval(x0, y0, x1, y1, fill='blue')
class calc_triagle(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        tri = tk.Canvas(self)
        tri.pack(pady=10,padx=10)
        FOV = 81.3
        x1 = window.winfo_width()
        y1 = window.winfo_height()/2
        x2 = (math.tan((180 - FOV)/2) * y1)
        y2 = 0
        x3 = x2
        y3 = window.winfo_height()
        tri.create_polygon(x1,y1, x2,y2, x3,y3)

Window = window()

Window.mainloop()
