import yaml
class ConfigMapper(object):
    def __init__(self, filename):
        with open(filename) as file:
            self.values = yaml.load(file, yaml.FullLoader)
            print(yaml.dump(self.values))
    def getDicts(self):
        #gives the values.
        return self.values['driveMotors']
