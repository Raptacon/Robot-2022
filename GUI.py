from struct import pack
from telnetlib import X3PAD
from tkinter import CENTER, E, NW, Canvas,Tk
import tkinter as tk
from turtle import bgcolor, width
from networktables import NetworkTables as networktable
import math
limeTable = networktable.getTable("limelight")

def on_open():
    calc_circle()
    calc_triagle()
    window.after(1, next)

def next():
    print(window.winfo_geometry())
    window.after(1, on_open)

window = Tk()
window.title("mini Map")
window.geometry("400x300+0+0")

print(window.winfo_geometry())

myCanvas = Canvas(window, bg = "white")
myCanvas.config(highlightthickness= 5, highlightbackground= "red")
myCanvas.pack(fill = tk.BOTH, expand = True)
def create_circle(x, y, r, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill='blue')
def calc_circle():
    x = 0
    y = 0
    numball = 5
    ball = 0
    while(ball <= numball):
        ball += 1
        x += 20
        y += 20
        create_circle(x, y, 20, myCanvas)
def calc_triagle():
    FOV = 81.3
    x1 = window.winfo_width()
    y1 = window.winfo_height()/2
    x2 = (math.tan((180 - FOV)/2) * y1)
    y2 = 0
    x3 = x2
    y3 = window.winfo_height()
    print(x1,y3)


    return myCanvas.create_polygon(x1,y1, x2,y2, x3,y3)

myCanvas.pack()
window.after(1,next)
window.after(1,on_open)
window.mainloop()
