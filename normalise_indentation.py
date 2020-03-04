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
        self.view.run_command('auto_set_indentation')

        fresh_view_settings = self.view.settings()
        prefs_view = self.extract_indentation_prefs(fresh_view_settings)
        self.log("indentation preferences for current view:", prefs_view)
        return prefs_view

    def collapse_spaces_to_tabs(self):
        self.wait_for_self_view_to_populate()
        self.view.run_command('unexpand_tabs')
        self.view.settings().set('translate_tabs_to_spaces', False)

    def collapse_spaces_to_tabs_line_by_line(self, tab_size__old, tab_size__new):
        """
        Instead of just collapsing sequences of spaces to tab symbols _globally_, we:

        - process file line by line;
        - watch for sudden indentation jumps:
            - OK: 1 level, 2 levels, 3 levels
            - WEIRD: 1 level, 4 levels, 3 levels
        - we keep track of last non-weird indentation level
        - for "weird" lines, we calculate amount of leading whitespace required
          for keeping relative left margin as close as possible to original.
        """

        def reindent_basic(line):
            tabsize = line["tab_size__new"]
            lvl = line["level"]
            whitespaceless = line["stripped"]
            return (" " * tabsize * level) + whitespaceless

        def reindent_tricky(line):
            return line

        def parse_indentation(raw_line, tab_size__old, tab_size__new):
            """
            to properly reindent every line we need some info
            about indentation of it's predecessor
            """
            detabbed = raw_line.replace("\t", " " * tab_size_old)
            stripped = raw_line.lstrip()
            spaces = len(detabbed) - len(stripped)
            return {
                "tab_size__old" : tab_size__old,
                "tab_size__new" : tab_size__new,
                "raw"           : raw_line,
                "detabbed"      : detabbed,
                "stripped"      : stripped,
                "level__abs"    : spaces,
                "level"         : spaces // tab_size__old,
                "padding"       : spaces % tab_size__old,
                "reindent_with" : None
                }

        def reindent_line(line, line_above):
            """
            - TODO: cash calculated reindentations and use them instead of recalculating
            """
            tab_in_whitespaces = " " * line["tab_size__new"]
            do_shallow_step = lambda : line["level"] * tab_in_whitespaces
            do_same_level_as_line_above = lambda : line_above["reindent_with"]

            def do_deep_step():
                """
                here be recalculation of shit
                AAAAAAAAAAAAAAAAAAAAAAAAAA!!!
                - for "weird" lines, we calculate amount of leading whitespace required
                  for keeping relative left margin as close as possible to original.
                """
                pass

            if line_above == None:
                # 1st line "normally indented" by definition
                reindent_with = do_shallow_step()
            elif line["level__abs"] == line_above["level__abs"]:
                # same level, totally
                reindent_with = do_same_level_as_line_above()
            else:
                level_diff = line["level"] - line_above["level"]
                if level_diff < 2:
                    # negatives are out-denting
                    reindent_with = do_shallow_step()
                else:
                    # dramatic jump! someone escaped newlines, lined up
                    #                           shit in consequent lines,
                    # and got way too much creative!
                    reindent_with = do_deep_step()
                    

            line["reindent_with"] = reindent_with
            reindented_line = reindent_with + line["stripped"]
            return reindented_line

        self.wait_for_self_view_to_populate()
        
        # -- tabs->spaces->tabs to deal with in-line "formatting" tabs
        # 1st line of view has None as description of previous line. LOGIKA.
        whole_view = sublime.Region(0, view.size())
        view_content = self.view.substr(whole_view)

        lines__raw = view_content.splitlines()
        lines__parsed = [parse_indentation(l, tab_size__old, tab_size__new) for l in raw_lines]
        lines__reindented = [reindent_line(l, p) for l, p in zip(lines__parsed, [None] + lines__parsed)]

        # -- 1. join reindented lines with view's line end symbol
        # -- 2. replace content
        # -- 3. restore selection

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