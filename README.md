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
