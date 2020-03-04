# What to do with hard-wrapped lines and logical indentation in non-py files?

E.g., we have a snippet of JS indented with spaces, 4 per level:

```javascript
if (foo 
...,...,...,&& bar
...,...,...,&& quux || zot ) {
...,bring_it_on();
} else {
...,slack_off();
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

Another sample:

```bash
mycommand --option_a --option_b
...,...,...,...,...,...,--option_c 41
...,...,...,...,...,...,--option_d "foo"
...,...,...,...,...,...,file.*
```

Then we to 8-spaces-per-actual-tab and it doesn't look nice at all:

```bash
mycommand --option_a --option_b
\t      \t      \t      \t      \t      \t      --option_c 41
\t      \t      \t      \t      \t      \t      --option_d "foo"
\t      \t      \t      \t      \t      \t      file.*
```
