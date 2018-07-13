% FAQ
% John M. Gabriele

**"Why write another documentation processing program?"**

See the [rationale page](rationale.html).



**"Why use Markdown? Why not LaTeX, reST, moinmoin wiki syntax, etc?"**

The main focus of Rippledoc is to be a very *easy* way to create your
docs and make them available, no manual required. From "zero" to
"docs" in no time flat. Markdown is, IMO, the easiest of the markup
formats to write, to read, and to remember; and
[pandoc-markdown](http://pandoc.org/MANUAL.html#pandocs-markdown)
tastefully adds what's missing from original Markdown.



**"But my favorite language uses {fave-markup}!"**

Documentation often benefits greatly when *others* also contribute to
it. Good writers may not know your markup format of choice, and may
not be interested in taking the time to learn it. But they very likely
already know Markdown (or can [learn it in 5
minutes](quick-markdown-example.html)).



**"But Rippledoc is written in Python! My project uses {other-language}!"**

Rippledoc is a fairly simple program which happens to be written in
Python but which could easily be rewritten in any number of other
languages.

Under the hood, Rippledoc uses [Pandoc](http://johnmacfarlane.net/pandoc/)
to do the heavy lifting. Although Pandoc can translate between various
markup formats, Rippledoc is only using it to convert Markdown to
HTML. There are many other Markdown implementations that you could use
if you wanted to (a bunch are listed at [the Markdown
wiki](http://xbeta.org/wiki/show/Markdown) and the [Markdown Wikipedia
page](http://en.wikipedia.org/wiki/Markdown)), though they might not
have the excellent enhancements that Pandoc provides.



**"Why use Pandoc under the hood? Why not {my-favorite-markdown-implementation}?"**

Because Pandoc:

  * supports tables, definition lists, line blocks, footnotes, and $\LaTeX$ math
  * supports syntax highlighting
  * is high-quality and reliable
  * is actively maintained
  * supports the command-line options that Rippledoc requires
  * runs fast
  * is easy to install on GNU/Linux


**"Bah, my project is hosted on gitlab (or similar); why not just let
users read the docs there, since gitlab automatically renders .md
files as html?"**

Mainly because:

  * Pandoc supports a number of very useful extensions which gitlab's
    markdown processor may not (see previous FAQ item).
  * Rippledoc provides excellent navigation links, and lets you order
    your docs as well.
  * With Rippledoc you can customize styling.


**"Why does Rippledoc process all md files every time I run it?"**

Because Rippledoc figures out prev/next links, and also the links in
the the toc's contain document titles, it's tricky to keep track of
which files need regenerating when a title is changed or a new doc
file is added. So, Rippledoc currently takes the easy way out and
simply regenerates all files every time.


**"I don't like Rippledoc's default output style. Can I change it?"**

Certainly. When you first run Rippledoc, it creates default styles.css
file which you can then modify.
