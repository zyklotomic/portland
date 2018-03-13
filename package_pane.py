import urwid
import useflag_data
import urwidtable
import config_parser
import vardb
import portage_env
import os
import re

class Package_Pane(urwid.ListBox):
    def __init__(self, ebuild):  
        title = urwid.Text(('blue-bold', ebuild.get_cp()))
        
        row_titles = ['Description', 'Homepage', 'SLOT(S)', 'License', 'IUSE']
        title_keys = ['DESCRIPTION', 'HOMEPAGE', 'SLOT'   , 'LICENSE', 'IUSE']
        ebuild_vd = ebuild.getVariablesDict()
        row_dict = {}
        self.title = ebuild.get_cp()
         
        # Detecting the available variables
        for j,i in enumerate(title_keys):
            if i in ebuild_vd:
                row_dict[row_titles[j]] = ebuild_vd[i]
            else:
                row_dict[row_titles[j]] = 'None'
        
        # PKG INFO
        pkg_table = urwidtable.Table(row_dict)
        divider = urwid.Divider('-')
        
        # AVAILABLE INFO
        versions_title = urwid.Text(('bold', 'Available Versions'))
        versions = [urwid.Text(i) for i in ebuild.get_versions()] 

        # MERGED INFO
        emerge_title = urwid.Text(('bold', 'Emerge History'))

        emerged_tables = [] 
        if ebuild.get_cp() in vardb.cp_list:
            db_dir = portage_env.VARDBPKG + '/' + ebuild.get_cat()
            list_dir = os.listdir(db_dir)
            package_name = re.search('(.*/)(.*)', ebuild.get_cp()).group(2)
            merged_list = [i for i in list_dir if i.find(package_name, 0) != -1]
            for k in merged_list:
                curEbuild = vardb.MergedEbuild(ebuild.get_cat() + '/' + k)
                curEbuild_dict = curEbuild.get_var_dict() 
                ebuild_row_titles = ['BUILD_TIME', 'CFLAGS', 'CXXFLAGS', 'LDFLAGS',
                                     'CHOST', 'IUSE_EFFECTIVE', 
                                     'IUSE', 'SLOT', 'USE', 'DEPEND',
                                     'FEATURES', 'LICENSE', 'repository']  
                merged_dict = {}
                for t in ebuild_row_titles:
                    try:
                        merged_dict[t] = curEbuild_dict[t]
                    except:
                        pass

                ebuild_table = urwidtable.Table(merged_dict, title=k)
                emerged_tables.append(ebuild_table) 
        else:
            emerged_tables.append(urwid.Text('No past merges'))


        widget_list = [title, pkg_table, divider, versions_title, *versions, divider,
                      emerge_title, *emerged_tables]
        
        super(Package_Pane, self).__init__(urwid.SimpleFocusListWalker(widget_list))

    def get_title(self):
        return self.title

# palette = [('blue-bold', 'light blue', 'default', 'bold'),
#             ('bold', 'white', 'default', 'bold'),
#             ('italics', 'white', '', 'underline'),
#             ('green-bold', 'light green', 'default', 'bold')]
vim_ebuild = config_parser.Ebuild('dev-lang/python')
ebuild_2 = config_parser.Ebuild('app-editors/neovim')
ebuild_2pane = Package_Pane(ebuild_2)
vim_pane = Package_Pane(vim_ebuild)
# loop = urwid.MainLoop(vim_pane, palette)
# loop.run()
