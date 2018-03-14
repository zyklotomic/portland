import urwid
import package_pane
import tree_pane
import useflag_pane
import config_pane
import config_parser

class MainView(urwid.Frame):
    def __init__(self): # Default pane on launch
        self.tabs = []
        self.tab_focus = 0
        init_pane = tree_pane.Miller_Pane()
        edit_box = urwid.Edit()
        self.tabs.append(init_pane)
        self.pop_up_open = False
        
        init_header = get_status_text(self.tab_focus, len(self.tabs),
                self.tabs[self.tab_focus].get_title())
         
        super(MainView, self).__init__(urwid.LineBox(self.tabs[self.tab_focus]), 
                header=init_header, footer=edit_box)
    
    def open_tabs_box(self):
        self.pop_up_open = True
        tab_buttons = []
        for index, tab in enumerate(self.tabs):
            text = str(index + 1) + ": " + tab.get_title()
            button = urwid.AttrMap(urwid.Button(text), None, focus_map='reversed')
            urwid.connect_signal(button.original_widget, 'click', 
                    lambda button,index: self.set_tab_focus(index), index)
            tab_buttons.append(button)
        
        list_box = urwid.ListBox(urwid.SimpleFocusListWalker(tab_buttons))
        self.contents['body'] = (list_box, None)       

    def open_pane_choice(self):
        self.pop_up_open = True
        tree_button = urwid.Button("Category / Package Tree List")
        usel_button = urwid.Button("Local USE Flag Index")
        useg_button = urwid.Button("Global USE Flag Index") 
        conf_button = urwid.Button("Configuration Files")
        enter_pkg = urwid.Edit("Get Package Information <category/package-name>: ")
        
        urwid.connect_signal(tree_button, 'click', 
                lambda button,pane: self.open_tab(pane), tree_pane.Miller_Pane())
       
        urwid.connect_signal(usel_button, 'click', 
                lambda button,pane: self.open_tab(pane), useflag_pane.USEFlag_Pane())
        
        urwid.connect_signal(useg_button, 'click', 
                lambda button,pane: self.open_tab(pane), useflag_pane.USEFlag_Pane(state='global'))

        urwid.connect_signal(conf_button, 'click', 
                lambda button,pane: self.open_tab(pane), config_pane.Config_Pane())
 
        urwid.connect_signal(enter_pkg, 'change', 
                lambda edit,text: self.open_pkgtab(text))
        
        pane_buttons = list(map(lambda x: urwid.AttrMap(x, None, focus_map='reversed'),
            [tree_button, usel_button, useg_button, conf_button, enter_pkg]))
        
        pane_choices = urwid.ListBox(urwid.SimpleFocusListWalker(pane_buttons))
        self.contents['body'] = (pane_choices, None)

    def open_pkgtab(self, pkg):
        try:
            self.open_tab(package_pane.Package_Pane(
                config_parser.Ebuild(pkg)))
        except:
            pass


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
 
    def set_focus(self):
        self.set_tab_focus(0)

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
        if key == 'o':
            self.open_pane_choice()

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


        # pkg_pane = package_pane.vim_pane
        # pkg_pane2 = package_pane.ebuild_2pane
        # usef_pane = useflag_pane.USEFlag_Pane() 
        # self.tabs.append(pkg_pane)
        # self.tabs.append(pkg_pane2)
        # self.tabs.append(usef_pane)
