from re import X
from tkinter import Y
from utils.XYRVector import XYRVector
from robotMap import XboxMap

class transform:
    def transform(self, Axes):
        return XYRVector(0, 0, 0)
class transformTank(transform):
    def transform(self, Axes):
        Axes[0] # Axis 1
        Axes[1] # Axis 2
        Axes[2] # Axis 3
        Axes[3] # Axis 4

        l = Axes[1]
        r = Axes[2]

        # I'm so sorry
        # https://www.desmos.com/calculator/dw1hoo9lnp

        # When r<0 and y<0:
        R1= .5*(((l**2)+4*r+4)**.5 - l)-1
        Y1= .5*(((l**2)+4*r+4)**.5 + l)-1

        # When r<0 and y>0:
        R2= .5*(r+((r**2)-4*l+4)**.5)-1
        Y2= .5*(r-((r**2)-4*l+4)**.5)+1

        # When r>0 and y<0:
        R3= .5(r-((r**2)+4*l+4)**.5)+1
        Y3= .5(r+((r**2)+4*l+4)**.5)-1

        # When r>0 and y>0:
        R4= 1-.5*(l+((l**2)-4*r+4))
        Y4= 1+.5*(l-((l**2)-4*r+4))

        # You can verify this logic with the graph
        # https://www.desmos.com/calculator/b9ig0ymtvq
        if Y2>0 or Y4>0:
            Y = max(Y2, Y4)
        else:
            Y = min(Y1, Y3)

        # https://www.desmos.com/calculator/uoddoiynu6
        if R3>0 or R4>0:
            R = max(R3, R4)
        else:
            R = min(R1, R2)

        return XYRVector(0, Y, R)

class transformArcade(transform):
    def transform(self, Axes):
        Axes[0] # Axis 1
        Axes[3] # Axis 4

        Y = (Axes[3])
        R = (Axes[0])

        return XYRVector(0, Y, R)






class transformSwerve(transform):
    def transform(self, Axes):
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
