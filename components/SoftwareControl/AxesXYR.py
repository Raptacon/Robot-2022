from re import X
from tkinter import Y
from utils.XYRVector import XYRVector
from robotMap import XboxMap

class transform:
    def transform(self, Axes):
        return XYRVector(0, 0, 0)
class transformTank(transform):
    def transform(self, Axes, tank):
        Axes[0] # Axis 1
        Axes[1] # Axis 2
        Axes[2] # Axis 3
        Axes[3] # Axis 4

        l = Axes[1]
        r = Axes[2]

        # I'm so sorry
        # https://www.desmos.com/calculator/aedmycj0py

        # When r<0 and y<0:
        # R= .5*((l**2+4*r+4)**.5 - l)-1
        # Y= .5*((l**2+4*r+4)**.5 + l)-1

        # When r>0 and y<0:
        # R= r/2 + 1 - .5*(r**2+4*l+4)**.5
        # Y=
        if


        Y = max(Axes[3], Axes[1])
        R = (Axes[3]-Axes[1])/(2-abs(Y))



        return XYRVector(0, Y, R)

class transformArcade(transform):
    def transform(self, Axes, arcade):
        Axes[0] # Axis 1
        Axes[3] # Axis 4

        Y = (Axes[3])
        R = (Axes[0])

        return XYRVector(0, Y, R)






class transformSwerve(transform):
    def transform(self, Axes, swerve):
        Axes[0] # Axis 1
        Axes[2] # Axis 3
        Axes[3] # Axia 4

        Y = (Axes[3])
        R = (Axes[0])
        X = (Axes[2])

        return XYRVector(X, Y, R)


class AxesXYR:
    transformDict = {"tank":transformTank, "arcade":transformArcade, "swerve":transformSwerve}

    def transform(self, transformKey:str, Axes:list):

        if transformKey in self.transformDict.keys():
            transformer = self.transformDict[transformKey]
            return transformer.transform(Axes)
