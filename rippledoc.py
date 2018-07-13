#!/usr/bin/env python3

# Copyright 2018 John Gabriele <jgabriele@fastmail.fm>
#
# This file constitutes the Rippledoc program.
#
# Rippledoc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# Rippledoc is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Rippledoc.  If not, see <http://www.gnu.org/licenses/>."

import os, os.path, sys, subprocess, io, re

VERSION = "2018-07-11"

project_name = None
copyright_info = None

dirs_to_skip = []
fnm_to_doc_title = {}
master_toc_list_items = []

# Needed for prev/next links. Does not include dirs.
full_ordered_list_of_fnms = []

def main():
    print(f"================ Rippledoc, version {VERSION} ================")

    if len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print(mlsl("""\
        You run this program in the root (top-level) of your
        documentation directory to generate easily-navigable HTML files
        from your (pandoc-)markdown-formatted doc files. For more info,
        see the docs this program came with, or else its docs online at
        <http://www.unexpected-vortices.com/sw/rippledoc/index.html>.

        Usage:

            rippledoc.py
            rippledoc.py -h|--help

        To remove all traces of this program having been used in your docs
        directory, delete:

          * all toc.conf files
          * all toc.md files
          * the styles.css and _copyright files
          * all generated .html files

        Exiting.
        """))
        sys.exit(0)

    if not os.path.exists("index.md"):
        print(mlsl("""\
        [**] Unable to find an "index.md" file here. Please make
        [**] sure you're running this program in the root (top-level)
        [**] of your doc directory, and that there's an index.md file
        [**] present here. Exiting.
        """))
        sys.exit(0)

    global project_name
    project_name = get_title_from('./index.md')
    print(f"""Generating docs for "{project_name}" ...""")

    if not os.path.exists("_copyright"):
        print(mlsl("""\
        [**] Unable to find a "_copyright" file here. Please make
        [**] sure you're running this program in the root (top-level)
        [**] of your doc directory, and that there's a _copyright file
        [**] present here. This file typically contains something like:
        [**]
        [**]     Copyright 2018 Moe Ghoul
        [**]
        [**] (including raw HTML is ok too). Exiting.
        """))
        sys.exit(0)

    global copyright_info
    copyright_info = io.open("_copyright").read().strip()

    if not os.path.exists("styles.css"):
        print("""Didn't find a styles.css file here. Creating one...""")
        with io.open("styles.css", "w") as sty_file:
            sty_file.write(styles_default_css_content)

    print("Checking file and directory names for weirdness...")
    check_file_and_dir_names()

    print("Noting any dirs to skip (i.e., those with no .md files in or below them)...")
    # These may be dirs containing only image files or what have you.
    populate_dirs_to_skip(".")
    if dirs_to_skip:
        for dir_to_skip in dirs_to_skip:
            print(f"  * Will skip {dir_to_skip}.")

    # full filename --> doc title (from first line of md file)
    print("Recording each md file's doc title...")
    populate_fnm_to_doc_title()

    print("Checking toc.conf files...")
    process_dirs_create_toc_conf_files()

    print("Reading in all toc.conf data...")
    populate_full_ordered_list_of_fnms('.')

    print("Generating toc.md files...")
    create_master_toc_md_file()
    create_other_toc_md_files()

    print("Transmogrifying .md files into html files...")
    process_all_md_files()

    print("Done.")


# ================================================================
# Multi-Line Strip Left. Strips off number of spaces of
# the first line of `s` (which is a multi-line string).
def mlsl(s):
    lines = s.splitlines()
    spaces_to_remove = len(lines[0]) - len(lines[0].lstrip())
    out = []
    for line in lines:
        out.append(
            line.replace(' ' * spaces_to_remove, '', 1))
    return "\n".join(out)


def get_title_from_doc(fnm):
    lines = io.open(fnm).readlines()
    if not lines:
        print(mlsl(f"""\
        [**] Found {fnm} but it's empty. Please add a title to it
        [**] and some content as well. Exiting.
        """))
        sys.exit(0)
    line = lines[0]
    if not line.startswith("% "):
        print(mlsl(f"""\
        [**] The first line of "{fnm}", doesn't start with "% ",
        [**] (indicating its title) as any well-formatted pandoc-markdown
        [**] file should. Please check it out. Exiting.
        """))
        sys.exit(0)
    title = line[1:].strip()
    return title


def check_file_and_dir_names():
    r1 = re.compile(r'[\w\./-]+$')
    msg = mlsl("""\
    [**] Should only contain letters, numbers, underscores, and
    [**] dashes (no spaces). Please have a look. Exiting.
    """)
    for (this_dir, dirs_here, files_here) in os.walk('.'):
        if not r1.match(this_dir):
            print(mlsl(f"""\
            [**] Don't like the look of the dir name "{this_dir}".
            {msg}
            """))
            sys.exit()
        for d in dirs_here:
            if not r1.match(d):
                print(mlsl(f"""\
                [**] Don't like the look of the dir name "{os.path.join(this_dir, d)}."
                {msg}
                """))
                sys.exit()
        for fnm in files_here:
            if not r1.match(fnm):
                print(mlsl(f"""\
                [**] Don't like the look of the file name "{os.path.join(this_dir, fnm)}".
                {msg}
                """))
                sys.exit()


def populate_dirs_to_skip(path):
    if is_any_mds_here_or_below(path):
        # If there are, we need to dig deeper and keep looking
        # for subdirs that may have no md files below them.
        for p in list_dirs_here(path):
            populate_dirs_to_skip(p)
    else:
        dirs_to_skip.append(path)


def is_any_mds_here_or_below(path):
    for (this_dir, dirs_here, files_here) in os.walk(path):
        for fnm in files_here:
            if fnm.endswith('.md'):
                return True
    return False


# Returns full path names.
def list_dirs_here(pth):
    res = []
    for p in os.listdir(pth):
        full_path = os.path.join(pth, p)
        if os.path.isdir(full_path):
            res.append(full_path)
    return res


def populate_fnm_to_doc_title():
    for (this_dir, dirs_here, files_here) in os.walk('.'):
        for fnm in [f for f in files_here if f.endswith('.md')]:
            full_fnm = os.path.join(this_dir, fnm)
            title = get_title_from(full_fnm)
            fnm_to_doc_title[full_fnm] = title


def get_title_from(fnm):
    line = None
    with io.open(fnm) as f:
        line = f.readline()
    if not line or not line.startswith('% '):
        print(mlsl(f"""\
        [**] Problem with {fnm}. It doesn't appear to have a
        [**] title (as in, "% Some Title" as its first line). Please
        [**] remedy the situation. Exiting.
        """))
        sys.exit()
    return line[2:].strip()


def process_dirs_create_toc_conf_files():
    for (this_dir, dirs_here, files_here) in os.walk('.'):
        toc_fnm = os.path.join(this_dir, 'toc.conf')
        md_fnms = [fnm for fnm in files_here if fnm.endswith('.md')]
        if 'toc.md' in md_fnms:
            md_fnms.remove('toc.md')
        if this_dir == '.':
            md_fnms.remove('index.md')
        dirs_here_for_toc = [d for d in dirs_here if os.path.join(this_dir, d) not in dirs_to_skip]
        if is_at_or_under_skipped_dir(this_dir):
            if os.path.exists(toc_fnm):
                print(f"  * Found a derelict toc.conf file in {this_dir}. Removing it.")
                os.remove(toc_fnm)
            continue
        if os.path.exists(toc_fnm):
            # Check that its contents match what's actually here.
            toc_conf_content = io.open(os.path.join(this_dir, 'toc.conf')).read().strip().splitlines()
            s_toc = set(toc_conf_content)
            s_found = set(md_fnms + dirs_here_for_toc)
            s_extra = s_found - s_toc
            if s_extra:
                print(f'''In {this_dir}, items were found that were absent from {toc_fnm}:''')
                for item in s_extra:
                    print(f'  * Adding {item} to the toc.conf.')
                with io.open(toc_fnm, 'a') as f:
                    f.write('\n'.join(list(s_extra)) + '\n')
            s_extra = s_toc - s_found
            if s_extra:
                print(f'''[**] {toc_fnm} contains items that aren't in {this_dir}:''')
                for item in s_extra:
                    print(f'[**]   * {item}')
                print(f'''[**] Please rectify. Exiting.\n''')
                sys.exit()
        else:
            print(f'''  * Didn't find "{toc_fnm}". Creating it ...''')
            with io.open(toc_fnm, 'w') as f:
                f.write('\n'.join(md_fnms + dirs_here_for_toc))
                f.write('\n')


def is_at_or_under_skipped_dir(tgt):
    # Checks if the target dir `tgt` is the same as or under any
    # of the dirs in `dirs_to_skip`.
    for d in dirs_to_skip:
        if d in tgt:
            return True
    return False


def populate_full_ordered_list_of_fnms(path):
    # `path` is a directory name, typically started off like
    # `populate_full_ordered_list_of_fnms('.')`. We call this function
    # after all toc.conf files have been created/checked, so we assume
    # all paths passed in are good ones (with a toc.conf file in them).
    if path == '.':
        full_ordered_list_of_fnms.append('./index.md')
    with io.open(os.path.join(path, 'toc.conf')) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            line = os.path.join(path, line)
            if line.endswith('.md'):
                full_ordered_list_of_fnms.append(line)
            else:
                populate_full_ordered_list_of_fnms(line)


def create_master_toc_md_file():
    populate_master_toc_list_items('.')
    with io.open('toc.md', 'w') as f:
        f.write('% Table of Contents\n\n')
        f.write('\n'.join(master_toc_list_items))
        f.write('\n')


def populate_master_toc_list_items(d):
    toc_fnm = os.path.join(d, 'toc.conf')
    depth = toc_fnm.count('/') - 1
    indent = '    ' * depth
    with io.open(toc_fnm) as f:
        for line in f:
            line = line.strip()
            if line.endswith('.md'):
                md_path = os.path.join(d, line)
                title = fnm_to_doc_title[md_path]
                ht_path = md_path[:-2] + 'html'
                master_toc_list_items.append(f"""{indent}  * [{title}]({ht_path})""")
            else:
                d_path = os.path.join(d, line)
                ht_path = os.path.join(d_path, 'toc.html')
                master_toc_list_items.append(f"""{indent}  * [{line}/]({ht_path})""")
                populate_master_toc_list_items(d_path)


def create_other_toc_md_files():
    for (this_dir, dirs_here, files_here) in os.walk('.'):
        if 'toc.conf' in files_here and this_dir != '.':
            fnms = io.open(os.path.join(this_dir, 'toc.conf')).read().splitlines()
            with io.open(os.path.join(this_dir, 'toc.md'), 'w') as f:
                f.write(f'% Contents of {this_dir}\n\n')
                for fnm in fnms:
                    if fnm.endswith('.md'):
                        html_fnm = fnm[:-2] + 'html'
                        doc_title = fnm_to_doc_title[os.path.join(this_dir, fnm)]
                        f.write('  * [' + doc_title + '](' + html_fnm + ')\n')
                    else:
                        f.write('  * [' + fnm + '/](' + fnm + '/toc.html)\n')
                f.write('\n')


def process_all_md_files():
    for (this_dir, dirs_here, files_here) in os.walk('.'):
        md_fnms = [f for f in files_here if f.endswith('.md')]
        for md_fnm in md_fnms:
            pandoc_process_file(os.path.join(this_dir, md_fnm))


def pandoc_process_file(md_fnm):
    html_fnm = md_fnm[:-2] + 'html'

    # Get the header and footer files ready, for this particular md_fnm.
    depth = md_fnm.count('/') - 1

    html_bef = html_before.replace('{{path-to-index}}', '../' * depth + 'index.html')
    html_bef = html_bef.replace('{{project-name}}', project_name)

    nav_bar_content = get_nav_bar_content(md_fnm)
    html_bef = html_bef.replace('{{nav-bar-content}}', nav_bar_content)

    html_aft = html_after.replace('{{nav-bar-content}}', nav_bar_content)
    html_aft = html_aft.replace('{{copyright-info}}', copyright_info)
    html_aft = html_aft.replace('{{link-to-this-page-md}}', os.path.basename(md_fnm))

    io.open('/tmp/before.html', 'w').write(html_bef)
    io.open('/tmp/after.html' , 'w').write(html_aft)

    pandoc_cmd = ['pandoc', md_fnm]
    pandoc_cmd.extend(['-f', 'markdown+smart', '-s', '--toc', '--mathjax'])
    depth = md_fnm.count('/') - 1
    pandoc_cmd.append('--css=' + '../' * depth + 'styles.css')
    pandoc_cmd.extend(['-B', '/tmp/before.html', '-A', '/tmp/after.html'])
    pandoc_cmd.extend(['-o', html_fnm])
    subprocess.check_call(pandoc_cmd)


def get_nav_bar_content(md_fnm):
    pr, nx = make_prev_next_links(md_fnm)
    toc = make_master_toc_link(md_fnm)
    ht_path = make_linked_html_path(md_fnm)
    space = '&nbsp;&nbsp;&nbsp;'
    nav_bar = f"""{pr} | {nx} {space} {toc} {space} {ht_path}"""
    return nav_bar


def make_prev_next_links(md_fnm):
    idx = None
    prev_text, next_text = '←prev', 'next→'
    prev_link, next_link = prev_text, next_text
    if not md_fnm.endswith('/toc.md'):
        idx = full_ordered_list_of_fnms.index(md_fnm)
        if idx > 0:
            md_fnm_prev = full_ordered_list_of_fnms[idx - 1]
            rel_path_md = get_rel_path_from_to(md_fnm, md_fnm_prev)
            rel_path_html = rel_path_md[:-2] + 'html'
            prev_link = f"""<a href="{rel_path_html}">{prev_text}</a>"""
        if idx < len(full_ordered_list_of_fnms) - 1:
            md_fnm_next = full_ordered_list_of_fnms[idx + 1]
            rel_path_md = get_rel_path_from_to(md_fnm, md_fnm_next)
            rel_path_html = rel_path_md[:-2] + 'html'
            next_link = f"""<a href="{rel_path_html}">{next_text}</a>"""
    return prev_link, next_link


def make_master_toc_link(md_fnm):
    depth = md_fnm.count('/') - 1
    toc_link = None
    toc_string = 'Table of Contents'
    if md_fnm == './toc.md':
        toc_link = toc_string
    else:
        toc_link = f"""<a href="{'../' * depth + 'toc.html'}">{toc_string}</a>"""
    return toc_link


def make_linked_html_path(md_fnm):
    idx = None
    depth = md_fnm.count('/') - 1 # the depth we're at right now for this page
    html_fnm = md_fnm[:-2] + 'html'
    pieces = html_fnm.split('/')[1:] # drop the '.' for now
    tmp_piece = pieces.pop()  # the relative filename at the end
    res = []
    pieces.reverse()
    for i, dr in enumerate(pieces):
        if tmp_piece == 'toc.html' and i == 0:
            res.append(dr)
        else:
            res.append(f"""<a href="{'../' * i + 'toc.html'}">{dr}</a>""")
    res.append('.')
    res.reverse()
    res.append(tmp_piece)
    return 'Current page: ' + '/'.join(res)


def get_rel_path_from_to(fr, to):
    if os.path.dirname(fr) == os.path.dirname(to):
        return os.path.basename(to)
    else:
        depth = fr.count('/') - 1
        return '../' * depth + to


html_before = """
<div id="main-outer-box">

<div id="my-header">
  <a href="{{path-to-index}}">{{project-name}}</a>
</div>

<div id="header-nav-bar">
{{nav-bar-content}}
</div>

<div id="content">

"""

html_after = """
</div> <!-- content -->

<div id="footer-nav-bar">
{{nav-bar-content}}
</div>

<div id="my-footer">
{{copyright-info}}<br/>
<a href="{{link-to-this-page-md}}">Pandoc-Markdown source for this page</a><br/>
(Docs processed by
<a href="http://www.unexpected-vortices.com/sw/rippledoc/index.html">Rippledoc</a>.)
</div> <!-- my-footer -->

</div> <!-- main-outer-box -->

"""

styles_default_css_content = """\
body {
    color: #222;
    line-height: 140%;
    font-family: sans-serif;
    background-color: #fff;
}

#main-outer-box {
    /* Contains all other divs for the page. */
}

#my-header {
    font-weight: bold;
    font-size: large;
    padding: 4px 10px 10px 10px;
    border-bottom: 1px solid #ddd;
}

#my-header a {
    text-decoration: none;
}

#header-nav-bar, #footer-nav-bar {
    background-color: #eee;
    font-size: small;
}

/* Pandoc automatically puts title, subtitle, author, and date
   into a header elem at the top of the page. */
header .author { display: none; }
header .date   { display: none; }

/* Pandoc's doc-specific ToC. */
nav#TOC {
    background-color: #e5efdf;
    border: 1px solid #cedec4;
}

#header-nav-bar {
    padding: 6px 6px 8px 10px;
}

#footer-nav-bar {
    padding: 6px 6px 10px 10px;
}

#content {
    padding: 20px;
    background-color: #fff;
    border-top: 1px solid #ddd;
    border-bottom: 1px solid #ddd;
}

caption {
    font-style: italic;
    font-size: small;
    color: #555;
}

a:link {
    color: #3A4089;
}

a:visited {
    color: #875098;
}

table {
    background-color: #eee;
    padding-left: 2px;
    border: 2px solid #d4d4d4;
    border-collapse: collapse;
}

th {
    background-color: #d4d4d4;
    padding-right: 4px;
}

tr, td, th {
    border: 2px solid #d4d4d4;
    padding-left: 4px;
    padding-right: 4px;
}

dt {
    font-weight: bold;
}

code {
    background-color: #eee;
}

pre {
    line-height: 135%;
    background-color: #eee;
    border: 1px solid #ddd;
    padding-left: 6px;
    padding-right: 2px;
    padding-bottom: 5px;
    padding-top: 5px;
}

blockquote {
    background-color: #d8deea;
    border: 1px solid #c6d1e7;
    border-radius: 6px;
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 16px;
    padding-right: 16px;
}

blockquote code, blockquote pre {
    background-color: #cad2e4;
    border-style: none;
}

#my-footer {
    clear: both;
    padding: 10px;
    font-style: italic;
    font-size: x-small;
    border-top: 1px solid #ddd;
}

h1, h2, h3, h4, h5, h6 {
    font-family: sans-serif;
}

h3, h5 {
    font-style: italic;
}
"""

# -----------------------------------
main()
