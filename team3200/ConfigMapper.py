
class ConfigMapper(object):
    def __init__(self, filename):
        self.config = open(filename, "r")
        self.values = self.readValues()
    def readValues(self):
        #Makes a dictionary based off of values in the config.yml file. Name and value must be separated by ': ' in the file. Otherwise this will not work.
        values = {}
        lines = self.config.readlines()
        for line in lines:
            if ':' in line:
                values[str(line[:line.index(': ')])] = line[line.index(': ')+2:-1]
                print("CONFIG VALUE: "+str(line[line.index(': ')+2:-1]))
        return values
    def makeDict(self, base, motors):
        #base: a string as a base for creating motors.
        #motors: a dictionary of motors to add this dictionary to. Should not contain motors, this is to populate this dictionary.
        bases = {}
        for name, value in self.values.items():
            if base in value:
                bases[name[name.index(base):]] = value
            else:
                print("Base not in value. Please change.")
        return motors