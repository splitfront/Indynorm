# get buffer contents

view.substr(sublime.Region(0, view.size()))

# get current cursor position

(row,col) = self.view.rowcol(self.view.sel()[0].begin())