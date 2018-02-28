import urwid

class Ebuild_Pane:
    
    def __init__(self, cpv):
        self.cpv = cpv

        self.is_merged = self.cpv in ebuild_dict

        self.widget_list = []
