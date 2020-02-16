import sublime, sublime_plugin

class NormaliseIndentationCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.log('\n\n\n', '== * == * == * == * ==', 'Normalise Indentation')
        self.prefs_base = self.get_prefs_base()
        self.prefs_view = self.get_prefs_view()

        have_spaces, want_spaces, same_tab_size = [
            self.prefs_view['translate_tabs_to_spaces'],
            self.prefs_base['translate_tabs_to_spaces'],
            self.prefs_view['tab_size'] == self.prefs_base['tab_size']
        ]

        if have_spaces:
            if want_spaces:
                if same_tab_size:
                    # nothing to do, but we gotta deal with leftover mix of \t's and \s's
                    self.log('spaces/spaces/same size -- replace tabs with spaces just in case');
                    self.expand_tabs_to_spaces()
                else:
                    # normalize tab width by substition juggle
                    self.log("spaces/spaces/size_mismatch -- fix tab width w/ spaces->tabs->spaces trick")
                    self.collapse_spaces_to_tabs()
                    self.set_tab_size_to_default()
                    self.expand_tabs_to_spaces()
            else: # want_tabs
                # whatever are tab widths we can just collapse
                self.log('spaces/tabs/whatever -- collapse spaces to tabs')
                self.collapse_spaces_to_tabs()
                self.set_tab_size_to_default()
        else: 
            # have tabs
            self.log("tabs/whatever/whatever -- set correct tab size")
            self.set_tab_size_to_default() # won't hurt anyway
            if want_spaces:
                # now it can get SPACE'd if requred
                self.log("tabs/spaces/whatever -- expand tabs!")
                self.expand_tabs_to_spaces()

    def extract_indentation_prefs(self, st_settings):
        result = {}
        for n in ['tab_size', 'translate_tabs_to_spaces']:
            # we need False values too, thus explicit check
            if st_settings.get(n) != None: 
                result[n] = st_settings.get(n)
        return result

    def get_prefs_base(self):
        """combine editor defaults and language-specific settings"""
        prefs_base = {}

        settings_subl = sublime.load_settings('Preferences.sublime-settings')
        prefs_subl = self.extract_indentation_prefs(settings_subl)
        self.log("indentation prefs from editor preferences", prefs_subl)
        prefs_base.update(prefs_subl)

        syntax = self.view.settings().get('syntax').split('/')[-1]
        # some ancient installations probably have .tmLanguage still...
        language = syntax.replace('.tmLanguage', '').replace('.sublime-syntax', '')
        settings_lang = sublime.load_settings(language + '.sublime-settings')
        prefs_lang = self.extract_indentation_prefs(settings_lang)
        self.log("indentation prefs from " + syntax, prefs_lang)
        prefs_base.update(prefs_lang)
        
        self.log("indentation preferences (editor & syntax, merged):", prefs_base)
        return prefs_base

    def get_prefs_view(self):
        """get indentation settings for active tab"""

        # The default implementation of detect_lines requires 10 indented lines before it makes a guess
        # on indentation at all, and often make mistakes.
        # there's a better indentation detector: https://github.com/jfcherng/Sublime-AutoSetIndentation
        # which hooks into default command, and you're advised to install if if you're in ST <4050
        # self.view.run_command('detect_indentation')
        view.run_command('auto_set_indentation')

        fresh_view_settings = self.view.settings()
        prefs_view = self.extract_indentation_prefs(fresh_view_settings)
        self.log("indentation preferences for current view:", prefs_view)
        return prefs_view

    def collapse_spaces_to_tabs(self):
        self.wait_for_self_view_to_populate()
        self.view.run_command('unexpand_tabs')
        self.view.settings().set('translate_tabs_to_spaces', False)

    def expand_tabs_to_spaces(self):
        self.wait_for_self_view_to_populate()
        self.view.run_command('expand_tabs')
        self.view.settings().set('translate_tabs_to_spaces', True)

    def set_tab_size_to_default(self):
        self.wait_for_self_view_to_populate()
        self.view.settings().set('tab_size', self.prefs_base['tab_size'])

    def wait_for_self_view_to_populate(self):
        # e.g., sometimes self.view == None
        while not self.view:
            pass

    def log(self, *payload):
        settings = sublime.load_settings('NormaliseIndentation.sublime-settings')
        if settings.get('enable_logging', False):
            for chunk in payload:
                print(chunk)

class NormaliseIndentationOnOpen(sublime_plugin.EventListener):

    def on_load(self, view):
        settings = sublime.load_settings('NormaliseIndentation.sublime-settings')
        if settings.get('normalise_indentation_on_load', False): 
            view.run_command('normalise_indentation')

    # view gains editing focus
    def on_activated(self, view): 
        settings = sublime.load_settings('NormaliseIndentation.sublime-settings')
        if settings.get('normalise_indentation_on_activate', False):
            view.run_command('normalise_indentation')