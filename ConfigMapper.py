import yaml
class ConfigMapper(object):
    def __init__(self, filename):
        with open(filename) as file:
            self.values = yaml.load(file, yaml.FullLoader)
    def getDicts(self):
        #gives the values.
        return self.values['motors']
