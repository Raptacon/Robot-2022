
class ConfigMapper(object):
    def __init__(self, filename):
        self.config = open(filename, "r")
    def readValues(self):
        #Makes a dictionary based off of values in the config.yml file. Name and value must be separated by ': ' in the file. Otherwise this will not work.
        values = {}
        lines = self.config.readlines()
        for line in lines:
            if ':' in line:
                values[str(line[:line.index(': ')])] = line[line.index(': ')+2:-1]
                print("CONFIG VALUE: "+str(line[line.index(': ')+2:-1]))
        return values