---
Title: Markdown Demo
Description: An example page to showcase <i>StuffPages</i>
Author: Florian Krause
Style: styles/default.css
---

**Table of Contents:**

- [Introduction](#introduction)
- [Headers](#headers)
- [Emphasis](#emphasis)
- [Lists](#lists)
- [Links](#links)
- [Images](#images)
- [Code and Syntax Highlighting](#code-and-syntax-highlighting)
- [Tables](#tables)
- [Blockquotes](#blockquotes)
- [Horizontal Rules](#horizontal-rules)
- [Line Breaks](#line-breaks)
- [Footnotes](#footnotes)
- [Definition Lists](#definition-lists)
- [Task Lists](#task-lists)
- [Emoji](#emoji)
- [Inline HTML](#inline-html)
- [Extensions](#extension)


# Introduction

This document has been adatpted from  https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet.


# Headers

```
# H1
## H2
### H3
#### H4
##### H5
###### H6

Alternatively, for H1 and H2, an underline-ish style:

Alt-H1
======

Alt-H2
------
```

# H1
## H2
### H3
#### H4
##### H5
###### H6

Alternatively, for H1 and H2, an underline-ish style:

Alt-H1
======

Alt-H2
------

# Emphasis

```
Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~
```

Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~


# Lists

(In this example, leading and trailing spaces are shown with with dots: ⋅)

```
Ordered list:

1. First ordered list item
2. Another item
⋅⋅* Unordered sub-list.
1. Actual numbers don't matter, just that it's a number
⋅⋅1. Ordered sub-list
4. And another item.

⋅⋅⋅You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown).

⋅⋅⋅To have a line break without a paragraph, you will need to use two trailing spaces.⋅⋅
⋅⋅⋅Note that this line is separate, but within the same paragraph.⋅⋅
⋅⋅⋅(This is contrary to the typical GFM line break behaviour, where trailing spaces are not required.)

Unordered list:

* Unordered list can use asterisks
- Or minuses
+ Or pluses
```

Ordered list:

1. First ordered list item
2. Another item
    * Unordered sub-list.
1. Actual numbers don't matter, just that it's a number
    1. Ordered sub-list
4. And another item.

     You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown).

     To have a line break without a paragraph, you will need to use two trailing spaces.  
     Note that this line is separate, but within the same paragraph.  
     (This is contrary to the typical GFM line break behaviour, where trailing spaces are not required.)

Unordered list:

* Unordered list can use asterisks
- Or minuses
+ Or pluses


# Links

There are two ways to create links.

```
[I'm an inline-style link](https://www.google.com)

[I'm an inline-style link with title](https://www.google.com "Google's Homepage")

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[I'm a relative reference to a repository file](../blob/master/LICENSE)

[You can use numbers for reference-style link definitions][1]

Or leave it empty and use the [link text itself]

Some text to show that the reference links can follow later.

Also, plain URLs are automatically turned into links: http://python.org.

[arbitrary case-insensitive reference text]: https://www.mozilla.org
[1]: http://slashdot.org
[link text itself]: http://www.reddit.com
```

[I'm an inline-style link](https://www.google.com)

[I'm an inline-style link with title](https://www.google.com "Google's Homepage")

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[I'm a relative reference to a repository file](../blob/master/LICENSE)

[You can use numbers for reference-style link definitions][1]

Or leave it empty and use the [link text itself]

Some text to show that the reference links can follow later.

Also, plain URLs are automatically turned into links: http://python.org.

[arbitrary case-insensitive reference text]: https://www.mozilla.org
[1]: http://slashdot.org
[link text itself]: http://www.reddit.com


# Images

```
Here's a logo (hover to see the title text):

Inline-style:
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

Reference-style:
![alt text][logo]

[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"

Large images will be scaled to fit on the screen:

![Testcard](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/FuBK_testcard_vectorized.svg/2000px-FuBK_testcard_vectorized.svg.png)
```

Here's a logo (hover to see the title text):

Inline-style:
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

Reference-style:
![alt text][logo]

[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"

Large images will be scaled to fit on the screen:

![Testcard](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/FuBK_testcard_vectorized.svg/2000px-FuBK_testcard_vectorized.svg.png)


# Code and Syntax Highlighting

Code blocks are part of the Markdown spec, but syntax highlighting isn't. However, many renderers -- like Github's and *StuffPages* -- support syntax highlighting. Which languages are supported and how those language names should be written will vary from renderer to renderer. *StuffPages* supports highlighting for dozens of languages (and not-really-languages, like diffs and HTTP headers); to see the complete list, see [here](http://pygments.org/languages/).

```
Inline `code` has `back-ticks around` it.
```

Inline `code` has `back-ticks around` it.

Blocks of code are either fenced by lines with three back-ticks <code>```</code>, or are indented with four spaces. I recommend only using the fenced code blocks -- they're easier and only they support syntax highlighting.

    ```javascript
    var s = "JavaScript syntax highlighting";
    alert(s);
    ```

    ```python
    s = "Python syntax highlighting"
    print s
    ```

    ```
    No language indicated, so no syntax highlighting.
    But let's throw in a &lt;b&gt;tag&lt;/b&gt;.
    ```

```javascript
var s = "JavaScript syntax highlighting";
alert(s);
```

```python
s = "Python syntax highlighting"
print s
```

```
No language indicated, so no syntax highlighting in Markdown Here (varies on Github).
But let's throw in a <b>tag</b>.
```


# Tables

Tables aren't part of the core Markdown spec, but they are part of GFM and *StuffPages* supports them. They are an easy way of adding tables to your page -- a task that would otherwise require copy-pasting from another application.

```
Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned |  |
| col 2 is      | centered      |    |
| zebra stripes | are neat      |     |

The outer pipes (|) are optional, and you don't need to make the raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3
```

Colons can be used to align columns.

| Tables        | Are           | Cool |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned |  |
| col 2 is      | centered      |    |
| zebra stripes | are neat      |     |

The outer pipes (|) are optional, and you don't need to make the raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3


# Blockquotes

```
> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.
```

> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.


# Horizontal Rules

```
Three or more...

---

Hyphens

***

Asterisks

___

Underscores
```

Three or more...

---

Hyphens

***

Asterisks

___

Underscores


# Line Breaks

My basic recommendation for learning how line breaks work is to experiment and discover -- hit &lt;Enter&gt; once (i.e., insert one newline), then hit it twice (i.e., insert two newlines), see what happens. You'll soon learn to get what you want.

Here are some things to try out:

```
Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.
```

Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also begins a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.

(Technical note: *StuffPages* uses GFM line breaks, so there's no need to use MD's two-space line breaks.)


# Footnotes

```
Footnotes[^1] have a label[^@#$%] and the footnote's content, which can include Markdown itself[^3].

///Footnotes Go Here///

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".
[^3]: 
    The first paragraph of the definition.

    Paragraph two of the definition.

    > A blockquote with
    > multiple lines.

        a code block

    A final paragraph.
```

Footnotes[^1] have a label[^@#$%] and the footnote's content, which can include Markdown itself[^3].

///Footnotes Go Here///

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".
[^3]: 
    The first paragraph of the definition.

    Paragraph two of the definition.

    > A blockquote with
    > multiple lines.

        a code block

    A final paragraph.


# Definition Lists

```
Apple
:   Pomaceous fruit of plants of the genus Malus in 
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.
```

Apple
:   Pomaceous fruit of plants of the genus Malus in 
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.



# Task Lists

- [ ] foo
  - [ ] foo
  - [x] foo
- [x] foo


# Emoji

```
Emojis are very useful :smile: :thumbsup:.

You can also escape `:` characters to escape the emoji: \:smile:.
```

Emojis are very useful :smile: :thumbsup:.

You can also escape `:` characters to escape the emoji: \:smile:.


# Inline HTML


You can also always use raw HTML in your Markdown, and it'll mostly work pretty well.

```
To reboot your computer, press <kbd>ctrl</kbd>+<kbd>alt</kbd>+<kbd>del</kbd>.

Use <sub>sub</sub>sript or <sup>super</sup>script and <u>underline</u> text.

<style>.embed-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; } .embed-container iframe, .embed-container object, .embed-container embed { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }</style><div class='embed-container'><iframe src='https://www.youtube.com/embed/tntOCGkgt98' frameborder='0' allowfullscreen></iframe></div>
```

To reboot your computer, press <kbd>ctrl</kbd>+<kbd>alt</kbd>+<kbd>del</kbd>.

Use <sub>sub</sub>sript or <sup>super</sup>script and <u>underline</u> text.

<style>.embed-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; } .embed-container iframe, .embed-container object, .embed-container embed { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }</style><div class='embed-container'><iframe src='https://www.youtube.com/embed/tntOCGkgt98' frameborder='0' allowfullscreen></iframe></div>


# Extensions

You can also extend *StuffPages* with [Python Markdown extensions](https://pythonhosted.org/Markdown/extensions/index.html). Just install the extensions and add them to `extras` in `config.py`.
