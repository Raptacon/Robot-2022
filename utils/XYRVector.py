
from cmath import sqrt


class XYRVector:
    """
    3 values ranging from -1 to 1
    X: Translation to the left and right (right being positive)
    Y: Translation forwards and backwards (forward being positive)
    R: Rotation along the horizontal (counterclockwise is positive)
    """

    def __init__(self, X, Y, R):
        self.X = X
        self.Y = Y
        self.R = R

    def getMagnitudeTranslation(self):
        magnitude = sqrt(self.X **2 , self.Y **2)
        return magnitude

    def setX(self, X):
        self.X = X

    def setY(self, Y):
        self.Y = Y

    def setR(self, R):
        self.R = R

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def getR(self):
        return self.R
