> /!\\ This is a **work in progress**.  
> If you got a link for this directly from me, report any bugs and quirks using IM or whatever; if not — open issues.


# Normalise Indentation mk2

A plugin to normalise indentation of text files according to your local preferences (including syntax-specific ones).

## Compatibility and possible conflicts

> NB: started as a fork of an abandoned [`Normalize Indentation`](https://github.com/Ennosuke/Normalize-Indentation) plugin, then completely rewrote it — please uninstall old one first, it doesn't work anyway.

Before installing this version, __please remove the [predecessor](https://github.com/Ennosuke/Normalize-Indentation)__, which doesn't work with ST3 anyway. To avoid possible collisions, I used `normalise` instead of `normalize` wherever possible (command itself, menu items, names of configuration files &c).

## Usecase

- you prefer such-and-such indentation (say, tabs w/ 2 spaces per tab);
- you're looking at a file indented _differently_;
- plugin presumes your preferences for indentation of spec. filetypes are reflected in corresponding config files (ST allows you to override on per-syntax basis);
- instead of poking at menus, you press `Ctrl+Alt+I`, *boom!*, problem solved.

## Features

- robust indentation detector by [`AutoSetIndentation`](https://packagecontrol.io/packages/AutoSetIndentation):
    - works with short files (less than 10 lines of code);
    - much smarter with edge cases and weird stuff.
- supports `*.sublime-syntax` in addition to venerable `*.tmLanguage`;
- tries it's best to deal with mixed indentation;

How does it actually work:

1. On file load, AutoSetIndentation detects indentation settings for current file (tabs or spaces, amount of spaces per tab);
2. We combine editor's defaults, general user preferences and syntax specific preferences to figure out what kind of indentation user expects to see in such and such type of file;
3. We convert and adapt file contents so **1** become **2** in most consistent way possible.