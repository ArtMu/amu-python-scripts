#!/usr/bin/env python

import sys
import time
import collections
import ssh

#global min_len, max_len, first_arg

global hexaPattern

class parser():

	client = None
	def __init__(self):
		self.client = ssh.SSHClient()
		self.client.load_system_host_keys()
		self.client.set_missing_host_key_policy(ssh.WarningPolicy())
		self.count = None
	
	def create_log(self, start, end):
		
		print "### Creating temporally log, start timestamp: " + start
		self.client.exec_command("awk '$0 > \"" + start + "\"' /var/log/jbossas/standalone/server.log > timeWindowTempLogFile")
		time.sleep(2)
		
	def parse_logfile(self, search_word, lines):
		(stdin, stdout, stderr) = self.client.exec_command("grep -A " + lines + 
														" --group-separator'=====================================================================' " 
														+ search_word + " timeWindowTempLogFile")
		
		result = stdout.read()
		# DEBUG print "### STDOUT result " + result
		return result
		
	def latest_timestamp(self):
		(stdin, stdout, stderr) = self.client.exec_command("tail -n 1 /var/log/jbossas/standalone/server.log|grep -o '[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'")	
		latest = stdout.read()
		print "### Latest " + latest
		return latest
		
	def log_to_node(self, hostname, user, passw):
		printout = "### Try to connect over SSH ..."
		try:
			
			print '### Connecting...'
			printout = '### Connecting... \n'
			port = 22			
			self.client.connect(hostname, port, user, passw)
			
			#chan = self.client.invoke_shell()
			print "### Client get_transport " + repr(self.client.get_transport())
			print '### Connection established'
			printout += '### Connection established\n'
			print
			stdin, stdout, stderr = self.client.exec_command("pwd")
			print "### PWD: " + stdout.read()
			#interactive.interactive_shell(chan)
			#chan.close()
			
		except Exception, e:
			print '### Caught exception: %s: %s' % (e.__class__, e)
			printout += '### Caught exception: %s: %s' % (e.__class__, e)
			#traceback.print_exc()
			try:
				self.client.close()
			except:
				pass
			sys.exit(1)

		return printout
	
	def close(self):
		self.client.close()
	
	def calc_error_statistics(self, result):
		self.count = str(result).count("ERROR")
		print "### Count " + str(self.count)
		errorTable = []
		logLines = str(result).split("\n")
		for line in logLines:
			if 'ERROR [' in line:
				print "### Line: " + line
				start = str(line).index('ERROR [') + 7
				substring = line[start:]	# Start part
				end = substring.index(']')
				substring = substring[:end]
				errorTable.append(substring)
		
		return self._print_info(errorTable, self.count)
	
	def get_error_count(self):
		#print "### Count: " + self.count
		return str(self.count)
	
		
	def _print_info(self, errors, count):
		""" Method use Counter of Collections to show frequency of similar digits. 
		str.format is used for tabulating results """
		frq_counter = collections.Counter(errors)
		errorDict = dict()
		
		print "\n\n################################################################################"
		print "			RESULTS:"
		print "ERROR:					 PERCENT:"
		for errorline in frq_counter:
			print errorline, "{0:.2f}".format((float(frq_counter[errorline])*100)/count)
			errorDict[errorline] = "{0:.1f}".format((float(frq_counter[errorline])*100)/count) + "\n"
			print "----------------------------------------------------------------------"
		print "################################################################################"
		return errorDict