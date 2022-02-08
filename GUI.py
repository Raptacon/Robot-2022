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
        self.label = tk.Canvas(self)
        self.label.pack(fill = 'both',expand= True)
        position = [[5,0.5],[10,1],[15,-11],[54,0]]
        numball = len(position)
        HightOffSet = 2
        ball = 0
        self.calc_tri(self.label)
        #self.label.tkraise()
        print(position[ball][0])
        while(ball < numball):
            if position[ball][0] <= 10:
                hyp = math.sqrt(position[ball][0] ** 2 - HightOffSet ** 2)
                xft = hyp * math.cos(position[ball][1])
                yft = hyp * math.sin(position[ball][1])
                x = 400 - (xft * 40)
                y = 150 + (yft * 15)
                self.create_circle(x, y, 5, self.label)
            else:
                x = 0
                yft = hyp * math.sin(position[ball][1])
                y = 150 + (yft * 15)
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
        x1 = 400
        y1 = 300/2
        x2 = (math.tan((180 - FOV)/2) * y1)
        y2 = 0
        x3 = x2
        y3 = 300
        canvasNametri.create_polygon(x1,y1, x2,y2, x3,y3)

Window = window()
Window.geometry('400x300+0+0')
Window.resizable(0,0)
Window.mainloop()
