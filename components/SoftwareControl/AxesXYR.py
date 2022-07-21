from utils.XYRVector import XYRVector
from utils.AxesEnums import AxesTransforms

class transform:
    def transform(self, Axes):
        return XYRVector(0, 0, 0)

class transformTank(transform):
    def transform(self, Axes):
        # Axes[1] # Axis 2
        # Axes[3] # Axis 4

        l = Axes[1]
        r = Axes[3]

        # I'm so sorry
        # https://www.desmos.com/calculator/dw1hoo9lnp

        # Input/Output graph:
        # https://www.desmos.com/calculator/eu9sruirci

        # When r<0 and y<0:
        R1= .5*(((l**2)+4*r+4)**.5 - l)-1
        Y1= .5*(((l**2)+4*r+4)**.5 + l)-1

        # When r<0 and y>0:
        R2= .5*(r+((r**2)-4*l+4)**.5)-1
        Y2= .5*(r-((r**2)-4*l+4)**.5)+1

        # When r>0 and y<0:
        R3= .5*(r-((r**2)+4*l+4)**.5)+1
        Y3= .5*(r+((r**2)+4*l+4)**.5)-1

        # When r>0 and y>0:
        R4= 1-.5*(l+((l**2)-4*r+4)**.5)
        Y4= 1+.5*(l-((l**2)-4*r+4)**.5)

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
        Axes[1] # Axis 2
        Axes[2] # Axis 3

        Y = (Axes[1])
        R = (Axes[2])

        return XYRVector(0, Y, R)

class transformSwerve(transform):
    def transform(self, Axes):
        Axes[0] # Axis 1
        Axes[1] # Axis 2
        Axes[2] # Axis 3

        Y = (Axes[1])
        R = (Axes[2])
        X = (Axes[0])

        return XYRVector(X, Y, R)

class AxesXYR:
    transTank = transformTank()
    transArcade = transformArcade()
    transSwerve = transformSwerve()


    def __init__(self):
        self.transformDict = {AxesTransforms.kTank: self.transTank,
                        AxesTransforms.kArcade: self.transArcade,
                        AxesTransforms.kSwerve: self.transSwerve}

    def transform(self, transformKey:AxesTransforms, Axes:list):

        if transformKey in self.transformDict.keys():
            transformer = self.transformDict[transformKey]
            return transformer.transform(Axes)
        else:
            return XYRVector(0, 0, 0)

    def execute(self):
        pass
