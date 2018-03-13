import os
import portage_env

# Returns dictionary of Global USE Flags as keys to values of flag desc. 
def getGlobalUseDict(directory=portage_env.USE_DESC):
    globalUseDict = {}
    with open(directory, 'r') as use_desc:
        for line in use_desc:
            # Potential improvement: Use regex instead?
            # Checks if line is not commented and non-empty
            if line[0:1] != "#" and line != '\n':
                useIndex = line.find(' - ', 0)
                globalUseDict[line[0:useIndex]] = line[useIndex+3:-1] 
    return globalUseDict

# Returns dictionary of dictionaries of local USE Flags. 
# Since flag desc. (due to diff behaviors) differs
# between ebuilds

def getLocalUseDict(directory=portage_env.USE_LOCAL_DESC):
    localUseDict = {}
    with open(directory, 'r') as use_local_desc:
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
                    localUseDict[useFlag] = {packageName : useFlagDesc}
                else:
                    localUseDict[useFlag][packageName] = useFlagDesc
    return localUseDict


def getGlobalUse(self, useflag):
    if useflag in self:
        return self[useflag]
    else:
        return -1

def getLocalUse(useflag):
    if useflag in self:
        return self[useflag]
    else:
        return -1

def useconfIsValid(raw_useflag_list):
    for useflag in useflag_list:
        if useflag not in globalUseDict and useflag not in localUseDict:
            return False
    return True
