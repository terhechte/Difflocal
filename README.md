# Difflocal

#### Compare "Localizable.strings" files

If you don't use a full fledged localization tool for Cocoa or iOS development, like the [Localization Suite](http://www.loc-suite.org/), then at some point you will have changed your primary localization file (say English.lproj/Localizable.strings) and need to port these additions to your other locales, so that your translators can work on them.

Here, the problem arises that if you generate a new Localizable.strings via

`find -E . -iregex '.*\.(m|h|mm)$' -print0 | xargs -0 genstrings -a -o Resources/en.lproj`

then the order of the keys in the file can change. This makes it very difficult to 'diff' the new locale for changes. 

Difflocal remedies that by comparing two locale files (say your current, updated locale, and the older, unupdated locale) and printing all keys that exist in the one but not in the other.

## Installation:
* Download the file `or` Clone the repository
* Copy difflocal.py into your path (/usr/local/bin, or /usr/bin) or your source directory
* `chmod +x difflocal.py` on the script

## Usage:
difflocal.py Resources/English.lproj/Localizable.strings Resources/de.lproj/Localizable.strings

## Returns:

> Locale is missing key: %i Likes, %i Comments
> 
> Locale is missing key: %i More




