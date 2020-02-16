# Normalise Indentation mk2

A plugin to normalise indentation of text files according to local preferences. 

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

## Compatibility and possible conflicts

Before installing this version, __please remove the predecessor__, which doesn't work with ST3 anyway. To avoid possible collisions, I used `normalise` instead of `normalize` wherever possible (command itself, menu items, names of configuration files &c). 

## Looking into:

I'm kinda new to ST plugin dev and need to read it's documentation first, but maybe I should:

- [ ] test for compatibility with ST2.
- [ ] implement "to and fro" conversion (doesn't look like a good idea — needs a git hook and extra lines in `.gitignore`, but maybe):
    - `on_open` of `./foobar.quux`, detect indentation and store it in `./~indentation_state_for_foobar_quux`;
    - `.gitignore` for `./~indentation_state_for_*`;
    - `on_commit` hook to revert files to their old indentation settings according to saved state;
    - looks a bit baroque, but I often find myself looking at kinds of freaky stuff, yet I don't want to pollute diffs with my quirks.
- [ ] add more granular control:
    - `Ctrl+Alt+I` sets indentation to personal preference;
    - `Ctrl+Alt+Shift+I` sets it to built-in language standart.
- [ ] improve ST UI integration:
    - [ ] move menu item to `View > Indentation`;
    - [ ] add menu item to window's `Spaces/Tabs` menu;
- [ ] support per-project \* per-language preferences (if ST as a platform supports it);