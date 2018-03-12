import os
import portage_env
import urwid
import config_parser 
import package_pane

list_dir = [i for i in os.listdir(portage_env.EBUILD_TREE) 
        if os.path.isdir(portage_env.EBUILD_TREE + '/' + i)]
tree_dict = {}

for j in list_dir:
    cpv_dir = portage_env.EBUILD_TREE + '/' + j
    cpv_dir_list = os.listdir(cpv_dir)
    tree_dict[j] = [i for i in cpv_dir_list if os.path.isdir(cpv_dir + '/' + i)]

class Miller_Pane(urwid.Columns):
    def __init__(self, col=list_dir):
        button_list = []
        for i in list_dir:
            button = urwid.AttrMap(urwid.Button(i), None, focus_map='reversed')
            button_list.append(button)

        left_walker = urwid.SimpleFocusListWalker(button_list)
        urwid.connect_signal(left_walker, "modified", Miller_Pane.update_rcol, self)
        self.left_col = urwid.ListBox(left_walker)

        self.right_col = self.get_rcol('app-editors')

        self.columns = list(map(lambda x: urwid.AttrMap(x, None, focus_map='blue-bold'),
                [self.left_col, self.right_col]))
        super(Miller_Pane, self).__init__(self.columns, dividechars=1)

    def get_rcol(self, cat):
        right_col = urwid.ListBox(urwid.SimpleFocusListWalker(
                get_pkg_buttons(cat))) # get button label
        return right_col

    def update_rcol(self):
        curr_button_label = get_focused_label(self.left_col) # get button label
        rcol = self.get_rcol(curr_button_label) 
        self.contents[1] = (urwid.AttrMap(rcol, None, focus_map='blue-bold'), self.options())

    def get_col()

def get_pkg_buttons(cat):
    button_list = []
    for pkg in tree_dict[cat]:
        button = urwid.AttrMap(urwid.Button(pkg), None, focus_map='reversed')
        urwid.connect_signal(button.original_widget, 'click', open_pane, pkg)
        button_list.append(button)
    return button_list

def get_focused_label(listwalker):
    return str(listwalker.get_focus()[0].original_widget.get_label())

def open_pane(pkg):
    pass

palette = [('reversed', 'standout', ''),
            ('blue-bold', 'light blue', 'default', 'bold')]

# loop = urwid.MainLoop(Miller_Pane(), palette)
# loop.run()
