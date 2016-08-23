AutoRequire
===========

When you save a file, this plugin automatically destructs libraries into the functions from that library that you're
using in the saved file. You specify what keywords you want destructed in your AutoRequire.sublime-settings file.

Example
-------

AutoRequire.sublime-settings:
````
{
	"auto_require" : [
		{
			"name": "ramda",
			"keywords": ["map", "inc", "filter", "even"]
		}
}
````

MyFile.coffee before file save:
````
{} = require 'ramda' #auto_require:ramda

bigger = map inc, [1,2]
evens = filter even [1,2]
````

MyFile.coffee **after** file save:
````
{map, inc, filter, even} = require 'ramda' #auto_require:ramda

bigger = map inc, [1,2]
evens = filter even [1,2]
````




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

- stop xxxx followed by colon to desctuct, e.g. merge: 
- Make into Package Control
- Enable more than one destruction per file
- Update ramda keywords in AutoRequire.sublime-settings to 0.15.0
