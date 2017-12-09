import subprocess
import re
import os
import io

EPREFIX=subprocess.check_output(["portageq","envvar","EPREFIX"])
ETC=EPREFIX + "/etc"

class MakeConf:

    # Importing make.conf
    if os.path.isfile(ETC + '/make.conf'):
        make_conf = open(ETC + '/make.cnof', 'r')
    else if os.path.isfile(ETC + '/portage/make.conf'):
        make_conf = open(ETC + '/portage/make.conf', 'r'):
    else:
        raise FileNotFoundError("No make.conf found in /etc/portage/ or /etc/!")

    def __init__(self):
        self.variables = []
        self.variables_dict = {} 
        for i in make.conf:
            if i.find('=',0) != -1: # true if there is a '=' on this line
                self.variables.append(re.match('\S+(?=\s*=\s*")',i).group(0))
        for flag in variables:
            curRegex = '(?:' + flag + '\s*=\s*").*(?=")'
            variable_dict[flag] =  re.search(curRegex, make_conf.read(),re.MULTILINE)
        

class PackageUse:

# Importing package.use
if os.path.isfile(ETC + '/portage/package.use'):
    package_use = open(ETC + '/portage/package.use')
else:
    raise FileNotFoundError("No package.use found in /etc/portage/!")
        

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
