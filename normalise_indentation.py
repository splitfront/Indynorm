import sublime, sublime_plugin, time

# temp. solution for calling from NormaliseIndentationOnOpen,
# later gonna be refactored into smth more organised
def extract_indentation_prefs(st_settings):
    result = {}
    for n in ['tab_size', 'translate_tabs_to_spaces']:
        # we need False values too, thus explicit check
        if st_settings.get(n) != None: 
            result[n] = st_settings.get(n)
    return result

def get_prefs_base(view):
    """combine editor defaults and language-specific settings"""
    prefs_base = {}

    settings_subl = sublime.load_settings('Preferences.sublime-settings')
    prefs_subl = extract_indentation_prefs(settings_subl)
    log("indentation prefs from editor preferences", prefs_subl)
    prefs_base.update(prefs_subl)

    syntax = view.settings().get('syntax').split('/')[-1]
    # some ancient installations probably have .tmLanguage still...
    language = syntax.replace('.tmLanguage', '').replace('.sublime-syntax', '')
    settings_lang = sublime.load_settings(language + '.sublime-settings')
    prefs_lang = extract_indentation_prefs(settings_lang)
    log("indentation prefs from " + syntax, prefs_lang)
    prefs_base.update(prefs_lang)
    
    log("indentation preferences (editor & syntax, merged):", prefs_base)
    return prefs_base

def get_prefs_view(view):
    """get indentation settings for active tab"""

    # The default implementation of detect_lines requires 10 indented lines before it makes a guess
    # on indentation at all, and often make mistakes.
    # there's a better indentation detector: https://github.com/jfcherng/Sublime-AutoSetIndentation
    # which hooks into default command, and you're advised to install if if you're in ST <4050
    # self.view.run_command('detect_indentation')
    view.run_command('auto_set_indentation')

    fresh_view_settings = view.settings()
    prefs_view = extract_indentation_prefs(fresh_view_settings)
    log("indentation preferences for current view:", prefs_view)
    return prefs_view

def collapse_spaces_to_tabs(view):
    view.run_command('unexpand_tabs')
    view.settings().set('translate_tabs_to_spaces', False)

def expand_tabs_to_spaces(view):
    view.run_command('expand_tabs')
    view.settings().set('translate_tabs_to_spaces', True)

def set_tab_size_to_default(view):
    prefs_base = get_prefs_base(view)
    view.settings().set('tab_size', prefs_base['tab_size'])

def wait_for_view_to_populate(self):
    # e.g., sometimes self.view == None
    # time.sleep(0.2)
    # or we can do it like...
    while not self.view:
        pass

def log(*payload):
    settings = sublime.load_settings('NormaliseIndentation.sublime-settings')
    if settings.get('enable_logging', False):
        for chunk in payload:
            print(chunk)

class NormaliseIndentationCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        log('== * == * == * == * ==', 'Normalise Indentation')
        prefs_base = get_prefs_base(self.view)
        prefs_view = get_prefs_view(self.view)

        have_spaces, want_spaces, same_tab_size = [
            prefs_view['translate_tabs_to_spaces'],
            prefs_base['translate_tabs_to_spaces'],
            prefs_view['tab_size'] == prefs_base['tab_size']
        ]

        if have_spaces:
            if want_spaces:
                if same_tab_size:
                    # nothing to do, but we gotta deal with leftover mix of \t's and \s's
                    log('spaces/spaces/tab_size same -- replace tabs with spaces just in case')
                    wait_for_view_to_populate(self)
                    expand_tabs_to_spaces(self.view)
                else:
                    # normalize tab width by substition juggle
                    log("spaces/spaces/tab_size mismatch -- fix tab width w/ spaces->tabs->spaces trick")
                    wait_for_view_to_populate(self)
                    collapse_spaces_to_tabs(self.view)
                    set_tab_size_to_default(self.view)
                    expand_tabs_to_spaces(self.view)
            else: # want_tabs
                # whatever are tab widths we can just collapse
                log('spaces/tabs/tab_size whatever -- collapse spaces to tabs')
                wait_for_view_to_populate(self)
                collapse_spaces_to_tabs(self.view)
                set_tab_size_to_default(self.view)
        else: 
            # have tabs
            log("tabs/tabs OR spaces/tab_size whatever -- set correct tab size")
            wait_for_view_to_populate(self)
            set_tab_size_to_default(self.view) # won't hurt anyway
            if want_spaces:
                # now it can get SPACE'd if requred
                log("tabs/spaces/tab_size whatever -- expand tabs!")
                wait_for_view_to_populate(self)
                expand_tabs_to_spaces(self.view)

class NormaliseIndentationOnOpen(sublime_plugin.EventListener):
    # file is opened
    def on_load(self, view):
        return
        settings = sublime.load_settings('NormaliseIndentation.sublime-settings')
        if settings.get('normalise_indentation_on_load', False): 
            view.run_command('normalise_indentation')

    # view gains editing focus
    def on_activated(self, view): 
        return
        settings = sublime.load_settings('NormaliseIndentation.sublime-settings')
        if settings.get('normalise_indentation_on_activate', False):
            view.run_command('normalise_indentation')

    # def on_text_command(self, view, command_name, args):
    #     # old settings still available here
    #     print("\n\n\nOriginal tab settings detected:")
    #     view.run_command('auto_set_indentation')
    #     print(self.extract_indentation_prefs(self.get_prefs_view(view)))
    #     if command_name == "set_setting" and args['setting'] == 'tab_size':
    #         # new settings passed as parameters to listener
    #         print("As " + command_name + " is called, new settings are")
    #         print(args)
