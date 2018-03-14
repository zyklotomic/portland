import urwid

class Table(urwid.Pile): 
    
    def __init__(self, row_dict, column_headers=[], title=None):
        self.title = title
        self.row_dict = row_dict
        self.column_headers = column_headers
        self.num_col_h  = len(column_headers)
        self.num_row = len(row_dict) 
        palette = [('boldt', 'white', 'light red', 'bold')]
        
        if len(self.column_headers) != 0:
            for i in row_dict:
                if len(row_dict[i]) != self.num_col_h:
                    raise TypeError("Number of column entries does not match up with number of column headers")
        
        self.rowtitle_len = max([len(i) for i in row_dict]) # Shortest length of row title
        # Creation of urwid widget
        u_rows = [] # list of urwid row objects to be piled 
        if self.title != None:
            title_text = urwid.AttrMap(urwid.Text(self.title, align='left'),
                    'blue-bold')
            u_rows.append(title_text)

        if len(self.column_headers) != 0:
            header_row = [urwid.Divider('-')] + [urwid.Text(i, align='left') for i in self.column_headers]
            u_rows.append(urwid.Columns(header_row))

        for r in self.row_dict:
            row_list = [('fixed', self.rowtitle_len, urwid.Text(('green-bold', r)))]
            row_list.append(urwid.Text(self.row_dict[r]))
            u_rows.append(urwid.Columns(row_list, dividechars=1))

        super(Table, self).__init__(u_rows)

    
    def get_row(self, row_title): 
        return self.row_dict[row_title]

    def get_entry(self, row_title, column_header):
        i = self.column_headers.index(column_header)
        return self.get_row(column_headers)[i]

    def get_column_headers(self): 
        return self.column_headers

    def get_num_row(self): 
        return self.num_row

    def get_utable(self, filter_function=None): 
        return self.utable
         

# if __name__ == "__main__":
#     rd = {"Apple" : ('red', '5', '6'), "Pear" : ('white', '1', '80')}
#     useTable = Table(rd, column_headers=['color', 'price', 'quantity'])
#     cnn = urwid.Columns([urwid.Text("hi"), urwid.Divider(), urwid.Text("wow"), urwid.Text("ree")])
#     loop = urwid.MainLoop(urwid.Filler(urwid.Pile([useTable.get_utable(), cnn]), 'top'))
#     loop.run()
