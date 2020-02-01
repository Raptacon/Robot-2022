
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
        return values
    
    def makeDict(self, base, motors):
        #base: a string as a base for creating motors.
        #motors: a dictionary of motors to add this dictionary to. Should not contain motors, this is to populate this dictionary.
        bases = {}
        for name, value in self.values.items():
            if base in name:
                try:
                    bases[name[name.index(base)+len(base):]] = int(value)
                except:
                    bases[name[name.index(base)+len(base):]] = value
                if value == "None":
                    bases[name[name.index(base)+len(base):]] = None
                if value == "True":
                    bases[name[name.index(base)+len(base):]] = True
                if value == "False":
                    bases[name[name.index(base)+len(base):]] = False

        motors[base] = bases
        print("MOTORS: {}".format(motors))
        return motors