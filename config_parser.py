import subprocess
import re
import os

EPREFIX=subprocess.check_output(["portageq","envvar","EPREFIX"])
ETC=EPREFIX + "/etc"

class MakeConf:

# Importing make.conf
if os.path.isfile(ETC + '/make.conf'):
    make_conf = open(ETC + '/make.cnof', 'r')
else if os.path.isfile(ETC + '/portage/make.conf'):
    make_conf = open(ETC + '/portage/make.conf', 'r'):
else:
    return "make.conf not found!"

    def __init__(self):
        variables = {}


class PackageUse:

# Importing package.use
if os.path.isfile(ETC + '/portage/package.use'):
    package_use = open(ETC + '/portage/package.use')
else:
    return "package.use not found!"
        

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
    ACTIVE_FLAGS.insert(0, get_environment_useflags())
    ACTIVE_FLAGS.insert(1, get_makeconf_useflags())
    ACTIVE_FLAGS.insert(2, get_makedefaults_useflags())
    ACTIVE_FLAGS.insert(3, get_makeglobals_useflags())
    ACTIVE_FLAGS.insert(4, get_packageuse_useflags())
    ACTIVE_FLAGS.insert(5, get_iuse_useflags())
    ACTIVE_FLAGS.insert(6, get_usemask_useflags())
    ACTIVE_FLAGS.insert(7, get_useforce_useflags())
    ACTIVE_FLAGS.insert(8, get_portage_useflags())
