# What to do with hard-wrapped lines and logical indentation in non-py files?

Instead of just collapsing sequences of spaces to tab symbols _globally_, we:

- process file line by line;
- watch for sudden indentation jumps:
    - OK: 1 level, 2 levels, 3 levels
    - WEIRD: 1 level, 4 levels, 3 levels
- we keep track of last non-weird indentation level
- for "weird" lines, we calculate amount of leading whitespace required
  for keeping relative left margin as close as possible to original.

E.g., we have a snippet of JS indented with spaces, 4 per level:

```javascript
if (foo 
............&& bar
............&& quux || zot ) {
....bring_it_on();
} else {
....slack_off();
}
```

After we convert it to tab-indented with 4 tabs per level, it will become this:

```javascript
if (foo 
\t  \t  \t  && bar
\t  \t  \t  && quux || zot ) {
\t  tbring_it_on();
} else {
\t  slack_off();
}
```

Problems start when we try to go from "spaces, 4/level" to "tabs, 8/level"
(notice huge shift to the right on lines 2 & 3):

```javascript
if (foo 
\t      \t      \t      && bar
\t      \t      \t      && quux || zot ) {
\t      bring_it_on();
} else {
\t      slack_off();
}
```