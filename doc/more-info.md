% More Info
% John Gabriele

Rippledoc is talkative. Just run it and it will tell you if you're
missing something.


What it Expects
===============

Rippledoc has a few rules:

  * All doc files which you'd like Rippledoc to process must be
    Markdown-formatted (see [Pandoc's
    Markdown](http://pandoc.org/MANUAL.html#pandocs-markdown))
    and their filenames must end in ".md". Rippledoc only cares about
    and processes filenames ending in ".md" --- notably, it ignores
    ".txt" files.

  * You must have either an index.md file in your doc directory, or
    else a README.md file in the directory above it. Plus at least one
    other .md file in the doc directory.

  * Your doc files (../README.md too if you're using it in place of
    an index.md here) must begin with a "header block" supplying a
    title, for example:

        % Title for this Doc

    You can also add additional lines to that block for author and
    date (see [Title
    Block](http://pandoc.org/MANUAL.html#extension-pandoc_title_block)).

  * A file named "\_copyright" is required in your doc dir; this is
    how Rippledoc knows it's at the top-level of your docs (in case
    you were to accidentally run it in a subdirectory
    therein). Rippledoc will place the raw html content of \_copyright
    as-is into the footer of every html file it generates. The
    \_copyright file will usually contain something simple like:

    ~~~html
    Copyright <a href="https://www.you.info">Your Name</a>, 2014–2018
    ~~~

Further, Rippledoc:

  * is happy to process nested subdirectories of .md files
  * gleefully ignores directories containing no .md files (for
    example, you might have just a subdirectory of images)



What it Does
============

Rippledoc generates cross-linked html files from your
markdown-formatted doc files. It also generates:

  * a top-level styles.css file (feel free to customize), and
  * default toc.conf files for each directory with any .md files in or
    under it.

A given generated html file resides in the same directory as its
corresponding source .md file (you'll see a link directly to the .md
file in the corresponding html page's footer).

To rearrange the order in which docs are listed in the table of
contents, edit any of the toc.conf files and re-run rippledoc.py.

Either a top-level index.md file, or else a README.md file one
directory above the doc directory, is special and required. It serves
as the "front page" of your documentation. Also, its title (in its
"[title
block](http://pandoc.org/MANUAL.html#extension-pandoc_title_block)")
should be the name of your project --- it will be shown in the header
of every generated page.

<a id="simple-template"/>
As a simple template, you might start each of your docs looking
something like this:

~~~~
% Title Goes Here
% Author Name
% 2018-07

Some text.

An H1 Heading
=============

Some text.

An H2 Heading
-------------

And so on.
~~~~

The title after the "`% `" is what will appear in the table of
contents (except for index.md or ../README.md, the title of which will
be used as the name of your documentation project as a whole).

For more help writing Pandoc's Markdown, see the [Quick Markdown
Example](quick-markdown-example.html).

Once you've got some docs written, you might rsync/ftp/scp your docs
dir to the web to publish them ([as shown
earlier](index.html#quick-usage)).
