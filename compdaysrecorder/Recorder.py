from datetime import datetime, timedelta
from datetime import date as dt
import csv
from collections import defaultdict
import os
import fileinput
import sys

class Recorder :
	
	def __init__(self):
		self._REC_PATH = "data/records/record.rec"
		self._QUOTA_PATH = "data/records/quota.rec"
		self._STD_DAY = 8					# number of hours in a regular day
		self._NIGHT_TIME_BONUS = 0.25		# I earn (_STD_DAY * NIGHT_BONUS) compensation hours if I work by night
		self._WE_TIME_BONUS = 2				# Weekend
		self._OVT_TIME_BONUS = 0				# extra time
		
		# Keeps track of the compensation hours earned/lost day after day.
		self._offHours = dict()
		
		# These are the _entries
		self._entries = dict()
		
		# Load the record file
		self.load_entries()
		
		
	'''
	Loads all the _entries in a dictionary where keys are datetime.date objects and
	values are subdictionary of the form {shift, extra} where
		- shift is a char amongst {d,a,n,o,h}
		- extra is an int
	'''
	def load_entries(self):
		# Open the file and browse.
		with open(self._REC_PATH, 'rb') as f:
			reader = csv.DictReader(f, dialect='excel', delimiter=',')
			
			for row in reader:
				date = datetime.strptime(row['Date'], "%d%m%Y").date()
				self._entries[date] = {'shift':row['Shift'], 'extra':int(row['Extra'])}
		
		return self._entries
		
	
	'''
	Returns the entry corresponding to the parameter date.
	The parameter date must be a datetime object.
	
	The returned value is either -1 if the entry was not found
	or a dictionary of the form {shift, extra} where
		- shift is a char amongst {d,a,n,o,h}
		- extra is an int
	'''		
	def findEntry(self,date):
		if date not in self._entries.keys() :
			return -1
		else :
			return self._entries[date]
		
			
	'''
	Returns the last entry in the record file.
	The returned value is a dictionary {date, shift, extra}
	where 
		- date is a datetime object
		- shift is a char amongst {d,a,n,o,h}
		- extra is an int
	'''
	def findLastEntry(self):
		last = dt.min	# the minimum representable date from datetime module
		for d in self._entries.keys() :
			if d > last : last = d
		
		return {'date':last, 'shift':self._entries[last]['shift'], 'extra':self._entries[last]['extra']}
		
	
	'''
	Returns the first entry of the record file.
	'''
	def findFirstEntry(self):
		first = dt.max
		for d in self._entries.keys():
			if d < first : first = d
			
		return {'date':first, 'shift':self._entries[first]['shift'], 'extra':self._entries[first]['extra']}
	
	
	'''
	Writes an entry to the record file. Overwrite an entry if it
	already exists.
	'''
	def writeEntry(self, date, shift, extra):
		# String convertion
		dateStr = dt.strftime(date, "%d%m%Y")
		
		first = self.findFirstEntry()['date']
		last = self.findLastEntry()['date']
		recorded = self.findEntry(date) != -1
		
		# Check if this entry is the most recent one.
		if date > last :
			# Then simply add a new entry at the very end of the file
			with open(self._REC_PATH, 'a') as f:
				f.write("{},{},{}\n".format(dateStr,shift,extra))
		
		# Check if this entry is the oldest one.
		elif date < first :
			# Add the new entry at the very beginning of the file
			for line in fileinput.input(self._REC_PATH, inplace=1):
				if line.split(',')[0]=="Date" :
					sys.stdout.write(line)
					sys.stdout.write("{},{},{}\n".format(dateStr,shift,extra))
				else :
					sys.stdout.write(line)
					
		# Insert the entry in the middle
		else :
			insertDone = False
			if not recorded :
				# The entry to insert is a new one
				for line in fileinput.input(self._REC_PATH, inplace=1):
					tmp = line.split(',')[0]
					if (tmp!="Date" and datetime.strptime(tmp, "%d%m%Y").date() > date and insertDone == False) :
						# Just reached the first entry that is more recent than the date
						# we want to insert.
						# Insert the new entry just before the current line
						sys.stdout.write("{},{},{}\n".format(dateStr,shift,extra))
						insertDone = True
					sys.stdout.write(line)
			else :
				# The entry to insert already exists. We only need to modify it.
				for line in fileinput.input(self._REC_PATH, inplace=1):
					if dateStr in line :
						line = "{},{},{}\n".format(dateStr,shift,extra)
					
					sys.stdout.write(line)
				
		#Update self._entries
		self._entries[date] = {'shift':shift, 'extra':extra}
		
		
	def isWeekend(self, date) :
		if date.isoweekday() == 6 or date.isoweekday() == 7 :
			return True
		else :
			return False
		
			
	'''
	Compute the compensation hours by browsing the _entries and populating self._offHours
	'''
	def compute_offHours(self):
		acc = 0
		# Browse the _entries
		for (k, v) in self._entries.items() :
			shift = v['shift']
			extra = v['extra']
			
			if shift != 'h' :
				if shift == 'o' : acc -= self._STD_DAY
			
				elif self.isWeekend(k) :
					# Working during the week-end
					if shift == 'n' : acc += self._STD_DAY*self._WE_TIME_BONUS + self._STD_DAY*self._NIGHT_TIME_BONUS
					else : acc += self._STD_DAY*self._WE_TIME_BONUS
				
				elif shift == 'n' :
					# Working on a regular day
					acc += self._STD_DAY*self._NIGHT_TIME_BONUS
			
#			print("{} : ACC == {}".format(dt.strftime(k, "%d-%m-%Y"),acc))
		
		return acc
				
		
			
	'''
	Returns the number of compensation hours earned at day `date`.
	If the parameter `date` is not given, returns the number of comp
	hours for today.
	
	The returned value is a float.
	'''
	def get_offHours(self):
		# /!\ 1h50 every week
		# 1/4 jours de recup pour 4 shifts de nuit
		# 2 jours de recup pour le samedi
		# 2 jours de recup pour le dimanche + 100% de surpaie
		result = 0.0
		with open(self._REC_PATH, 'rb') as f:
			reader = csv.DictReader(f, dialect='excel', delimiter=',')
			for row in reader:
				if (row['Shift'] == 'n'):
					pass
					
		
	def getOffDays(self):
		h = self.get_offHours()
		return h/8
		
		
		
		
				
