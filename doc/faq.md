% FAQ
% John M. Gabriele

**"Why write another documentation processing program?"**

See the [rationale page](rationale.html).



**"Why use Markdown? Why not LaTeX, reST, moinmoin wiki syntax, etc?"**

The main goal of Rippledoc is to assist in making docs as easy as
possible to create, write, and to contribute to. Aside from probably
being the most widely known, Markdown is, IMO, the easiest of the
markup formats to read, and also very easy to write and to remember;
and [pandoc-markdown](http://pandoc.org/MANUAL.html#pandocs-markdown)
tastefully adds what's missing from original Markdown and/or
[CommonMark](http://commonmark.org/).



**"But my favorite programming language uses {fave-markup}!"**

Documentation often benefits greatly when *others* also contribute to
it. Good writers may not know your markup format of choice, and may
not be interested in taking the time to learn it and the its required
tooling. But they very likely already know Markdown (or can [learn it
in 5 minutes](quick-markdown-example.html)).



**"But Rippledoc is written in Python! My project uses {other-language}!"**

Rippledoc is a fairly simple program which happens to be written in
Python and which could easily be rewritten in any number of other
languages.

Under the hood, Rippledoc uses [Pandoc](http://pandoc.org/) to do the
heavy lifting. Although Pandoc can translate between various markup
formats, Rippledoc is only using it to convert Markdown to HTML. There
are many other Markdown implementations that you could use if you
wanted to (most languages tend to have at least one implementation),
though they might not have the excellent enhancements that Pandoc
provides. See [CommonMark](http://commonmark.org/) for more info on
Markdown and various implementations of it.



**"Why use Pandoc under the hood and not {my-favorite-markdown-implementation}?"**

Because Pandoc:

  * supports tables, definition lists, line blocks, footnotes, and $\LaTeX$ math
  * supports code block syntax highlighting
  * is high-quality and reliable
  * is actively maintained
  * supports the command-line options that Rippledoc requires
  * runs fast
  * is easy to install on GNU/Linux


**"Bah, my project is hosted on GitLab (or similar); why not just let
users read the docs there, since GitLab automatically renders .md
files as html?"**

Mainly because:

  * Pandoc (used by Rippledoc) supports a number of very useful
    Markdown syntax extensions which GitLab's markdown processor may
    not (see previous FAQ item).
  * Rippledoc provides excellent navigation links, a table of
    contents, and lets you order your docs (providing prev/next links).
  * With Rippledoc you can customize styling and more easily incorporate
    your docs into your project's website.


**"Wait. Why use Rippledoc when I can just put up (or enable) a wiki?"**

Because:

  * You usually have to edit wiki content on the web, rather than in
    your text editor. Potential contributors who are skilled writers
    will not want to make substantial doc contributions via a web
    form.
  * Thoughtful writers will often not want to contribute to a wiki,
    since their careful writing can so easily be wrecked-up by a
    heedless hit-and-run editor.
  * Wikis require management (sometimes vigilant management).
    This includes removing spam, but also intervening when editors
    disagree on eachother's changes.
  * Wikis have a way of becoming disorganized while simultaneously
    becoming out of date. And once that happens no one wants to
    touch them.
  * They very likely do not support the nice syntactic markdown
    extensions that Pandoc (used by Rippledoc) does.
  * They provide no nice table of contents nor easy navigation links.
  * If you want to move your docs at some point, it's not always
    easy to extract your doc files from wikis or to migrate to another
    wiki.
  * Changes to the wiki generally are not connected with commits to
    your source code repo.



**"Why does Rippledoc process all md files every time I run it?"**

Because Rippledoc figures out prev/next links, and also the links in
the the toc's contain document titles, it's tricky to keep track of
which files need regenerating when a title is changed or a new doc
file is added, or when a toc.conf is changed. So, Rippledoc currently
takes the easy way out and simply regenerates all files every time.


**"I don't like Rippledoc's default output style. Can I change it?"**

Certainly. When you first run Rippledoc it creates a default
styles.css file which you can then modify.
