% Rippledoc
% John Gabriele
% 2018-08

**A particularly easy-to-use doc processing tool.**

Find the Rippledoc docs rendered in lovely html at
<http://www.unexpected-vortices.com/sw/rippledoc/index.html>.

Rippledoc is a command-line program that generates easily-navigable
html from a bunch of Markdown-formatted text files (it ripples down
into subdirectories looking for md files). That is, it turns:

~~~
doc/
    index.md
    changes.md
    getting-started.md
    examples/
        ex-1.md
        ex-2.md
~~~

into:

~~~
doc/
    index.md
    index.html
    changes.md
    changes.html
    styles.css # <-- additionally created by Rippledoc
    toc.conf   # <-- additionally created by Rippledoc
    getting-started.md
    getting-started.html
    examples/
        ex-1.md
        ex-1.html
        ex-2.md
        ex-2.html
        toc.conf  # <-- additionally created by Rippledoc
~~~

(You can, optionally, omit the ./index.md file and instead use a
../README.md if you prefer.)

Rippledoc requires nearly zero configuration; you just run it in a
directory containing Markdown-formatted text files (see [more
info](more-info.html) for the few rules you've got to follow) and it
does the rest.

You can find the source located at
<https://gitlab.com/uvtc/rippledoc>.

Under the hood, Rippledoc uses [Pandoc](http://pandoc.org/) to do the
markdown ➞ html conversion.


Purpose
=======

The main goals for Rippledoc are:

  * make it as easy as possible to create and write nice-looking,
    ordered, easily-navigable docs
  * make it as easy as possible for others to contribute to your docs



OS Compatibility
================

The author has not given even a passing thought to running this
program on any OS other than GNU/Linux.



Quick Usage
===========

~~~bash
cd ~/my-project/doc
# Rippledoc needs either a ../README.md or an ./index.md.
# It also needs a _copyright file present, plus at least one
# other doc file.
touch _copyright index.md getting-started.md  # changes.md, ... others?
# Edit those files, then run Rippledoc.
rippledoc.py
~~~

and point your browser to <file:///path/to/my-project/doc/index.html>
to see the results.

> Of course, [this site you're reading
> now](http://www.unexpected-vortices.com/sw/rippledoc/index.html) was
> generated using Rippledoc.

To upload your docs to a server, you might use rsync:

~~~bash
rsync -urv --delete /path/to/your-proj/doc you@remote:public_html/your-proj
~~~

That will put the local `doc` directory into the remote `your-proj`
directory.



License
=======

Copyright 2014–2018 John Gabriele

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
