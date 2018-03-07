import urwid
import useflag_data

class USEFlag_Pane:

    def __init__(self, global_dict, local_dict):
        self.global_dict = global_dict
        self.local_dict = local_dict
        
        g_widget_list = []
        for i in self.global_dict:
            g_widget_list.append(urwid.Text(('blue-bold', i)))
            g_widget_list.append(urwid.Text(self.global_dict[i]))
            g_widget_list.append(urwid.Divider())

        self.glistbox = urwid.ListBox(urwid.SimpleListWalker(g_widget_list))

    def get_gwidget(self):
        return self.glistbox

palette = [('blue-bold', 'light blue', 'default', 'bold')]
gl = useflag_data.getGlobalUseDict()
ll = {}
pane = USEFlag_Pane(gl, ll)
loop = urwid.MainLoop(pane.get_gwidget(), palette)
loop.run()
