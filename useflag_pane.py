import urwid
import useflag_data
import urwidtable

global_dict = useflag_data.getGlobalUseDict()
local_dict = useflag_data.getLocalUseDict()

def filter_dict(usedict, bool_func):
    keys = [i for i in list(usedict.keys()) if bool_func(i)]
    return {n: usedict[n] for n in keys}

def filter_dict_str_search(usedict, string):
    return filter_dict(usedict, lambda x: x.find(string) != -1)

def get_lwidget_list(usedict=local_dict):
    l_widget_list = [urwid.Text(('bold', "Local USE Flags"))]
    for j in usedict:
        table = urwidtable.Table(row_dict=usedict[j], title=j)
        l_widget_list.append(table)
        l_widget_list.append(urwid.Divider())
    return l_widget_list

def get_gwidget_list(usedict=global_dict):
    return [urwidtable.Table(usedict, title="Global USE Flags")]

tt = filter_dict(global_dict, lambda x: x.find("sy") != -1)

class USEFlag_Pane(urwid.Frame):
    def __init__(self, state='local'): 
        self.state = state
        if self.state == 'local':
            self.walker = urwid.SimpleListWalker(get_lwidget_list())
        if self.state == 'global':
            self.walker = urwid.SimpleListWalker(get_gwidget_list())
        self.col_w = urwid.ListBox(self.walker)
        self.edit_box = urwid.Edit("Search: ")
        urwid.connect_signal(self.edit_box, 'change', 
                lambda edit,text: self.search_update(text))

        super(USEFlag_Pane, self).__init__(self.col_w, footer=self.edit_box)

    def keypress(self, size, key):
        if key != '/':
            key = super(USEFlag_Pane, self).keypress(size, key)
        elif key == '/':
            self.focus_position = 'footer'
        elif key == 'esc':
            self.focus_position = 'body'

    def search_update(self, string):
        try:
            if self.state == 'local':
                fltr_dict = {n: local_dict[n] for n in local_dict if n.find(string) != -1}
                self.col_w.body = urwid.SimpleListWalker(get_lwidget_list(fltr_dict))
                self.contents['body'] = self.col_w.body
            if self.state == 'global':
                fltr_dict = {n: global_dict[n] for n in global_dict if n.find(string) != -1}
                self.col_w.body = urwid.SimpleListWalker(get_gwidget_list(fltr_dict))
                self.contents['body'] = self.col_w.body
        except:
            pass

    def get_title(self):
        return "USE Flag Index"

if __name__ == '__main__':
    palette = [('blue-bold', 'light blue', 'default', 'bold'),
            ('green-bold', 'light green', '', 'bold')]
    pane = USEFlag_Pane()
    loop = urwid.MainLoop(pane, palette)
    loop.run()
