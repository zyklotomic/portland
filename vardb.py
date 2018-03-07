import portage_env
import re
from os import listdir

category_list = listdir(portage_env.VARDBPKG)
cpv_list = []

for cat in category_list:
    for pkg in listdir(portage_env.VARDBPKG + '/' + cat):
        cpv_list.append(cat + '/' + pkg)

cp_list = [re.search('.*(?=-[0-9])', i).group(0) for i in cpv_list]

class MergedEbuild:

    def __init__(self, cpv):
        slash_index = cpv.find('/', 0)
        self.category = cpv[:slash_index]
        self.package_name = cpv[slash_index + 1:]
        
        self.db_var_dict = {}
        self.file_names_list = listdir(portage_env.VARDBPKG + '/' + cpv)
        for file_name in self.file_names_list:
            try: # In the case file is not a text file, such as environment.bz2
                with open(portage_env.VARDBPKG + '/' + cpv + '/' + file_name) as the_file:
                    self.db_var_dict[file_name] = the_file.read()
            except:
                pass
    
    def get_var_dict(self):
        return self.db_var_dict

    def get_package_name(self):
        return self.package_name
