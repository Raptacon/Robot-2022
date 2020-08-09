import yaml
import logging as log
from pprint import pprint
import os
from pathlib import Path

class ConfigMapper(object):
    def __init__(self, filename, configDir):
        """
        Initlizes the config off a tree of yamls.
        "/" holds global config
        "<subsystem>" holds configs for subsystems
        configDir points to folder with configs. Future work make it take a list and search.
        """
        self.configDir = configDir
        initialData = self.__loadFile(filename)
        log.debug("Intial data %s", initialData)
        self.subsystems = self.__convertToSubsystems(initialData, "/")
        root = self.subsystems["/"]
        if not "compatibility" in root:
            log.warning("No Compatibility string found. Matching all")
            self.subsystems["compatibility"] = ["any"]
        if not isinstance(root["compatibility"], list):
            root["compatibility"] = [root["compatibility"]]
        
        root["compatibility"] =  [x.lower() for x in root["compatibility"]]


    def getSubsystem(self, subsystem):
        """
        returns the complete config for specified subsystem or none if not found
        """
        #gives the values.

        if subsystem in self.subsystems:
            return self.subsystems[subsystem]
        return None

    def checkCompatibilty(self, compatString):
        """
        Checks if a string is marked as compatible in the config
        """
        compatString = [x.lower() for x in compatString]

        root = self.getSubsystem("/")
        if root == "all" or "all" in compatString:
            return True
        for string in root["compatibility"]:
            if string in compatString:
                return True
        return False

    def getSubsystems(self):
        subsystems = list(self.subsystems.keys())
        subsystems.remove("/")
        return subsystems

    def getGroupDict(self, subsystem, groupName, name = None):
        """
        returns a dictonary with data from a subsystem matching the groups and
        if given then name.
        i.e.
        if you have a lifter with
        lifter.sensors.groups=sensor
        lifter.intakeMotors.groups=motors
        lifter.beltMotors.groups=motors
        calling getTypeDict("lifter", "motors")
        returns all motors in intakeMotors and beltMotors

        calling getTypeDict("lifter", "motors", "beltMotors")
        returns all motors in beltMotors

        calling getTypeDict("lifter", "sensor")
        returns all sensors
        """
        data = self.getSubsystem(subsystem)
        data =  self.__getGroups(data, groupName, name)
        if "groups" in data:
            data.pop("groups")

        return data

    def getTypesDict(self, subsystem, typeNames, name = None):
        """
        returns a dictonary with data from a subsystem matching the type(s) and
        Once a type is found in an entry it is not searched any deeper
        """
        if not isinstance(typeNames, list):
            typeNames = [typeNames]
        data = self.getSubsystem(subsystem)
        data = self.__getTypes(data, typeNames, name)
        
        return data

    def __getGroups(self, data, groupName, name):
        """
        internal call, recusivley search the data for entries with
        groups in "types" and if a name is given only types inside key with name
        """

        retVal = {}
        for key in data:
            if isinstance(data[key], dict):
                recusiveDict = self.__getGroups(data[key], groupName, name)
                retVal.update(recusiveDict)

            if isinstance(data[key], dict) and "groups" in data[key]:
                if name and not key == name:
                    continue

                if groupName in data[key]["groups"]:
                    retVal.update(data[key])
        return retVal

    def __getTypes(self, data, typeNames, name):
        """
        internal call, recusivley search the data for entries with
        typeName in ["types"] and if a name is given only types inside key with name
        """
        retVal = {}
        for key in data:
            if isinstance(data[key], dict):
                recusiveDict = self.__getTypes(data[key], typeNames, name)
                retVal.update(recusiveDict)

            if isinstance(data[key], dict) and "type" in data[key]:
                if name and not key == name:
                    continue

                if data[key]["type"] in typeNames:
                    retVal[key] = data[key]
        return retVal


    def __loadFile(self, filename):
        """
        Loads a yaml or yml file and returns the contents as dictionary
        """
        with open(self.configDir + os.path.sep + filename) as file:
            values = yaml.load(file, yaml.FullLoader)
            return values


    def __convertToSubsystems(self, inputData, defSubsystem):
        """
        Takes a dictionary and searchs for subsystem types to create leafs of a new tree.
        Loads files as "file" is encountered
        """
        if "subsystem" in inputData:
            subsystem = inputData["subsystem"]
        else:
            subsystem = defSubsystem

        processedData = {}
        processedData[subsystem] = {}

        for key in inputData:

            #if file, load file and walk
            if isinstance(inputData[key], dict) and "file" in inputData[key]:
                fileName = inputData[key].pop("file")
                fileType = inputData[key].pop("type")
                if not fileType == "yaml":
                    log.error("Unknonw file type fileType. Trying Yaml")
                log.info("Loading %s into entry %s", fileName, key)
                data = self.__loadFile(fileName)
                #Flatten the root node of newly loaded yaml file.
                for loadedKey in data:
                    if isinstance(data[loadedKey], dict):
                        inputData[key].update(data[loadedKey])
                    else:
                        inputData[key][loadedKey] = data[loadedKey]

            #if subsystem, walk subsystem
            if "subsystem" in inputData[key] and isinstance(inputData[key], dict):
                log.info("Walking subsystem")
                #make a new subsystem
                print("Crashing????")
                print(inputData[key])
                print(inputData[key]["subsystem"])
                processedData[inputData[key]["subsystem"]] = self.__convertToSubsystems(inputData[key], inputData[key]["subsystem"])

            #copy field over if no special processing
            processedData[subsystem][key] = inputData[key]
        
        return processedData



def findConfig(configName):
    """
    Will determine the correct yml file for the robot.
    Please run 'echo (robotCfg.yml) > robotConfig' on the robot.
    This will tell the robot to use robotCfg file remove the () and use file name file.
    Files should be configs dir
    """
    configPath = os.path.dirname(__file__) + os.path.sep + ".." +os.path.sep + "configs" + os.path.sep
    home = str(Path.home()) + os.path.sep
    defaultConfig = configName
    robotConfigFile = home + configName

    if not os.path.isfile(robotConfigFile):
        log.error("Could not find %s. Using default", robotConfigFile)
        robotConfigFile = configPath + "default"
    try:
        file = open(robotConfigFile)
        configFileName = file.readline().strip()
        file.close()
        configFile = configPath + configFileName
        
        if os.path.isfile(configFile):
            log.info("Using %s config file", configFile)
            return configFileName, configPath
        log.error("No config? Can't find %s", configFile)
        log.error("Using default %s", defaultConfig)
    except Exception as e:
        log.error("Could not find %s", robotConfigFile)
        log.error(e)
        log.error("Please run `echo <robotcfg.yml> > ~/robotConcig` on the robot")
        log.error("Using default %s", defaultConfig)

    return defaultConfig, configPath


if __name__ == "__main__":
    mapper = ConfigMapper("doof.yml", "configs")
    print("Subsystem driveTrain:", mapper.getSubsystem("driveTrain"))
    
    print("driveTrain Motors")
    pprint(mapper.getGroupDict("driveTrain", "motors"))
    
    print("Shooter motors:")
    pprint(mapper.getGroupDict("shooter", "motors", "loaderMotors"))

    print("All motors:")
    mapper.getGroupDict("/", "motors")
    #print()
    pprint(mapper.getGroupDict("/", "motors"))

    print("CANTalonFXFollower motors:")
    data = mapper.getTypesDict("/", "CANTalonFXFollower")
    #print()
    pprint(data)

    compatTest = ["Dog", "all", "doof", "minibot", "DOOF"]
    for item in compatTest:
        compat = mapper.checkCompatibilty(item)
        print(f"{item} is {compat}")

    print("Subsystems: ", mapper.getSubsystems())
