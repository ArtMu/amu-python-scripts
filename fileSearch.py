# Python version 2.7.3
# Arto Mujunen 11.05.2013
# Version 03
# Not 100% proof bug free because there hasn't had time to check all the special cases
# Some TODOs commented in code: e.g. no exception handling, 
# ------
# Arto Mujunen 21.05.2013
# Version 06
# Fixes:
# - Same file name in different folders problem fixed, Dictionary which collect information don't use as Key anymore the file name even counter - number.
# - Regular Expression Pattern has bug: it matched over 32 digit length strings. Now this is fixed by adding "\b" in the end of pattern.
# - Length of subString on line 94 get by len() - method not with fixed value
# - Some kind of "loose logic" thinking: break inside readlines() for - loop (line 119) in the else - branch - now fixed and removed. 
#	This caused the program exit from for - loop in the middle of file read.
# - Some cosmetic fixes
# Open issues:
# - Tool search only "port [Hexadecimal max 32 lenght]" string pairs, so no 2 spaces or tabs allowed between, "port" needs to be also lowercase.
# - File extension is "hard coded" to search currently only ".inform" - files, easy to change as user input based so user can choose what 
#
# Arto Mujunen 09.09.2014
# Version 07
# Updates:
# - File type is now given as input from user.

import sys
import os
import os.path
import re
import collections

def main():

	dirOperations()

# Go through the whole file - structure under given directory and save all the founded ".inform" - files to dictionary
def dirOperations():
	out = False
	path = ""

	# count for give the order number for the file in dictionary
	count = 0
	file_extension = '.inform'
		
	portsArray = []
	print "\n################################################################################"
	print "Special tool for search 'port [32 digit length Hexa value]' - string pair"
	print "Press < x > to exit" 
	print "################################################################################\n"
	while (out == False):
		input = raw_input("Give the input: ")
		print "You entered ", input
		if (input == 'x'or input == 'X'):
			sys.exit(0)
		if not os.access(input, os.W_OK):
			print "Not OK Path"
			print "Try again"
		else:
			print "OK Path"
			out = True

	# Amu: Choise if need to use input value
	
	temp_extension = raw_input("Give the File - type, the extension you want to search. If you give 'x' '.inform' is in use: ")
	print "You entered: ", temp_extension
	if not (temp_extension == 'x' or temp_extension == 'X'):
		file_extension = temp_extension
	
	print "File search for %s files will start."
	# Dictionary for all the inform - files
	list_of_files = {}
	
	# Amu: Used os.walk() is the core of this whole script
	# Amu: Dictionary for save all .inform files it saves Key as order number and Value as File with path
	for (dirpath, dirnames, filenames) in os.walk(path):
		for filename in filenames:
			if filename[-7:] == file_extension: 
				list_of_files[count] = os.sep.join([dirpath, filename])
				count = count + 1
	
	for value, path in list_of_files.items(): # returns the dictionary as a list of value pairs -- a tuple.
		# Amu debug
		# print "value and path: ", value, path
		portsArray.extend(gothrough(path))
	
	printInfo(portsArray)

# Amu: Method read the ".inform" - files and save all the port Hexadecimal combinations
# Return the Array (portArray) of finded matches brake if no maches
def gothrough(file):
	print "\n################################################################################"
	print "Lets seek in the folder in file: ", os.path.abspath(file)
	print "################################################################################\n"
	
	portArray = []
	
	# Amu: Regular Expression pattern to get strings with only hexa values and digit amount of between 4 - 32.
	# Amu Fix: last "\b" was lacking in the end of pattern thats why over 32 digit hexa values were falsely matched
	hexaPattern  = re.compile(r'\b[0-9a-fA-F]{4,32}\b') 
	
	# Amu: Add data to Array if valid string
	with open(file) as f:
		for line in f.readlines():
			if ("port" in line):

				print "\'port\' - string FOUND in file!"
				
				portStartIdx = line.rfind("port")
				
				# Sub-string which contains stuff after the "port" and 1 space
				subString = line[ portStartIdx + 5 : len(line)]
				# Amu comment: Only valid case is one space after "port", not sure if it is an issue.
				line_after_port = subString.split(' ')
				
				# We are interested about the first item line_after_port[0] (port's hexa value)
				# Clean e.g. tabs and newlines form the line_after_port[0] using strip()
				data = line_after_port[0].strip()
					
				# Amu: Check with Regular Expression pattern if string contain something else than Hexadecimal or it is too long
				hex = re.match(hexaPattern, data)
				if hex:
					print "This is MATCH, proper lenght and Hexadecimal", data
					portArray.append(data)

				else:
					print "This is not MATCH, not Hex or too long", data

			# Amu Debug	
			#else:	
			#	print "\'port\' - string NOT FOUND in file: ", f.name

	return portArray

# 	
def printInfo(ports):
	# Amu: Lets use Counter of Collections to show frequency of similar digits 
	frq_counter = collections.Counter(ports)
	
	print "\n\n################################################################################"
	print "		RESULTS:"
	print "PORT:		FRQ:"
	for portid in frq_counter:
		print '%s : %d' % (portid, frq_counter[portid])
	print "################################################################################"
	
# boiler
if __name__ == '__main__':
	main()