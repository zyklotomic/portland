import urwid
import package_pane
import tree_pane

# class Pane
#    def __init__(self, title, mainview):
#        self.mainview 

class MainView(urwid.Frame):
    def __init__(self): # Default pane on launch
        self.tabs = []
        self.tab_focus = 0
        init_pane = tree_pane.Miller_Pane()
        edit_box = urwid.Edit()
        self.tabs.append(init_pane)
        self.pop_up_open = False
        
        pkg_pane = package_pane.vim_pane
        pkg_pane2 = package_pane.ebuild_2pane
        self.tabs.append(pkg_pane)
        self.tabs.append(pkg_pane2)        

        init_header = get_status_text(self.tab_focus, len(self.tabs),
                self.tabs[self.tab_focus].get_title())
         
        super(MainView, self).__init__(urwid.LineBox(self.tabs[self.tab_focus]), 
                header=init_header, footer=edit_box )
    
    def open_tabs_box(self):
        self.pop_up_open = True
        tab_buttons = []
        for index, tab in enumerate(self.tabs):
            text = str(index + 1) + ": " + "hihihih"
            button = urwid.Button(text)
            urwid.connect_signal(button, 'click', MainView.set_tab_focus, index)
            tab_buttons.append(button) 
        list_box = urwid.ListBox(urwid.SimpleFocusListWalker(tab_buttons))
        self.contents['body'] =  (list_box, None)

    def open_pane_choice(self):
        self.pop_up_open = True
        pane_buttons = []
 
    # def open_tabs_box(self):
    #     self.tabs_box_open = True
    #     tab_buttons = []
    #     for index,tab in enumerate(self.tabs):
    #         text = str(index + 1) + ": " + "hihi"
    #         button = urwid.AttrMap(urwid.Button(text), None, focus_map='reversed')
    #         urwid.connect_signal(button.original_widget, 'click', 
    #                 MainView.set_tab_focus, *[self, index])
    #         tab_buttons.append(button)
    #     list_walker = urwid.ListBox(urwid.SimpleFocusListWalker(tab_buttons))
    #     self.contents['body'] = (list_walker, None)

    def close_box(self):
        self.tabs_box_close = False
        self.contents['body'] = (urwid.LineBox(self.tabs[self.tab_focus]), None)
        
    def open_tab(self, pane):
        self.tabs.append(pane)
        self.set_tab_focus(len(self.tabs) - 1)

    def close_tab(self, index):
        if len(self.tabs) > 1:
            del self.tabs[index]
            self.set_tab_focus(index)

    def set_tab_focus(self, index):
        self.tab_focus = index % len(self.tabs) 
        self.contents['body'] = (urwid.LineBox(self.tabs[self.tab_focus]), None)
        self.contents['header'] = (get_status_text(self.tab_focus, len(self.tabs),
                self.tabs[self.tab_focus].get_title()), None)

    def handle_input(self, key):
        if self.pop_up_open:
            if key == 'esc':
                self.close_box()
        
        if key in [str(i) for i in range(1,10)]:
            self.set_tab_focus(int(key)-1)
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
        if key == 'T':
            self.open_tabs_box()

def get_status_text(focus_index, num_tab, title):
    tab_text =  "Tab: " + str(focus_index + 1) + "/" + str(num_tab)
    return urwid.Columns([urwid.Text(title, align='left'), 
        urwid.Text(tab_text, align='right')])
 
palette = [('reversed', 'standout', ''),
        ('blue-bold', 'light blue', 'default', 'bold'),
        ('bold', 'white', '', 'underline'),
        ('green-bold', 'light green', 'default', 'bold')]

if __name__ == '__main__':
    mainv = MainView()
    loop = urwid.MainLoop(mainv, palette, unhandled_input=mainv.handle_input)
    loop.run()
