import urwid
import config_parser as cpa
import urwidtable

class Config_Pane(urwid.ListBox):
    def __init__(self):
        self.config_dicts = list(map(lambda x: x.getVariablesDict(),
            [cpa.MakeConf(), cpa.PackageUse(), cpa.PackageMask()]))
        titles = ["make.conf", "package.use", "package.mask"]

        self.tables = []
        for i,j in zip(self.config_dicts, titles):
            self.tables.append(urwidtable.Table(i, title=j))
            self.tables.append(urwid.Divider())
        self.walker = urwid.SimpleListWalker(self.tables)
        super(Config_Pane, self).__init__(self.walker)

    def get_title(self):
        return "Configuration File Settings"

if __name__ == '__main__':
    k = Config_Pane()
    palette = [('reversed', 'standout', ''),
            ('blue-bold', 'light blue', 'default', 'bold'),
            ('bold', 'white', '', 'underline'),
            ('green-bold', 'light green', 'default', 'bold')]
      
    loop = urwid.MainLoop(k, palette)
    loop.run()
