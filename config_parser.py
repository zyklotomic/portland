import re
import os
import io
import portage_env

EPREFIX = portage_env.EPREFIX
ETC = portage_env.ETC

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
        make_conf_dir = None

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
        package_use_dir = None

    # Maybe needs dict. created of all the dirs.
    def __init__(self, file_dir=package_use_dir):
        ConfFile.__init__(self)
        for j in collapse(file_dir):
            with open(j, 'r') as package_use:
                temp_list = []
                for i in package_use:
                    if i.find('#', 0) == -1 and i != '\n':
                        line_list =  i.split()
                        self.variables.append(line_list[0])
                        self.variables_dict[line_list[0]] = line_list[1:]

class UseMask(ConfFile):

    # Due to nature of ues.mask, having self.variables_dict
    # does not make sense.

    # importing use.mask
    if os.path.isfile(ETC + '/portage/profile/use.mask'):
        use_mask_dir = ETC + '/portage/profile/use.mask'
    else:
        use_mask_dir = None

    # variables_dict['file_path'] = variables in the file
    def __init__(self, file_dir=use_mask_dir):
        ConfFile.__init__(slf)
        for j in collapse(file_dir):
            with open(j, 'r') as use_mask:
                temp_list = []
                for i in use_mask:
                    if i.find('#', 0) == -1: # if line is uncommented
                        self.variables.append(i[:-1]) # -1 index to get rid of \n
                        temp_list.append(i[:-1])
                self.variables_dict[j] = temp_list

class PackageMask(ConfFile):

    if os.path.isdir(ETC + '/portage/package.mask'):
        package_use_dir = ETC + '/portage/package.mask'

    # variables_dict['file_path'] = variables in the file
    def __init__(self, file_dir=package_use_dir):
        ConfFile.__init__(self)
        for j in collapse(file_dir):
            with open(j, 'r') as package_mask:
                temp_list = []
                for i in package_mask:
                    if i != '\n':
                        self.variables.append(i[:-1])
                        temp_list.append(i[:-1])
                self.variables_dict[j] = temp_list

class PackageLicense(ConfFile):

    if os.path.isfile(ETC + '/portage/package.license'):
        package_license_dir = ETC + '/portage/package.license'
    else:
        package_license_dir = None

    def __init__(self, file_dir=package_license_dir):
        ConfFile.__init__(self)
        with open(file_dir, 'r') as package_license:
            for i in package_license:
                if i[:1] != '#':
                    self.variables.append(i)
                    self.variables_dict[i.split()[:1]] = i.split[1:]

class Ebuild(ConfFile):

    def __init__(self, cp): #cp category/package
        ConfFile.__init__(self)
        ebuild_dir = portage_env.EBUILD_TREE + '/' + cp
        self.cp = cp
        self.list_dir = os.listdir(ebuild_dir)
        self.ebuild_versions = [re.search('(-)(.*)(?=.ebuild)', i).group(2)
                               for i in self.list_dir
                               if i.find('.ebuild') != -1]
        
        # Only interested in select variables
        self.variables = ['DESCRIPTION', 'HOMEPAGE', 'SLOT', 'LICENSE', 'IUSE']
        temp_var_list = self.variables[:]
        # Pick an arbitrary ebuild file
        ebuild_file = [i for i in self.list_dir if i.find('.ebuild') != -1][0]

        with open(ebuild_dir + '/' + ebuild_file, 'r') as ebuild: # get ebuild directory correct
            for line in ebuild:
                if len(temp_var_list) == 0: 
                    break
                else:
                    for var in temp_var_list:
                        if line.find(var, 0) != -1:
                            var_val_regex = '({}.*=.*")(.*(?="))'.format(var)
                            var_value = re.search(var_val_regex, line).group(2)
                            self.variables_dict[var] = var_value
                            temp_var_list.remove(var)

    def get_cp(self):
        return self.cp
    
    def get_versions(self):
        return self.ebuild_versions
        

# Returns list of paths of all the files in a directory and it's subdirs.
def collapse(directory):
    if os.path.isfile(directory):
            return [directory]
    else:
        files = []
        list_dir = os.listdir(directory)
        for i in list_dir:
            if os.path.isfile(directory + '/' + i):
                    files.append(directory + '/' + i)
            else:
                for k in collapse(directory + '/' + i):
                    files.append(k)
        return files
