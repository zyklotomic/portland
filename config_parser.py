import subprocess
import re
import os
import io

EPREFIX=subprocess.check_output(["portageq","envvar","EPREFIX"]).decode().strip()
ETC=EPREFIX + "/etc"

class ConfFile:
    
    def __init__(self):
        """
        self.variables -- List of variables presenst in the config file
        self.variables_dict -- Dictionary of the variables and
        their corresponding variables
        """
        self.variables = []
        self.variables_dict = {}

    def getVariables(self, requestedVars=[]):
        k = []
        for i in requestedVars:
            if i in self.variables:
                k.append(self.variables_dict[i])
            else:
                k.append(-1)
        return k

    def getVariablesList(self):
        return self.variables

    def getVariablesDict(self):
        return self.variables_dict


class MakeConf(ConfFile):

    # Importing make.conf
    if os.path.isfile(ETC + '/make.conf'):
        make_conf_dir = ETC + '/make.conf'
    elif os.path.isfile(ETC + '/portage/make.conf'):
        make_conf_dir = ETC + '/portage/make.conf'
    else:
        raise FileNotFoundError("No make.conf found in /etc/portage/ or /etc/ !")

    def __init__(self, file_dir=make_conf_dir):
        ConfFile.__init__(self) 
        make_conf = open(file_dir, 'r')
       
        # Append all make.conf variables into self.variables
        for i in make_conf:
            if i.find('=',0) != -1: # true if there is a '=' on this line
                self.variables.append(re.match('\S+(?=\s*=\s*")',i).group(0))
                
        make_conf.close()

        # Collapse make_conf into a string w/o \n
        with open(file_dir, 'r') as s:
            make_conf_string = s.read().replace('\n', ' ') 
        # Enter the corresponding values to the keys into variables_dict        
        index = 0
        for variable in self.variables:
            index = make_conf_string.find(variable, index)
            self.variables_dict[variable] = re.search('(?<=")[^"]*', make_conf_string[index:]).group(0)
    

class PackageUse(ConfFile):

    # Importing package.use
    if os.path.isfile(ETC + '/portage/package.use'):
        package_use_dir = ETC + '/portage/package.use'
    else:
        raise FileNotFoundError("No package.use found in /etc/portage/!")
        
class UseMask(ConfFile):
    
    # Due to nature of ues.mask, having self.variables_dict
    # does not make sense.

    # importing use.mask
    if os.path.isfile(ETC + '/portage/profile/use.mask'):
        use_mask_dir = ETC + '/portage/profile/use.mask'
    else:
        raise FileNotFoundError("No use.mask found in /etc/portage/profile/ !")

    def __init__(self, file_dir=use_mask_dir):
        
        ConfFile.__init__(self) 
        with open(file_dir, 'r') as use_mask:
            for i in use_mask:
                if i.find('#', 0) == -1: # if line is uncommented
                    self.variables.append(i[:-1]) # -1 index to get rid of \n

class PackageMask(ConfFile):
    pass
    


"""
List format following the ACTIVE_FLAGS array in euse from gentoolkit. 
Indicies of ACTIVE_FLAGS, a list of enabled use flags:
    0: environment
    1: make.conf
    2: make.defaults
    3: make.globals, and local use flags
    4: package.use
    5: ebuild IUSE
    6: use.mask
    7: use.force
    8: flags indicated active by emerge --info (get_portageuseflags)
"""

ACTIVE_FLAGS = []

# USE Flag Getter Methods

def get_environment_useflags():
    pass
def get_makeconf_useflags():
    pass
def get_makeglobals_useflags():
    pass
def get_packageuse_useflags():
    pass
def get_iuse_useflags():
    pass
def get_usemask_useflags():
    pass
def get_useforce_useflags():
    pass
def get_portage_useflags():
    return subprocess.check_output(["portageq","envvar","USE"]).decode('utf8').split()

def fill_ACTIVE_FLAGS():
    useflag_methods = [ get_environment_useflags(),
                        get_makeconf_useflags(),
                        get_makedefaults_useflags(),
                        get_makeglobals_useflags(),
                        get_packageuse_useflags(),
                        get_iuse_useflags(),
                        get_usemask_useflags(),
                        get_useforce_useflags(),
                        get_portage_useflags() ]
    for i,j in enumerate(useflag_methods):
        ACTIVE_FLAGS.insert(i,j)
    """
    ACTIVE_FLAGS.insert(0, get_environment_useflags())
    ACTIVE_FLAGS.insert(1, get_makeconf_useflags())
    ACTIVE_FLAGS.insert(2, get_makedefaults_useflags())
    ACTIVE_FLAGS.insert(3, get_makeglobals_useflags())
    ACTIVE_FLAGS.insert(4, get_packageuse_useflags())
    ACTIVE_FLAGS.insert(5, get_iuse_useflags())
    ACTIVE_FLAGS.insert(6, get_usemask_useflags())
    ACTIVE_FLAGS.insert(7, get_useforce_useflags())
    ACTIVE_FLAGS.insert(8, get_portage_useflags())
    """
