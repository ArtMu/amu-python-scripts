amu-python-scripts
==================

My python scripts for automate some practicies or do fancy stuff.

- prime_factor.py - script lists Prime Factor values out from given number
More info about PF: http://en.wikipedia.org/wiki/Prime_factor

- web_pics_saver.py is a web - page image grabber tool's it is partly based on Regular expressions as, 
    parsing HTML page for image URLs and verifying URL format are based on RegEx. 
    In that way it is possible to optimize a bit and keep code more readable. 
Library urllib2 is used for HTTP operations and for get images.
Fetching images from chosen site will create new sub-folder based on domain name (location for pics: So pics are saved under current-dir/images/<domain-name-dir>.
User gives as argument the web - page from where he/she wants to save the images.

- string-pair-parser.py script is made for special use for parsing out "port [Hexadecimal max 32 lenght]" string pairs inside given Directory recursively. Currently it search only indside inform - files. v
It will report on the end all the found matched strings and the number of occurences.
This can be base for some parser which need this kind of functionality.
You can verify this functionlity by using the file structure I have included in my Repo.

- In StringPairParser/ folder you will found GUI version of next command line version: string-pair-parser.py
You will need WxPython 3rd party lib for that one and also directory for 
put the tool on work located under the script's location.
In this real GUI user can influence lot more what we are parsing than in command line tool. 
For this one you need to have WxPython Lib installed (2.8 version was suitable for Ubuntu 14.04, the 3.0 has some iisues)
