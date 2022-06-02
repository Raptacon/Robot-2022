from utils.XYRVector import XYRVector
from robotMap import XboxMap

class transform:
    def transform(self, Axes):
        return XYRVector(0, 0, 0)
class transformTank(transform):
    def transform(self, Axes):
        X = Axes[0]
        Y = Axes[1]

        return XYRVector(X, Y, 0)

class transformArcade(transform):
    pass

class transformSwerve(transform):
    pass
class AxesXYR:
    transformDict = {"tank":transformTank, "arcade":transformArcade, "swerve":transformSwerve}

    def transform(self, transformKey:str, Axes:list):

        if transformKey in self.transformDict.keys():
            transformer = self.transformDict[transformKey]
            return transformer.transform(Axes)
