import urwid
import package_pane
import tree_pane

class MainView(urwid.Frame):
    def __init__(self): # Default pane on launch
        self.tabs = []
        self.tab_focus = 0
        init_header = urwid.Text(str(self.tab_focus)) 
        init_pane = tree_pane.Miller_Pane()
        edit_box = urwid.Edit()
        self.tabs.append(init_pane)
         
        pkg_pane = package_pane.vim_pane
        pkg_pane2 = package_pane.ebuild_2pane
        self.tabs.append(pkg_pane)
        self.tabs.append(pkg_pane2)


        super(MainView, self).__init__(self.tabs[self.tab_focus], 
                header=init_header, footer=edit_box )
    
    def open_tab(self, pane):
        self.tabs.append(pane)
        self.set_tab_focus(len(self.tabs) - 1)

    def close_tab(self, index):
        if len(self.tabs) > 1:
            del self.tabs[index]
            self.set_tab_focus(index)

    def set_tab_focus(self, index):
        self.tab_focus = index % len(self.tabs) 
        self.contents['body'] = (self.tabs[self.tab_focus], None)
        self.contents['header'] = (urwid.Text(str(self.tab_focus)), None)

    def handle_input(self, key):
        if key in [str(i) for i in range(0,10)]:
            self.set_tab_focus(int(key))
        if key == 'x' or key == 'X':
            self.close_tab(self.tab_focus)
        if key == 'tab':
            self.set_tab_focus(self.tab_focus + 1)
        if key == 'shift tab':
            self.set_tab_focus(self.tab_focus - 1)
        if key == 'esc':
            self.focus_position = 'body'
        if key == '/':
            self.focus_position = 'footer'
        if key == 'n':
            self.open_tab(tree_pane.Miller_Pane())
        if key == 'd':
            self.close_tab(self.tab_focus)


palette = [('reversed', 'standout', ''),
        ('blue-bold', 'light blue', 'default', 'bold'),
        ('bold', 'white', '', 'underline')]

k = MainView()
loop = urwid.MainLoop(k, palette, unhandled_input=k.handle_input)
loop.run()
