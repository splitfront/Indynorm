# Normalise Indentation mk2

**Work in progress.** If you got a link for this directly from me, report any bugs and quirks using IM or whatever; if not — open issues.

A plugin to normalise indentation of text files according to your local preferences (including syntax-specific ones).

> NB: this is a complete fork/rewrite of an abandoned [`Normalize Indentation`](https://github.com/Ennosuke/Normalize-Indentation) plugin — please uninstall it first.

Usecase: 

- you prefer such-and-such indentation (say, tabs w/ 2 spaces per tab);
- you're looking at a file indented _differently_;
- it makes your brain itch;
- instead of poking at menus, you press `Ctrl+Alt+I`, *boom!*, problem solved.

Features:

- robust indentation detector by [`AutoSetIndentation`](https://packagecontrol.io/packages/AutoSetIndentation):
    - works with short files (less than 10 lines of code);
    - much smarter with edge cases and weird stuff.
- supports `*.sublime-syntax` in addition to venerable `*.tmLanguage`;
- works with mixed space/tab indentation;

## How does it actually work:

1. AutoSetIndentation does its best to detect indentation settings for current file (tabs or spaces, amount of spaces per tab);
2. We combine editor's defaults, general user preferences and syntax specific preferences to figure out what kind of indentation user expects to see in such and such type of file;
3. We convert and adapt file contents so 1 will become 2 in most consistent way possible.

## Compatibility and possible conflicts

Before installing this version, __please remove the predecessor__, which doesn't work with ST3 anyway. To avoid possible collisions, I used `normalise` instead of `normalize` wherever possible (command itself, menu items, names of configuration files &c). 

## TODO:

- [ ] settings from `View > Indentation` shall take precedence over stuff coming from settings files.

## Looking into:

I'm kinda new to ST plugin dev and need to read its documentation first, but m.b.:

- [ ] more granular control: separate commands to normalise to syntax file defaults and user overrides (including `View > Indentation`?);
- [ ] improve ST UI integration:
    - [ ] move menu item to `View > Indentation`;
    - [ ] add menu item to window's `Spaces/Tabs` menu;
- [ ] support per-project and/or per-language preferences (if ST as a platform supports it);
- [ ] find a way to convert indentation onload withouf polluting diffs:
    - `on_open` of `./foobar.quux`, detect indentation and store it in `./.~indentation_state_for_foobar_quux`;
    - `.gitignore` for `./~indentation_state_for_*`;
    - `on_commit` hook to revert files to their old indentation settings according to saved state;
    - looks a bit baroque, but I often find myself looking at kinds of freaky stuff, yet I don't want to pollute diffs with my quirks.