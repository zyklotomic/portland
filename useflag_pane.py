import urwid
import useflag_data
import urwidtable

global_dict = useflag_data.getGlobalUseDict()
local_dict = useflag_data.getLocalUseDict()

class USEFlag_Pane(urwid.ListBox):

    def __init__(self): 
        self.walker = urwid.SimpleListWalker(self.get_l_widget_list())
        super(USEFlag_Pane, self).__init__(self.walker)

    def flag_filter(self, bool_func):
        widget_list = [i for i in self.global_dict]
        self.body = urwid.SimpleListWalker(widget_list)

    def search(self, search_str):
        bool_func = lambda x: x.find(search_str) != -1
        self.flag_filter(bool_func)
        self.contents = (get_g_widget_list)

    def get_g_widget_list(self, usedict=global_dict):
        g_widget_list = []
        for i in usedict:
            g_widget_list.append(urwid.text(('blue-bold', i)))
            g_widget_list.append(urwid.text(self.global_dict[i]))
            g_widget_list.append(urwid.divider())
        return g_widget_list

    def get_l_widget_list(self, usedict=local_dict):
        l_widget_list = []
        for j in usedict:
            table = urwidtable.Table(row_dict=usedict[j], title=j)
            l_widget_list.append(table)
            l_widget_list.append(urwid.Divider())
        return l_widget_list


palette = [('blue-bold', 'light blue', 'default', 'bold'),
        ('green-bold', 'light green', '', 'bold')]
pane = USEFlag_Pane()
loop = urwid.MainLoop(pane, palette)
loop.run()
