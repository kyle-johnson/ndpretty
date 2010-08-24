#!/usr/bin/python
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

import sys
import os
import string

def parseData(data):
    startSearch = 0
    begin = 0
    end = 0
    newline = 0
    newData = []
    
    while 1:
        begin = string.find(data, '<pre>#!', startSearch)
        if begin == -1:
            # nothing found
            break

        end = string.find(data, '</pre>', begin)
        newline = string.find(data, '\n', begin)
        lang = data[begin+7:newline]

        newData.append(data[startSearch:begin])

        original = data[newline+1:end]

        print "Found a chunk of %s" % lang
        #print "====\n", data[newline+1:end], "\n====\n"

        if lang == 'html':
            # NaturalDocs turns < and > into &lt; and &gt;
            # we undo that
            original = string.replace(original, '&lt;', '<')
            original = string.replace(original, '&gt;', '>')
            original = string.replace(original, '&quot;', '"')

        # actual highlighting
        lex = get_lexer_by_name(lang)
        highlighted = highlight(original, lex, HtmlFormatter(noclasses=True, style='colorful'))
        newData.append(highlighted)
        
        startSearch = end+6
    
    # now just need to save the tail
    newData.append(data[startSearch:])
    
    return ''.join(newData)

def main():
    if len(sys.argv) < 2:
        print "You must specify a root documentation directory: ndpretty <documention dir>"
        sys.exit()
    
    if sys.argv[1][0:1] == '/':
        # they gave a full path
        path = os.path.join(sys.argv[1], 'files')
    else:
        # build the path
        path = os.path.join(os.getcwd(), sys.argv[1], 'files')

    if not os.path.exists(path):
        print "The path %s does not exist." % path
        sys.exit()
    else:
        print "parsing files in %s..." % path
    
    for fname in os.listdir(path):
        print "parsing %s..." % fname
        f = open(os.path.join(path, fname), 'r')
        data = parseData(f.read())
        f.close()
        f = open(os.path.join(path, fname), 'w')
        f.write(data)
        f.close()

if __name__ == "__main__":
    main()
    