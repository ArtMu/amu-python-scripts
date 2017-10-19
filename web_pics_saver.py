#!/usr/bin/env python
#
# Arto M 08.09.2014
# Implemented with Python Version: 2.7.6 on Ubuntu OS.
# Verified with windows 7 also, there shouldn't be any major problems.
# 
# This Web - page image grabber tool's is partly based on Regular expressions, 
#    parsing HTML page for image URLs and verifying URL format are based on RegEx. 
#    In that way it is possible to optimize a bit and keep code more readable. 
# Library urllib2 is used for HTTP operations and for get images.
# Fetching images from chosen site will create new sub-folder based on domain name (location for pics: current-dir/images/<domain-name-dir>
# Verification has done with pages as: www.disney.fi, www.huuto.net, www.animalplanet.com, www.hs.fi and www.yle.fi
# Tool write all the URLs where the images has been called to file: url_list_file.txt, 
# it checks if URL is already in list if it's there we don't write it again. 

# Next info pops up if user just run command 'python webPicsSaver.py' 
"""
Usage for the app: 
'python webPicsSaver.py <url_to_search_images>'
URL should be in form as http://www.disney.com or www.disney.com.
This command line - tool is for fetching and saving images from web - page.
Images from the web - page will be saved to: current-dir/images/<domain-dir>
"""
import re
import getopt  # Getting the options as --help
import urllib2
import os, sys
import time, datetime
import imghdr  # For checking the type of image file, special case
from os.path import splitext
import BaseHTTPServer
from posixpath import basename, dirname
from urlparse import urlparse

# next global var is used for regular expression way to choose URLs which points to valid type of image:
# [^\s] = ^ inverts the meaning aka match every char not whitespace, + = match one or more occurrence of previous,
# (?i) = starts case-insensitive mode, last capturing group list all OK image formats, 
# last in group '=\d{2,9}' allow also img link to be captured (ID length  2 - 9 digits).
glob_image_pattern = '([^\s]+(\.(?i)|(jpg|png|gif|bmp|=\d{2,6})))'

# This pattern expect URL which contains in the start the 'www' part name of domain (alphabets A-z and digits) 
# suffixes can be add later currently used those 5.
glob_www_pattern = '((www)\.([a-zA-Z0-9]+)\.(com|org|net|tv|gov|fi|se)$)'

def valid_address(input):
    """ Checking the validity of given URL. """
    print "## Given address: " + input
    # Case when base URL has been used 'www.a.com'
    if input[:7] != "http://":
        if not re.match(glob_www_pattern, input):
            print "Error: 1 Not valid URL, address must be form as 'http://www.a.com' or 'www.a.com'"
            sys.exit(1)
        input = "http://" + input
    # Case when 'http://' is included as part of URL - string
    elif input[:7] == "http://":
        short_url = input[7:]  # Lets remove 'http://' and let RegEx decide
        if not re.match(glob_www_pattern, short_url):
            print "Error: 2 Not valid URL, address must be form as 'http://www.a.com' or 'www.a.com'"
            sys.exit(1)   
    else:
        print "Error: You have some major problems with URL, address must be form as 'http://www.a.com' or 'www.a.com'"
        sys.exit(1)
    
    print "## Starting to retrieve from site: " + input         
    return input

def fetch_from_page(address):
    """ Starts fetching images from given site. Method use try block to check the access and handle errors. """
    print "## Starting to fetch address: " + address
    try:
        web_handle = urllib2.urlopen(address)
    except urllib2.HTTPError, e:
        print "## No access to URL: HTTP Error Code", e.code
        sys.exit(1)
    except urllib2.URLError, e:
        print "## No access to URL: " + e.reason[1]
        sys.exit(1)
    except:
        print "## No access to URL: unknown error"
        sys.exit(1)
    else:
        print "## Fetching OK from %s - page." % (address)
    return web_handle

def write_to_disk(url_set, dirname):
    """ Saves images founded from web - page to folder named by the domain """
# Debug:
#    for item in url_set:
#        print item
    # Create main folder for images if it doesn't yet exists
    if not os.path.exists('images'):
        os.mkdir("images")

    # Create sub-folder named as URL domain if it doesn't yet exists
    if not os.path.exists("images/"+dirname):
        os.mkdir("images/"+dirname)
    
    # Current path which is used later in the for - loop
    current_path = os.getcwd()
    for item in url_set:
        #print item
        parsed = urlparse(item)
        # Get the file name and type
        filename, filetype = splitext(basename(parsed.path)) 
        filename = filename + filetype

        # Regular Expression: we accept only URL which is pointing real image (jpg|png|gif|bmp) or ID digit length 2 -6
        if re.match(glob_image_pattern, item):
            try:
                print "## Trying to save file %s to folder %s." %(filename, dirname) 
                imgData = urllib2.urlopen(item).read()
                output = open(os.path.join(current_path + "/images/" + dirname, filename),'wb')
                output.write(imgData)
                output.close()
                # If HTTP - path was pointing to ID instead to real image we need to clarify the type of image.                
                if len(filetype) < 2:
                    name_without_suffix = current_path + "/images/" + dirname + "/" + filename
                    type = imghdr.what(name_without_suffix)
                    os.rename(name_without_suffix, name_without_suffix + "." + type)
                    if os.path.isfile(name_without_suffix + "." + type):
                        print"## File %s saved OK to disk." %(name_without_suffix + "." + type)
                
                if os.path.isfile(current_path + "/images/" + dirname + "/" + filename):
                    print"## File %s saved OK to disk." %(filename)
                    
                print "##################################################"       
            except Exception, e:
                print str(e)

def save_url_to_file(url):
    """ Saving the URL for file. If URL was written earlier it will be not updated. """

    list_file = open(os.getcwd() + '/' + 'url_list_file.txt', 'a')
    # Check if URL is already in file
    if not url in open('url_list_file.txt').read():
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%d-%m %H:%M:%S')
        list_file.write("## URL %s fetched first time in: %s" %(url, timestamp))
        list_file.write("\n#######################################################################\n")
        list_file.close()
    
def main():
    """ Main - method as entry point and to call the methods. """
    
    # Set - collection to save all the valid URLs
    url_set = set()
    
    # Catch options and arguments from user (options are --help and -h)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    except getopt.error, msg:
        print msg
        print "For help write: 'python %s --help'" % (sys.argv[0])
        sys.exit(1)

    # If user don't give options and arguments we show the usage/info text (documentation for this module: print __doc__)
    if len(opts) == 0 and len(args) == 0:
        print __doc__
        sys.exit(1)        
     
    # If user has given command with option '-h' or '--help' help text is printed from the start of the file
    if len(opts) > 0:
       for o, a in opts:
           if o in ('-h', '--help'):
               print __doc__
               sys.exit(1)

    if not len(args) == 1:
        print "You didn't give URL argument or you gave some extra argument, try help:"
        print "python %s --help" % (sys.argv[0])
        sys.exit(1)

    address = valid_address(args[0])
    
    # Error handling for HTTP open web - page operation, returns the handle for the content.
    www_handle = fetch_from_page(address)
    
    # Save the content of the page to www_text
    www_text = www_handle.read()

    dir = www_handle.geturl().rsplit('/',1)[0]
    if (dir == "http:/"):
        dir = www_handle.geturl()

    # Find and list all URLs started by <img> tag and the content of 'src' - attribute by RegEx
    matches = re.findall('<img .*src="(.*?)"', www_text)
    
    # Add all founded image URL - paths to url_set set - collection
    for match in matches:
        # Fix URL if user hasn't use 'http://' prefix
        if match[:7] != "http://":
            if match[0] == "/":
                slash = ""
            else:
                slash = "/"
            url_set.add(dir + slash + match)
        else:
            url_set.add(match)

    url_set = list(url_set)
    url_set.sort()
    
    parse_object=urlparse(address)
    # This call will return the body of the page URL: www.abc.com
    url_body = basename(parse_object.netloc)
    
    save_url_to_file(url_body)
    
    # Domain name will be the name for Directory. Next item from split URL www.abc.com = abc 
    dirname = url_body.split('.')[1]
    write_to_disk(url_set, dirname)

if __name__ == "__main__":
    main()
