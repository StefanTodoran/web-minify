# css-html-js-minify

Async single-file cross-platform no-dependencies minifier for web projects. Includes updates compared to fork, mostly minor bug fixes or optimizations, as well as more extensive test suite. 

[![GPL License](http://img.shields.io/badge/license-GPL-blue.svg?style=plastic)](http://opensource.org/licenses/GPL-3.0) [![LGPL License](http://img.shields.io/badge/license-LGPL-blue.svg?style=plastic)](http://opensource.org/licenses/LGPL-3.0) [![Python Version](https://img.shields.io/badge/Python-3-brightgreen.svg?style=plastic)](http://python.org)

TODO: replace this
https://pypi.python.org/pypi/css-html-js-minify

```shell
css-html-js-minify.py --help

usage: css-html-js-minify.py [-h] [--version] [--wrap] [--prefix PREFIX]
                             [--timestamp] [--quiet] [--hash] [--zipy]
                             [--sort] [--comments] [--overwrite]
                             [--after AFTER] [--before BEFORE] [--watch]
                             [--multiple] [--beep]
                             fullpath

CSS-HTML-JS-Minify. StandAlone Async cross-platform Unicode-ready Python3-ready Minifier for the Web.

positional arguments:
  fullpath         Full path to local file or folder.

optional arguments:
  -h, --help       show this help message and exit
  --version        show programs version number and exit
  --wrap           Wrap output to ~80 chars per line, CSS only.
  --prefix PREFIX  Prefix string to prepend on output filenames.
  --timestamp      Add a Time Stamp on all CSS/JS output files.
  --quiet          Quiet, Silent, force disable all logging.
  --hash           Add SHA1 HEX-Digest 11chars Hash to Filenames.
  --zipy           GZIP Minified files as '*.gz', CSS/JS only.
  --sort           Alphabetically Sort CSS Properties, CSS only.
  --comments       Keep comments, CSS/HTML only (Not Recommended)
  --overwrite      Force overwrite all in-place (Not Recommended)
  --after AFTER    Command to execute after run (Experimental).
  --before BEFORE  Command to execute before run (Experimental).
  --watch          Re-Compress if file changes (Experimental).
  --multiple       Allow Multiple instances (Not Recommended).

CSS-HTML-JS-Minify: Takes a file or folder full path string and process all
CSS/HTML/JS found. If argument is not file/folder will fail. Check Updates
works on Python3. Std-In to Std-Out is deprecated since it may fail with
unicode characters. SHA1 HEX-Digest 11 Chars Hash on Filenames is used for
Server Cache. CSS Properties are Alpha-Sorted, to help spot cloned ones,
Selectors not. Watch works for whole folders, with minimum of ~60 Secs between
runs.
```

- Takes a full path to anything, a file or a folder, then parse, optimize and compress for Production.
- If full path is a folder with multiple files it will use Async Multiprocessing.
- Pretty-Printed colored Logging to Standard Output and Log File on OS Temporary Folder.
- Set its own Process name and show up on Process lists.
- Can check for updates for itself.
- Full Unicode/UTF-8 support.
- Smooth CPU usage, Single Instance Checking.
- Can Obfuscate, GZIP and Hash files, also Watch for changes on files.
- Can execute arbitrary commands after and before running.
- `*.css` files are saved as `*.min.css`, `*.js` are saved as `*.min.js`, `*.htm` are saved as `*.html`

# Command-line usage

```bash
css-html-js-minify.py file.htm

css-html-js-minify.py file.css

css-html-js-minify.py file.js

css-html-js-minify.py /project/static/
```

# Python code usage

```python
from css_html_js_minify import process_single_html_file, process_single_js_file, process_single_css_file, html_minify, js_minify, css_minify

process_single_html_file('test.htm', overwrite=False)
# 'test.html'
process_single_js_file('test.js', overwrite=False)
# 'test.min.js'
process_single_css_file('test.css', overwrite=False)
# 'test.min.css'

html_minify('  <p>yolo<a  href="/" >o </a >     <!-- hello --></p>')
# '<p>yolo<a href="/" >o </a > </p>'
js_minify('var i = 1; i += 2 ;\n alert( "hello  "  ); //hi')
# 'var i=1;i+=2;alert("hello  ");'
css_minify('body {width: 50px;}\np {margin-top: 1em;/* hi */  }', comments=False)
# '@charset utf-8;body{width:50px}p{margin-top:1em}'
```

The optional arguments that these functions take are almost the same as the command-line flags.
Check the list above *(just use add_hash instead of hash)*. Additionally, you can force a specific path for the output files using ``output_path``.


# Install

```
pip install css-html-js-minify
```
Uninstall `pip uninstall css-html-js-minify`


# Why?

**Why another Compressor?**
- There are lots of compressors for web files out there! *Or maybe not?*.
- Many of them only work inside Django/Flask, or frameworks of PHP/Java/Ruby, or can not process whole folders.
- Many are broken or no longer supported, sometimes due to dependency issues

# Migration

To keep things simple [KISS](http://en.wikipedia.org/wiki/KISS_principle), the human readable indented commented hackable HTML is kept as `*.htm` and the compressed production-ready as `*.html`. This is inspired from JavaScript/CSS `*.min.js` and `*.min.css`. [We did not "invent" this file extension.](http://en.wikipedia.org/wiki/HTM)

To migrate from typical file extension HTML to HTM, which is the exactly same, you can run this:

```shell
find . -name "*.html" -exec rename "s/.html/.htm/" "{}" \;
```

This will make a copy of all `*.html` renaming them as `*.htm` recursively from the current folder. Nothing deleted.


# Requisites

- [Python 3.6+](https://www.python.org "Python Homepage")


# Coding Style Guide

- Lint, [PEP-8](https://www.python.org/dev/peps/pep-0008), [PEP-257](https://www.python.org/dev/peps/pep-0257), [iSort](https://github.com/timothycrosley/isort) must Pass Ok. `pip install pep8 isort`
- If there are any kind of tests, they must pass. No tests is also acceptable, but having tests is better.


# JavaScript support

- ES6 and ES7 and future standards may not be fully supported since they change quickly, mainly driven by Node.JS releases.
- Future JavaScript support is orphan, if you want to make ES6, ES7 work feel free to send pull request, we will merge it.


# Licence

- GNU GPL and GNU LGPL and MIT.

This work is free software:
You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This work is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this work.


# Example



<details>

<summary><b>Input CSS</b></summary>

```css
/*!
 * preserve commment
 */


/* delete comment */
.class, #NotHex, input[type="text"], a:hover  {
    font-family : Helvetica Neue, Arial, Helvetica, 'Liberation Sans', sans-serif;
    border: none;
    margin: 0 0 0 0;
    border-color:    fuchsia;
    color:           mediumspringgreen;
    background-position:0 0;;
    transform-origin:0 0;
    margin: 0px !important;
    font-weight :bold;
    color: rgb( 255, 255, 255 );
    padding : 0.9px;
    position : absolute;
    z-index : 100000;
    color: #000000;
    background-color: #FFFFFF;
    background-image: url("data:image/jpeg;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=");
;}
;;

```

</details>

<details>

<summary><b>Uglify (NodeJS):</b> (474 Bytes, 0.189 Secs)</summary>

```css
/* * preserve commment */ .class,#NotHex,input[type="text"],a:hover {font-family:Helvetica Neue,Arial,Helvetica,'Liberation Sans',sans-serif;border:0;margin:0;border-color:fuchsia;color:mediumspringgreen;background-position:0 0;transform-origin:0 0;margin:0 !important;font-weight:bold;color:#fff;padding:.9px;position:absolute;z-index:100000;color:#000;background-color:#fff;background-image:url("data:image/jpeg;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=")};
```

</details>

<details>

<summary><b>css-html-js-minify (Python3):</b> (469 Bytes, 0.010 Secs)</summary>

```css
/*!* preserve commment */ .class,#NotHex,input[type=text],a:hover{font-family:Helvetica Neue,Arial,Helvetica,'Liberation Sans',sans-serif;border:0;margin:0;border-color:#f0f;color:#00fa9a;background-position:0 0;transform-origin:0 0;margin:0 !important;font-weight:700;color:#fff;padding:.9px;position:absolute;z-index:100000;color:#000;background-color:#FFF;background-image:url(data:image/jpg;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=)}
```

</details>