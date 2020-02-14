import sublime, sublime_plugin

class IndynormCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.log('\n\n\n', '== * == * == * == * ==', 'Indynorm:')
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
                    # nothing to do, but in case there are leftover \t's...
                    self.log("action taken", {
                        'from': 'spaces',
                        'to': 'spaces',
                        'size': 'same',
                        'do':'replace tabs with spaces just in case'
                        })
                    self.expand_tabs_to_spaces()
                else:
                    # normalize tab width by substition round-trip
                    self.log("action taken", {
                        'from': 'spaces',
                        'to': 'spaces',
                        'size': 'MISMATCH',
                        'do':'replacement roundtrip!'
                    })
                    self.collapse_spaces_to_tabs()
                    self.set_tab_size_to_default()
                    self.expand_tabs_to_spaces()
            else: # want_tabs
                # whatever are tab widths we can just collapse
                self.log("action taken", {
                    'from': 'spaces',
                    'to': 'tabs',
                    'size': 'whatever',
                    'do': 'collapse spaces seq`s to tabs'
                    })
                self.collapse_spaces_to_tabs()
                self.set_tab_size_to_default()
        else: # have tabs
            self.log("action taken", {
                'from': 'tabs',
                'to': 'whatever',
                'size': 'whatever',
                'do':'expand tabs to spaces'
                })
            self.set_tab_size_to_default() # won't hurt anyway
            if want_spaces:
                # now it can get SPACE'd if requred
                self.expand_tabs_to_spaces()

    def extract_indentation_prefs(self, st_settings):
        result = {}
        for n in ['tab_size', 'translate_tabs_to_spaces']:
            # we need False values too
            if st_settings.get(n) != None: 
                result[n] = st_settings.get(n)
        return result

    def get_prefs_base(self):
        """combine editor defaults and language-specific settings"""
        prefs_base = {}

        settings_subl = sublime.load_settings('Preferences.sublime-settings')
        prefs_subl = self.extract_indentation_prefs(settings_subl)
        self.log("-- indentation prefs for editor", prefs_subl)
        prefs_base.update(prefs_subl)

        syntax = self.view.settings().get('syntax').split('/')[-1]
        language = syntax.replace('.tmLanguage', '').replace('.sublime-syntax', '')
        settings_lang = sublime.load_settings(language + '.sublime-settings')
        prefs_lang = self.extract_indentation_prefs(settings_lang)
        self.log("-- indentation prefs (syntax) for " + syntax, prefs_lang)
        prefs_base.update(prefs_lang)
        
        self.log("-- indentation prefs (merged local):", prefs_base)
        return prefs_base

    def get_prefs_view(self):
        """get indentation settings for active tab"""

        # The default implementation of detect_lines requires 10 indented lines before it makes a guess
        # on indentation at all, and often make mistakes.
        # there's a better indent. detector: https://github.com/jfcherng/Sublime-AutoSetIndentation
        # which hooks into default command,
        self.view.run_command('detect_indentation')

        freshly_updated_view_settings = self.view.settings()
        prefs_view = self.extract_indentation_prefs(freshly_updated_view_settings)
        self.log("-- prefs_view:", prefs_view)
        return prefs_view

    ## whitespace manipulation methods
    def collapse_spaces_to_tabs(self):
        self.clean_up_operations_queue()
        self.view.run_command('unexpand_tabs')
        self.view.settings().set('translate_tabs_to_spaces', False)

    def expand_tabs_to_spaces(self):
        self.clean_up_operations_queue()
        self.view.run_command('expand_tabs')
        self.view.settings().set('translate_tabs_to_spaces', True)

    def set_tab_size_to_default(self):
        self.clean_up_operations_queue()
        self.view.settings().set('tab_size', self.prefs_base['tab_size'])

    def clean_up_operations_queue(self):
        # e.g., sometimes self.view == None, we used time.sleep(1) before
        while not self.view:
            pass

    def log(self, *payload):
        if sublime.load_settings('Indynorm.sublime-settings').get('debug_mode', False):
            for chunk in payload:
                print(chunk)

class IndynormOnOpen(sublime_plugin.EventListener):

    def on_load(self, view):
        settings = sublime.load_settings('Indynorm.sublime-settings')
        if settings.get('convert_on_open', False): 
            view.run_command('indynorm')

    # view gains editing focus
    def on_activated(self, view): 
        settings = sublime.load_settings('Indynorm.sublime-settings')
        if settings.get('convert_on_activate', False):
            view.run_command('indynorm')