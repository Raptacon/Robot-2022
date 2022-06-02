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

        Y = max(Axes[3], Axes[1])
        R = (0.5*Axes[3]) - (0.5*Axes[1])



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
