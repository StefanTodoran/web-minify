#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""JavaScript Minifier functions for CSS-HTML-JS-Minify."""


import re

from io import StringIO  # pure-Python StringIO supports unicode.

from .css_minifier import condense_semicolons


__all__ = ('js_minify', )


def remove_commented_lines(js):
    """Force remove commented out lines from Javascript."""
    result = ""
    for line in js.splitlines():
        line = re.sub(r"/\*.*\*/" ,"" ,line) # (/*COMMENT */)
        
        # line = re.sub(r"//.*","" ,line) # (//COMMENT)
        pattern = r'(?:([^\/"\']|\/\*(?:[^*]|\*+[^*\/])*\*+\/|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')|\/\/.*)'
        line = re.sub(pattern, r'\1', line)

        result += '\n'+line
    return result


def simple_replacer_js(js):
    """Force strip simple replacements from Javascript."""
    return condense_semicolons(js.replace("debugger;", ";").replace(
        ";}", "}").replace("; ", ";").replace(" ;", ";").rstrip("\n;"))


def js_minify_keep_comments(js):
    """Return a minified version of the Javascript string."""
    ins, outs = StringIO(js), StringIO()
    JavascriptMinify(ins, outs).minify()
    return force_single_line_js(outs.getvalue())


def concatenate_shorthand_if_statements(js):
    lines = js.splitlines()
    output = []
    inside_if = False

    for line in lines:
        line = line.strip()

        if line.startswith('if') and not line.endswith('{'):
            inside_if = True
            output.append(line)
        elif inside_if:
            output[-1] += ' ' + line
            if line.endswith(';'):
                inside_if = False
        else:
            output.append(line)

    result = ""
    for line in output:
        result += "\n" + line

    return result


def concatenate_block_clauses(js):
    """
    When typescript is transpiled, sometimes if else statements and try catch blocks are
    written not as:
        if {
            ...
        } else {
            ...
        }
    ...but rather with the else being on the next line from the if statement, meaning:
        if {
            ...
        }
        else {
            ...
        }
    We need to concatenate these lines as putting a semicolon at the end of each line without
    concatenation would result in the else and catch statements breaking.
    """
    lines = js.splitlines()
    i = 0

    while i < len(lines) - 1:
        line = lines[i].strip()
        next_line = lines[i + 1].strip()
        
        if line.endswith("}") and (next_line.startswith("else") or next_line.startswith("catch")):
            lines[i] += " " + next_line
            del lines[i + 1]
        
        i += 1
    
    result = ""
    for line in lines:
        result += "\n" + line

    return result


def concatenate_chained_functions(js):
    """
    Given multiple lines with chained functions, e.g. a .then chain spread over
    multiple lines, concatenates all those lines into one.
    """
    lines = js.splitlines()
    i = 0

    while i < len(lines) - 1:
        line = lines[i].strip()
        next_line = lines[i + 1].strip()

        if not line.endswith(';') and next_line.startswith('.'):
            lines[i] += " " + next_line
            del lines[i + 1]
        else:    
            i += 1

    result = ""
    for line in lines:
        result += "\n" + line

    return result


def force_single_line_js(js):
    """Force Javascript to a single line, even if need to add semicolon."""
    # TODO: This is not ideal. We do want to concatenate everything
    # to a single line. HOWEVER the naive approach of ";".join will break
    # things, such as for example "if" statements without curly braces.
    return ";".join(js.splitlines()) if len(js.splitlines()) > 1 else js


class JavascriptMinify(object):

    """Minify an input stream of Javascript, writing to an output stream."""

    def __init__(self, instream=None, outstream=None):
        """Init class."""
        self.ins, self.outs = instream, outstream

    def minify(self, instream=None, outstream=None):
        """Minify Javascript using StringIO."""
        if instream and outstream:
            self.ins, self.outs = instream, outstream
        write, read = self.outs.write, self.ins.read
        space_strings = ("abcdefghijklmnopqrstuvwxyz"
                         "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$\\")
        starters, enders = '{[(+-', '}])+-"\''
        newlinestart_strings = starters + space_strings
        newlineend_strings = enders + space_strings
        do_newline, do_space = False, False
        doing_single_comment, doing_multi_comment = False, False
        previous_before_comment, in_quote = '', ''
        in_re, quote_buf = False, []
        previous = read(1)
        next1 = read(1)
        if previous == '/':
            if next1 == '/':
                doing_single_comment = True
            elif next1 == '*':
                doing_multi_comment = True
            else:
                write(previous)
        elif not previous:
            return
        elif previous >= '!':
            if previous in "'\"":
                in_quote = previous
            write(previous)
            previous_non_space = previous
        else:
            previous_non_space = ' '
        if not next1:
            return
        while True:
            next2 = read(1)
            if not next2:
                last = next1.strip()
                conditional_1 = (doing_single_comment or doing_multi_comment)
                if not conditional_1 and last not in ('', '/'):
                    write(last)
                break
            if doing_multi_comment:
                if next1 == '*' and next2 == '/':
                    doing_multi_comment = False
                    next2 = read(1)
            elif doing_single_comment:
                if next1 in '\r\n':
                    doing_single_comment = False
                    while next2 in '\r\n':
                        next2 = read(1)
                        if not next2:
                            break
                    if previous_before_comment in ')}]':
                        do_newline = True
                    elif previous_before_comment in space_strings:
                        write('\n')
            elif in_quote:
                quote_buf.append(next1)

                if next1 == in_quote:
                    numslashes = 0
                    for c in reversed(quote_buf[:-1]):
                        if c != '\\':
                            break
                        else:
                            numslashes += 1
                    if numslashes % 2 == 0:
                        in_quote = ''
                        write(''.join(quote_buf))
            elif next1 in '\r\n':
                conditional_2 = previous_non_space in newlineend_strings
                if conditional_2 or previous_non_space > '~':
                    while 1:
                        if next2 < '!':
                            next2 = read(1)
                            if not next2:
                                break
                        else:
                            conditional_3 = next2 in newlinestart_strings
                            if conditional_3 or next2 > '~' or next2 == '/':
                                do_newline = True
                            break
            elif next1 < '!' and not in_re:
                conditional_4 = next2 in space_strings or next2 > '~'
                conditional_5 = previous_non_space in space_strings
                conditional_6 = previous_non_space > '~'
                if (conditional_5 or conditional_6) and (conditional_4):
                    do_space = True
            elif next1 == '/':
                if in_re:
                    if previous != '\\':
                        in_re = False
                    write('/')
                elif next2 == '/':
                    doing_single_comment = True
                    previous_before_comment = previous_non_space
                elif next2 == '*':
                    doing_multi_comment = True
                else:
                    in_re = previous_non_space in '(,=:[?!&|'
                    write('/')
            else:
                if do_space:
                    do_space = False
                    write(' ')
                if do_newline:
                    write('\n')
                    do_newline = False
                write(next1)
                if not in_re and next1 in "'\"":
                    in_quote = next1
                    quote_buf = []
            previous = next1
            next1 = next2
            if previous >= '!':
                previous_non_space = previous


def js_minify(js):
    """Minify a JavaScript string."""
    print("""Future JavaScript support is orphan and not supported!.
          If you want to make ES6, ES7 work feel free to send pull requests.""")
    js = concatenate_shorthand_if_statements(js)
    js = concatenate_block_clauses(js)
    js = concatenate_chained_functions(js)
    js = remove_commented_lines(js)
    js = js_minify_keep_comments(js)
    return js.strip()
