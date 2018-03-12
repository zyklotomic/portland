import urwid
import useflag_data

class USEFlag_Pane(urwid.ListBox):

    def __init__(self): 
        g_widget_list = []
        for i in self.global_dict:
            g_widget_list.append(urwid.Text(('blue-bold', i)))
            g_widget_list.append(urwid.Text(self.global_dict[i]))
            g_widget_list.append(urwid.Divider())

        self.walker = self.SimpleListWalker() 
        self.glistbox = urwid.ListBox(urwid.SimpleListWalker(g_widget_list))
        super(USEFlag_Pane, self).__init__(self.walker)

    def flag_filter(self, bool_func):
        widget_list = [ i for i in listb if bool_func(i)]
        self.body = urwid.SimpleListWalker(widget_list)

    def search(self, search_str):
        bool_func = lambda x: x.find(search_str) != -1
        self.flag_filter(bool_func)

palette = [('blue-bold', 'light blue', 'default', 'bold')]
gl = useflag_data.getGlobalUseDict()
ll = {}
pane = USEFlag_Pane(gl, ll)
loop = urwid.MainLoop(pane.get_gwidget(), palette)
loop.run()
