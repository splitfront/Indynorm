import sublime
import sublime_plugin

import random
import string


def _find_view(window=None):
    """
    Check the current window for our temporary view.
    """
    window = sublime.active_window() if window is None else window

    for view in window.views():
        if view.settings().get("_temp_view", False):
            return view


def _temp_view(title, text, window=None, view=None):
    """
    Set the tab title and content of the provided view. If no view is provided,
    a new one is created first.
    """
    window = sublime.active_window() if window is None else window

    if view is None:
        view = window.new_file()
        view.settings().set("_temp_view", True)
    else:
        view.sel().clear()
        view.sel().add(sublime.Region(0, view.size()))
        view.run_command("left_delete")

    view.set_name(title)
    view.run_command("append", {"characters": text})


# class ExampleCommand(sublime_plugin.ApplicationCommand):
class FooBar:
    """
    Contrived example of creating or re-using a view.
    """
    count = 0

    def run(self):
        self.count += 1
        msg = "".join([random.choice(string.ascii_letters) for i in range(32)])

        _temp_view("Untitled %d" % self.count, "Text: %s" % msg, view=_find_view())