import useflag_data
from gui import urwidtable
import urwid

globalUseDict = useflag_data.getGlobalUseDict()
localUseDict = useflag_data.getLocalUseDict()

globalUseTable = urwidtable.Table(globalUseDict).get_utable()
listbox = urwid.Filler(globalUseTable, 'top')

k = urwid.MainLoop(listbox)
k.run()
