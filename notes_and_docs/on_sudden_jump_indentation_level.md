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

```
001|if (foo 
002|............&& bar
003|............&& quux || zot ) {
004|....bring_it_on();
005|} else {
006|....slack_off();
007|}
```

After we convert it to tab-indented with 4 tabs per level, it will become this:

```
001|if (foo 
002|\t  \t  \t  && bar
003|\t  \t  \t  && quux || zot ) {
004|\t  tbring_it_on();
005|} else {
006|\t  slack_off();
007|}
```

Problems start when we try to go from "spaces, 4/level" to "tabs, 8/level"
(notice huge shift to the right on lines 2 & 3):

```
001|if (foo 
002|\t      \t      \t      && bar
003|\t      \t      \t      && quux || zot ) {
004|\t      bring_it_on();
005|} else {
006|\t      slack_off();
007|}
```