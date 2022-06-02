from re import X
from tkinter import Y
from utils.XYRVector import XYRVector
from robotMap import XboxMap

class transform:
    pass
class transformTank(transform):
    pass

class transformArcade(transform):
    pass

class transformSwerve(transform):
    pass
class AxesXYR:
<<<<<<< Updated upstream

X = 0
Y = 0
R = 0
vectorXYR = [X],[Y],[R]

def Trasformations(imp1,imp2,imp3,imp4,self):
=======
    transformDict = {"tank":transformTank, "arcade":transformArcade, "swerve":transformSwerve}

    def transform(self, transformKey:str, Axes: list):

        if transformKey in self.transformDict.keys():
            transformer = self.transformDict[transformKey]
            return transformer.transform(Axes)
>>>>>>> Stashed changes
