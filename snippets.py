## get buffer contents

# view.substr(sublime.Region(0, view.size()))

## get current cursor position

# (row,col) = self.view.rowcol(self.view.sel()[0].begin())

## overwrite view content (even for unsaved views)
# https://forum.sublimetext.com/t/how-to-overwrite-the-content-of-an-untitled-view/32814/6

## views vs buffers
# https://forum.sublimetext.com/t/what-is-a-buffer/18353/2