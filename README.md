# Normalise Indentation mk2

A plugin to normalise indentation of text files according to local preferences. 

> NB: this is a remake of abandoned [`Normalize Indentation`](https://github.com/Ennosuke/Normalize-Indentation) plugin — please uninstall it first!

Usecase: 

- you prefer your code space-indented, 2-spaces-per-level of indentation;
- you're looking at a 4-spaces-per-level tab-indented file;
- it makes your brain itch;
- `Ctrl+Alt+Shift+I`, problem solved.

Features:

- _theoretically_, it should work with ST2, but I will not support it;
- added support for `*.sublime-syntax` (in addition to venerable `*.tmLanguage`);
- now correctly works with mixed space/tab indentation.

## Compatibility and possible conflicts

Before installing this version, __please remove the predecessor__, which doesn't work with ST3 anyway. To avoid possible collisions, I used `normalise` instead of `normalize` wherever possible (command itself, menu items, names of configuration files &c). 

## Auto-detection of indentation:

It's not a requirement, but I highly recommend to install [`AutoSetIndentation`](https://packagecontrol.io/packages/AutoSetIndentation):

- it works with short files (less than 10 lines of code);
- it's smarter with edge cases and weird stuff.

## Looking into:

- [ ] add [`AutoSetIndentation`](https://packagecontrol.io/packages/AutoSetIndentation) as a dependency?;
- [ ] "to and fro" conversion (doesn't look like a good idea -- needs a git hook and extra lines in `.gitignore`, but maybe):
    - `Ctrl+Alt+I` sets indentation to personal preference;
    - `Ctrl+Alt+Shift+I` sets it to built-in language standart.
- [ ] move menu item to `View > Indentation`;
- [ ] add menu item to window's `Spaces/Tabs` menu;
- [ ] support per-project/per-language preferences?
