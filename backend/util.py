import os

def createConfigSet(fileName, prefix=""):
    configSet = set()
    fileLocation = os.path.join( os.getcwd(), os.environ['SCRAPER_CONFIG_LOCATION'], fileName)
    for item in open(fileLocation, 'r'):
        configSet.add(prefix + item.strip().lower())

    return configSet