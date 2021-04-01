class DistanceDriver(StateMachine):

    def driveDistance(lidar.getDist):
        if lidar.getDist == 0:
            print("Distance is invaled")
        else:
            potisioni = lidar.getDist
            distanceToTravel = potisioni - distanceSet
            return distanceToTravel


    def setDistance():
        distanceSet = 30
        return distanceSet


    def TravelDistance(n):
        if (n == lidar.getDist):
            print("You have reched destnation")
