from cgitb import enable
from time import sleep
from struct import pack
from telnetlib import X3PAD
from tkinter import CENTER, E, NW, Canvas,Tk
import tkinter as tk
from turtle import pos
from networktables import NetworkTables as networktable
import math
class window(tk.Tk):
    CamTable = networktable.getTable("ML")
    NumBall = CamTable.getString("ML/detections").len()
    width = round((math.tan(math.radians((180 - 81.3)/2)) * 200))
    maxFT = 10
    position = [[3,40.65],[11,40.65],[13,-40.65],[9,40.65]]
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
        self.calc_tri(self.label)
        self.calc_cir(self.label)
    def calc_cir(self,canvas):
        
        numball = window.NumBall
        HightOffSet = 2
        ball = 0
        max = window.maxFT
        maxAngle = math.radians(40.65)
        #self.label.tkraise()
        while(ball < numball):
            num = window.position[ball][0]
            angle = math.radians(window.position[ball][1])
            hyp = math.sqrt(window.position[ball][0] ** 2 - HightOffSet ** 2) 
            xft = max / math.cos(angle)
            dist = min(hyp, xft)
            yft = dist * math.sin(angle)
            x = window.width - (dist * (window.width/max))*math.cos(angle)
            y = 200 + (yft*(400/(2*max*math.tan(maxAngle))))
            if window.CamTable.getString("label") == 'blue':
                self.create_circle_blue(x, y, 5, canvas)
            else:
                self.create_circle_red(x, y, 5, canvas)
            print(window.position[ball][0])
            window.position[ball][0] = 1 + window.position[ball][0]
            ball += 1
    def create_circle_blue(self,x, y, r, canvasName): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        canvasName.create_oval(x0, y0, x1, y1, fill='blue',tags = 'circle')
    def create_circle_red(self,x, y, r, canvasName): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        canvasName.create_oval(x0, y0, x1, y1, fill='blue',tags = 'circle')
    def calc_tri(self,canvasNametri):
        FOV = 81.3
        x1 = window.width
        y1 = 400/2
        x2 = 0
        y2 = 0
        x3 = x2
        y3 = 400
        canvasNametri.create_polygon(x1,y1, x2,y2, x3,y3, tags = 'rect')
def delete():
    Window.frames[Calc_circle].label.delete('circle')
    Window.frames[Calc_circle].calc_cir(Window.frames[Calc_circle].label)
    Window.after(1000, delete)
Window = window()
Window.geometry(str(Window.width)+'x400+0+0')
Window.resizable(0,0)
#while True:
    #Window.after(1000,delete)
delete()
Window.mainloop()
