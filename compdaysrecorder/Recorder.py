from datetime import datetime, timedelta
import csv
from collections import defaultdict
import os
import fileinput
import sys

class Recorder :
	
	def __init__(self):
		self.REC_PATH = "data/records/0102032014.rec"
		self.QUOTA_PATH = "data/records/quota.rec"
		self.REC_LINE_LEN = 13
		self.NIGHT_BONUS = 0.25
		self.SAT_BONUS = 2
		self.SUN_BONUS = 2
		
		# The following dictionary keeps track of the compensation hours earned/lost
		# day after day.
		self.offHours = dict()
		
		# These are the entries
		self.entries = dict()
		
		# Load the record file
		self.loadEntries()
		
		
	'''
	Loads all the entries in a dictionary
	'''
	def loadEntries(self):
		# Open the file and browse.
		with open(self.REC_PATH, 'rb') as f:
			reader = csv.DictReader(f, dialect='excel', delimiter=',')
			
			for row in reader:
				self.entries[row['Date']] = {'shift':row['Shift'], 'extra':int(row['Extra'])}
		
		return self.entries
		
	
	'''
	Returns the entry corresponding to the parameter date.
	The parameter date must be a string of the form ddmmyyyy.
	
	The returned value is either -1 if the entry was not found
	or a dictionary of the form {shift, extra} where
		- shift is a char amongst {d,a,n,o}
		- extra is an int
	'''		
	def findEntry(self,date):
		if date not in self.entries.keys() :
			return -1
		else :
			return self.entries[date]
		
			
	'''
	Returns the last entry in the record file.
	The returned value is a dictionary {date, shift, extra}
	where 
		- date is a string of the form ddmmyyyy
		- shift is a char amongst {d,a,n,o}
		- extra is an int
	'''
	def findLastEntry(self):
		result = datetime.min	# the minimum representable date from datetime module
		for d in self.entries.keys() :
			v = datetime.strptime(d, "%d%m%Y")
			if v > result : result = v
		
		return result
	
	
	'''
	Writes an entry to the record file. Overwrite an entry if it
	already exists.
	'''
	def writeEntry(self, date, shift, extra):
		#TODO : update self.entries when loadEntry is implemented
		# Check if this entry is the most recent one.
		last = datetime.strptime(self.findLastEntry()['date'], "%d%m%Y")
		this = datetime.strptime(date, "%d%m%Y")
		if this > last :
			# Then simply add a new entry at the very end of the file
			with open(self.REC_PATH, 'a') as f:
				f.write("{},{},{}\n".format(date,shift,extra))
				return 0
		
		# Insert the entry
		theDayAfter = this+timedelta(days=1)
		flag = False
		for line in fileinput.input(self.REC_PATH, inplace=1):
			if flag == False :
				if date in line :
					line = "{},{},{}\n".format(date,shift,extra)
					flag = True
				elif datetime.strftime(theDayAfter, "%d%m%Y") in line:
					# insert our entry just before this line
					newLine = "{},{},{}\n".format(date,shift,extra)
					sys.stdout.write(newLine)
					flag = True
				
				sys.stdout.write(line)
			else :
				sys.stdout.write(line)
			
	'''
	Compute the compensation hours by browsing the whole record file and generating
	another file with the comp hours evolution.
	'''	
	def computeOffHours(self):
		# Browse the record file
		with open(self.REC_PATH, 'rb') as frec :
			recReader = csv.DictReader(frec, dialect='excel', delimiter=',')
			# Overwrite the quota file
			for row in recReader:
				date = row['Date']				
				for line in fileinput.input(self.QUOTA_PATH, inplace=1):
					if date in line :
						sys.stdout.write()
		
			
	'''
	Returns the number of compensation hours earned at day `date`.
	If the parameter `date` is not given, returns the number of comp
	hours for today.
	
	The returned value is a float.
	'''
	def getOffHours(self):
		# /!\ 1h50 every week
		# 1/4 jours de recup pour 4 shifts de nuit
		# 2 jours de recup pour le samedi
		# 2 jours de recup pour le dimanche + 100% de surpaie
		result = 0.0
		with open(self.REC_PATH, 'rb') as f:
			reader = csv.DictReader(f, dialect='excel', delimiter=',')
			for row in reader:
				if (row['Shift'] == 'n'):
					pass
					
		
	def getOffDays(self):
		h = self.getOffHours()
		return h/8
		
		
		
		
				
