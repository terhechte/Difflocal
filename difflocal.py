#!/usr/bin/env python
import codecs
import optparse
import os
import re

"""
This small script compares Cocoa / iOS development Localizable.strings files.
These are usually UTF-16 and difficult to compare. In addition to that,
the order of the contents of the files varies per export, making diff very
difficult. This script reads all keys and compares them unrelated of order

It is based on diffstrings.py
(https://raw.github.com/facebook/three20/master/diffstrings.py)
but far easier. diffstrings does all kinds of fancy things like reading
an xcode project, and whatnot. I really just wanted to compare to .strings
files.
"""

# the default local file if no options are provided
default_localfile = "English.lproj/Localizable.strings"

# the default other file if no options are provided
default_otherfile = "languages/resources/de.lproj/Localizable.strings"


def openWithProperEncoding(path):
    if not os.path.isfile(path):
        return []

    try:
        f = codecs.open(path, 'r', 'utf-16')
        lines = f.read().splitlines()
        f.close()
    except UnicodeError:
        f = codecs.open(path, 'r', 'utf-8')
        lines = f.read().splitlines()
        f.close()

    return lines


def findKeys(path):
    reString = re.compile(r'\s*"((\\.|.)+?)"\s*=\s*"(.+?)";')
    keys = []
    keyTable = {}
    for line in openWithProperEncoding(path):
        m = reString.search(line)
        if m:
            source = m.groups()[0]
            keys.append(source)
            keyTable[source] = line
    return (keys, keyTable)


def compareKeysForLocals(lc1, lc2, detailed=False):
    def missingKeys(k1, k2):
        for key in k1:
            if not key in k2:
                yield key

    keys1, keyTable1 = findKeys(lc1)
    keys2, keyTable2 = findKeys(lc2)

    # first print the entries
    for key in missingKeys(keys1, keys2):
            print "Missing: %s" % (key,)

    # second print the detailed rows
    if detailed:
        print "----------------------------------------"
        for key in missingKeys(keys1, keys2):
            print keyTable1.get(key)


def parseOptions():
    usage = """usage: %prog [options]

    difflocal commpares two local files: your primary local that contains all the additions from your work on the project, and another local which doesn't contain the additions yet.

    It will compare the two files and list all the additions. The arguments are the paths of the two Localizable.strings files."""
    parser = optparse.OptionParser(usage)
    parser.set_defaults(originalLocaleFile=default_localfile,
                        otherLocalFile=default_otherfile, detailed=False)

    parser.add_option("-l", "--originalLocaleFile", dest="originalLocaleFile", type="str",
        help = "The filename of your source locale.  The default is 'en'.")

    parser.add_option("-o", "--otherLocalFile", dest="otherLocalFile", type="str",
        help = "The filename of the other locale to operate on")
    
    parser.add_option("-d", "--detailed", dest="detailed", type="int",
        help = "Should the script also print the complete missing line")

    options, arguments = parser.parse_args()

    return options


def main():
    options = parseOptions()

    if options.originalLocaleFile and options.otherLocalFile:
        compareKeysForLocals(options.originalLocaleFile,
                             options.otherLocalFile,
                            options.detailed)

if __name__ == "__main__":
    main()
