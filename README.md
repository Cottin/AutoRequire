AutoRequire
===========

When you save a file, this plugin automatically destructs libraries into the functions from that library that you're
using in the saved file. You specify what keywords you want destructed in your AutoRequire.sublime-settings file.

Installation
------------

On Mac

````
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
git clone git://github.com/Cottin/AutoRequire
````

On Linux

````
cd ~/.config/sublime-text-3/Packages/
git clone git://github.com/Cottin/AutoRequire
````

On Windows

````
cd %APPDATA%/Sublime Text 3/Packages/
git clone git://github.com/Cottin/AutoRequire
````
TODO
----

- Make into Package Control
- Enable more than one destruction per file
- Update ramda keywords in AutoRequire.sublime-settings to 0.15.0
