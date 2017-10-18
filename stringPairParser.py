#!/usr/bin/env python
#
# Python version 2.7.6, OS Ubuntu 14.04
# Arto Mujunen 09.09.2014
# Notes:
# - This is command line version of WxPython/strOccurenceParser.py GUI script version!!!
# - Idea is to find "key - value" pairs from given file types in file system, e.g. "port HE2243DF12"
# - Tool search based on user input
#       e.g: "[port/value/item] [Hexadecimal value]" string pairs, it allows only 1 space between strings.
#		It asks the first string value and max and min length of Hexa value from user as a start.
# - The os.walk() - method is the core for the whole tool. It goes top to down (as default) the directory tree.
#	It returns in every level 3 tuples: dir-path (1 value), dir-names and file-names 
# - File extension is given by user if user choose 'x' tool uses default ".inform" - files. 
# - Same file - name issue: If same name of file in different folders founded, Dictionary shouldn't use file name as keys 
#   other vice only first founded file will be in list thats why 'count' - counter is used as key (line 86). 
#   This use-case has been verified on TestDir/ with samename.inform files in different folders.
#
# - Optional issue: Search also form Symbolic link directories by using in os.walk() True for argument followlinks (line 81). 
# - in my gitHub you find the file - structure which you can use as initial testing purposes. 
#		Files in the structure have .inform - extension and they contains 'port' hexadecimal - string pairs spread around.    

import sys
import os
import os.path
import re
import collections

global min_len, max_len, first_arg

global hexaPattern

def main():
	print "### Main ###"
	file_type, path = user_inputs()
	search_valid_files(file_type, path)
	
def user_inputs():
	""" Catch User Inputs as directory and file type. """
	out = False
	path = ""
	file_extension = '.inform'
	
	print "\n################################################################################"
	print "Special tool for search '<what ever name> [32 digit length Hexa value]' - string pair"
	print "Press < x > to exit" 
	print
	print "Available Dir(s): "
	_list_available_dirs()
	print "################################################################################\n"
	while (out == False):
		path = raw_input("Give the Directory: ")
		print "You entered ", path
		if (path == 'x'or path == 'X'):
			sys.exit(0)
		if not os.access(path, os.W_OK):
			print "Not OK Path"
			print "Try again"
		else:
			print "OK Path"
			out = True
	
	global min_len, max_len, first_arg
	first_arg = raw_input("Give the first string [port/value/item] for your parsing.")
	min_len = raw_input("Give the minimum length of the Hexa - string.")
	print "Your minimum is: " + min_len
	max_len = raw_input("Give the maximum length of the Hexa - string.")
	print "Your maximum is: " + max_len
	
	# Explanation/Usage for the user inside raw_input 
	temp_extension = raw_input("""Give the File - type, the extension you want to search.
	If you give 'x' '.inform' - file type will be used: """)
	print "You entered: ", temp_extension
	if not (temp_extension == 'x' or temp_extension == 'X'):
		file_extension = temp_extension

	print "File search for << %s >> files will start." %(file_extension)

	return file_extension, path

def search_valid_files(file_extension, path):
	""" This method search all files from the needed file type and save them to list_of_files - dictionary. 
		This dictionary is parsed so that all found files will be gone through within _search_from_file() 
		method. All port values will be then extend to portsArray (extend() because we are merging 2 arrays).
		In the end _print_info() helper method is called list the "statistics" to screen.
	"""
	# Dictionary for all the inform - files
	list_of_files = {}
	
	portsArray = []
	# count for give the order number for the file in dictionary
	count = 0
	# Length of file extension used inside next for - loop to check validity of file type (extension length can vary)
	ex_len = len(file_extension)
	# Using os.walk() is the core idea of this whole script
	# Dictionary for save all .inform files it saves Key as order number and Value as File with path
	# OPTIONAL TASK F2: os.walk argument followlinks=True allows to search under symbolic links
	for (dirpath, dirnames, filenames) in os.walk(path, followlinks=True):
		for filename in filenames:
			if filename[-ex_len:] == file_extension:
				list_of_files[count] = os.sep.join([dirpath, filename])
				count = count + 1
	
	# Parse out the port values from each file (path) 
	for value, path in list_of_files.items():

		# .extend because we are "merging" 2 arrays
		portsArray.extend(_search_from_file(path))
	
	_print_info(portsArray)	

def _list_available_dirs():
	""" Local method Prints out all the directories inside current folder """
	# Handy one-liner to list all directories in current directory. [1] is for folders, [2] is for files
	dirs = os.walk('.').next()[1]
	for dir in dirs:
		print "Dir: " + dir

def _search_from_file(file):
	""" Local Method read the ".inform" - file and save all the port Hexadecimal combinations
		Returns the Array (portArray) of find matches
	"""
	print "\n################################################################################"
	print "Lets seek in the file: ", os.path.abspath(file)
	print "################################################################################\n"
	
	global hexaPattern, min_len, max_len, first_arg
	
	portArray = []
	search_word = first_arg
	
	# Regular Expression pattern to get strings with only Hexa values and digit amount of between 4 - 32.
	 
	hexaPattern  = re.compile(r'\b[0-9a-fA-F]{%s,%s}\b' %(min_len, max_len))
	# Add data to Array if valid string
	with open(file) as f:
		for line in f.readlines():
			# This check can be insensitive by using RegEx comment about that in start of the file.*
			if (search_word in line): 

				print search_word + " - string FOUND in file!"
				
				portStartIdx = line.rfind(search_word)
				
				# Sub-string which contains stuff after the "port" and 1 space
				subString = line[ portStartIdx + 5 : len(line)]
				# Comment: Only valid case is one space after "port", not sure if it is an issue.
				line_after_port = subString.split(' ')
				
				# We are interested about the first item line_after_port[0] (port's hexa value)
				# Clean e.g. tabs and newlines form the line_after_port[0] using strip()
				data = line_after_port[0].strip()

				# Check with Regular Expression pattern if string contain something else than Hexadecimal or it is too long
				hex = re.match(hexaPattern, data)
				if hex:
					print "This is MATCH, proper length and Hexadecimal", data
					portArray.append(data)

				else:
					print "This is not MATCH, not Hex or too long", data

	return portArray

def _print_info(ports):
	""" Method use Counter of Collections to show frequency of similar digits. 
	str.format is used for tabulating results """
	frq_counter = collections.Counter(ports)

	print "\n\n################################################################################"
	print "			RESULTS:"
	print "PORT:		 			FREQUENCY:"
	for portid in frq_counter:
		sys.stdout.write("{0:<50}{1:<10}\n".format(portid, frq_counter[portid]))
		print "----------------------------------------------------------------------"
	print "################################################################################"
	
# boiler
if __name__ == '__main__':
	main()