import os

# Can be extended in the future to allow for
# other repository locations
use_desc = open("/usr/portage/profiles/use.desc","r")
use_local_desc = open("/usr/portage/profiles/use.local.desc","r")

# Dictionaries for global USE flags and local USE flags
globalUseDict = {}
localUseDict = {}
make_conf_use = []

for line in use_desc:
    # Potential improvement: Use regex instead?
    # Checks if line is not commented and non-empty
    if line[0:1] != "#" and line != '\n':
        useIndex = line.find(' - ', 0)
        globalUseDict[line[0:useIndex]] = line[useIndex+3:-1]

for line in use_local_desc:
    # Checks if line is not commented and non-empty
    if line[0:1] != "#" and line != '\n': 
        initUseIndex = line.find(':', 0)
        endUseIndex = line.find(' - ', 0)
        initDescIndex = endUseIndex + 3

        packageName = line[0:initUseIndex]
        useFlag = line[initUseIndex+1:endUseIndex]
        useFlagDesc = line[initDescIndex:-1]
 
        if useFlag not in localUseDict:
            localUseDict[useFlag] = dict(packageName=useFlagDesc)
        else:
            localUseDict[useFlag][packageName] = useFlagDesc
            
def getGlobalUse(useflag):
    if useflag in globalUseDict:
        return globalUseDict[useflag]
    else:
        return False

def getLocalUse(useflag):
    if useflag in localUseDict:
        return localUseDict[useflag]
    else:
        return False

def useconfIsValid(raw_useflag_list):
    for useflag in useflag_list:
        if useflag not in globalUseDict and useflag not in localUseDict:
            return False
    return True
