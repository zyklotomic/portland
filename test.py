import urwid
import os
import vardb
import portage_env
import re

list_dir = [i for i in os.listdir(portage_env.EBUILD_TREE)
        if os.path.isdir(portage_env.EBUILD_TREE + '/' + i)]

tree_dict = {}

for i in list_dir:
    tree_dict[i] = [i for i in os.listdir(portage_env.EBUILD_TREE + '/' + i)
            if True] # will fix later 

button_list = [urwid.Button(i) for i in list_dir]

def get_pkg_buttons(cat):
    button_listk = []
    for pkg in tree_dict[cat]:
        button = urwid.Button(i)
        button_listk.append(button)
    return button_listk

left_col = urwid.ListBox(urwid.SimpleFocusListWalker(button_list))
r_col = urwid.ListBox(urwid.SimpleFocusListWalker(
    [urwid.Button(i) for i in tree_dict[left_col.focus.get_label()]]))
col = urwid.Columns([left_col, r_col])

loop = urwid.MainLoop(col)
loop.run()
