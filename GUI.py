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
    width  = round((math.tan(math.radians((180 - 81.3)/2)) * 200))
    def __init__(self):
        tk.Tk.__init__(self)
        myCanvas = tk.Frame(self, background= 'white')
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
        self.label = tk.Canvas(self)
        self.label.pack(fill = 'both',expand= True)
        position = [[5,40.65],[10,40.65],[15,0],[54,40.65]]
        numball = len(position)
        HightOffSet = 2
        ball = 0
        winx = self.calc_tri(self.label)
        #self.label.tkraise()
        while(ball < numball):
            if position[ball][0] <= 10:
                hyp = math.sqrt(position[ball][0] ** 2 - HightOffSet ** 2)
                xft = hyp * math.cos(math.radians(position[ball][1]))
                yft = hyp * math.sin(math.radians(position[ball][1]))
                x = window.width - (xft * (window.width/10))
                y = 200 + (yft * 20)
                print(y,yft)
                self.create_circle(x, y, 5, self.label)
            else:
                hyp = math.sqrt(position[ball][0] ** 2 - HightOffSet ** 2)
                x = 0
                yft = hyp * math.sin(math.radians(position[ball][1]))
                y = 200 + (yft * 20)
                print(y,yft)
                self.create_circle(x, y, 5, self.label)
            ball += 1
    def create_circle(self,x, y, r, canvasName): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        canvasName.create_oval(x0, y0, x1, y1, fill='blue')
    def calc_tri(self,canvasNametri):
        FOV = 81.3
        x1 = window.width
        y1 = 400/2
        x2 = 0
        y2 = 0
        x3 = x2
        y3 = 400
        canvasNametri.create_polygon(x1,y1, x2,y2, x3,y3)
        return x2

Window = window()
Window.geometry(str(Window.width)+'x400+0+0')
Window.resizable(0,0)
Window.mainloop()
