amu-python-scripts
==================

My python scripts for automate some practicies or do fancy stuff.

- prime_factor.py - script lists Prime Factor values out from given number
More info about PF: http://en.wikipedia.org/wiki/Prime_factor

- WebPageSaver.py is a web - page image grabber tool's it is partly based on Regular expressions as, 
    parsing HTML page for image URLs and verifying URL format are based on RegEx. 
    In that way it is possible to optimize a bit and keep code more readable. 
Library urllib2 is used for HTTP operations and for get images.
Fetching images from chosen site will create new sub-folder based on domain name (location for pics: So pics are saved under current-dir/images/<domain-name-dir>

- In WxPython/ folder you will found GUI version of string-pair-parser.py
You will need WxPython 3rd party lib for that one and also directory for 
put the tool on work located under the script's location.

- string-pair-parser.py script is made for special use for parsing out "port [Hexadecimal max 32 lenght]" string pairs inside given Directory recursively. Currently it search only indside inform - files. v
It will report on the end all the found matched strings and the number of occurences.
This can be base for some parser which need this kind of functionality.

- I made some basic changes to my GUI version of this dame parser under WxPython/ folder this is under construction but current version have real GUI and user can influence lot more to that what we are parsing. 
For this one you need to have WxPython Lib installed (2.8 version was suitable for Ubuntu 14.04, the 3.0 has some iisues)
Also currently you need to have the UI script and the searchEngine py:s in same folder as the Directory you want to parse.
Change come soon, i will add File - Browser so itrs easy to start the sseartch what ever folder. 
