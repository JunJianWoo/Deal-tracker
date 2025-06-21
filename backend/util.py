import os

def createConfigSet(fileName, prefix=""):
    configSet = set()
    fileLocation = os.path.join( os.getcwd(), os.environ['SCRAPER_CONFIG_LOCATION'], fileName)
    for item in open(fileLocation, 'r'):
        configSet.add(prefix + item.strip().lower())

    return configSet

def singleton(cls):
    """ Replaces class instantiation to a single instance decorator"""
    single_instance = None
    
    def get_instance(*args, **kwargs):
        nonlocal single_instance
        if single_instance is None:
            single_instance = cls(*args, **kwargs)
        return single_instance
    
    return get_instance