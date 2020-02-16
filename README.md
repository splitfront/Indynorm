# Normalise Indentation mk2

A plugin to normalise indentation of text files according to your local preferences (including syntax-specific ones).

> This is a **work in progress**. If you got a link for this directly from me, report any bugs and quirks using IM or whatever; if not — open issues.

> NB: started as a fork of an abandoned [`Normalize Indentation`](https://github.com/Ennosuke/Normalize-Indentation) plugin, then completely rewrote it — please uninstall old one first, it doesn't work anyway.

Usecase: 

- you prefer such-and-such indentation (say, tabs w/ 2 spaces per tab);
- you're looking at a file indented _differently_;
- plugin presumes your preferences for indentation of spec. filetypes are reflected in corresponding config files (ST allows you to override on per-syntax basis);
- instead of poking at menus, you press `Ctrl+Alt+I`, *boom!*, problem solved.

Features:

- robust indentation detector by [`AutoSetIndentation`](https://packagecontrol.io/packages/AutoSetIndentation):
    - works with short files (less than 10 lines of code);
    - much smarter with edge cases and weird stuff.
- supports `*.sublime-syntax` in addition to venerable `*.tmLanguage`;
- tries it's best to deal with mixed indentation;

How does it actually work:

1. On file load, AutoSetIndentation detects indentation settings for current file (tabs or spaces, amount of spaces per tab);
2. We combine editor's defaults, general user preferences and syntax specific preferences to figure out what kind of indentation user expects to see in such and such type of file;
3. We convert and adapt file contents so **1** become **2** in most consistent way possible.

## Compatibility and possible conflicts

Before installing this version, __please remove the predecessor__, which doesn't work with ST3 anyway. To avoid possible collisions, I used `normalise` instead of `normalize` wherever possible (command itself, menu items, names of configuration files &c). 

## TODO:

- [ ] settings from `View > Indentation` shall take precedence over stuff coming from settings files.

## Looking into:

- [ ] more granular control: separate commands to normalise to syntax file defaults and user overrides (including `View > Indentation`?);
    - [ ] By default, `AutoSetIndentation` works `on_load` — so we can just grab user's selection from `View > Indentation` and presume it is most important?
- [ ] improve ST UI integration:
    - [ ] move menu item to `View > Indentation`;
    - [ ] add menu item to window's `Spaces/Tabs` menu;
- [ ] support per-project and/or per-language preferences (if ST as a platform supports it);
- [ ] find a way to convert indentation onload withouf polluting diffs:
    - `on_open` of `./foobar.quux`, detect indentation and store it in `./.~indentation_state_for_foobar_quux`;
    - `.gitignore` for `./~indentation_state_for_*`;
    - `on_commit` hook to revert files to their old indentation settings according to saved state;
    - looks a bit baroque, but I often find myself looking at kinds of freaky stuff, yet I don't want to pollute diffs with my quirks.