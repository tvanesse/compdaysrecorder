# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from datetime import date as dt
import csv
from collections import defaultdict
import os
import fileinput
import sys

# Matplotlib
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib import pyplot as plt
import numpy as np

class Recorder :
	
	def __init__(self):
		self._REC_PATH = "data/records/record.rec"
		self._QUOTA_PATH = "data/records/quota.rec"
		self._STD_DAY = 8					# number of hours in a regular day
		self._NIGHT_TIME_BONUS = 0.25		# I earn (_STD_DAY * NIGHT_BONUS) compensation hours if I work by night
		self._SUN_TIME_BONUS = 1
		self._OVT_TIME_BONUS = 0			# extra time
		self._OFFSET = 110
		
		# Keeps track of the compensation hours earned/lost day after day.
		self._offHours = dict()
		
		# These are the _entries
		self._entries = dict()
		
		# Load the record file
		self.load_entries()
		self.computeOffHours()
		
		
	def orderDict(self, d):
		keysList = sorted(d.keys())
		valuesList = list()
		for elem in keysList:
			valuesList.append(d[elem])
			
		return (keysList, valuesList)
		
		
	def load_entries(self):
		"""
		Loads all the _entries in a dictionary where keys are datetime.date objects and
		values are subdictionary of the form {shift, extra} where
			- shift is a char amongst {d,a,n,o,h}
			- extra is an int
		"""
		# Open the file and browse.
		with open(self._REC_PATH, 'rb') as f:
			reader = csv.DictReader(f, dialect='excel', delimiter=',')
			
			for row in reader:
				date = datetime.strptime(row['Date'], "%d%m%Y").date()
				self._entries[date] = {'shift':row['Shift'], 'extra':int(row['Extra'])}
		
		return self._entries
		
			
	def findEntry(self,date):
		'''
		Returns the entry corresponding to the parameter date.
		The parameter date must be a date object.
	
		The returned value is either -1 if the entry was not found
		or a dictionary of the form {shift, extra} where
			- shift is a char amongst {d,a,n,o,h}
			- extra is an int
		'''
		if date not in self._entries.keys() :
			return -1
		else :
			return self._entries[date]
		
			
	def findLastEntry(self):
		'''
		Returns the last entry in the record file.
		The returned value is a dictionary {date, shift, extra}
		where 
			- date is a date object
			- shift is a char amongst {d,a,n,o,h}
			- extra is an int
		'''
		last = dt.min	# the minimum representable date from datetime module
		for d in self._entries.keys() :
			if d > last : last = d
		
		return {'date':last, 'shift':self._entries[last]['shift'], 'extra':self._entries[last]['extra']}
		
	
	def findFirstEntry(self):
		'''
		Returns the first entry of the record file.
		'''
		first = dt.max
		for d in self._entries.keys():
			if d < first : first = d
			
		return {'date':first, 'shift':self._entries[first]['shift'], 'extra':self._entries[first]['extra']}
	
	
	def writeEntry(self, date, shift, extra):
		'''
		Writes an entry to the record file. Overwrite an entry if it
		already exists.
		'''
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
		
	
	def removeEntry(self, date):
		#TODO : check if it works
		# Make sure the entry corresponding to `date` is already recorded
		if self.findEntry(date) != -1 :
			for line in fileinput.input(self._REC_PATH, inplace=1):
				if dt.strftime(date, "%d%m%Y") in line :
					continue
				else :
					sys.stdout.write(line)
			del self._entries[date]
			return 0
		else :
			print("The entry does not exist. There is nothing to delete.")
			return -1
		
		
	def isSunday(self, date) :
		if date.isoweekday() == 7 :
			return True
		else :
			return False
		
			
	def computeOffHours(self):
		'''
		Compute the compensation hours by browsing the _entries and populating self._offHours
		'''
		acc = self._OFFSET
		# Browse the _entries
		for (k, v) in self._entries.items() :
			shift = v['shift']
			extra = v['extra']
			
			if shift != 'h' :
				if shift == 'o' : acc -= self._STD_DAY
			
				elif self.isSunday(k) :
					# Working on Sunday
					if shift == 'n' : acc += self._STD_DAY*self._SUN_TIME_BONUS + self._STD_DAY*self._NIGHT_TIME_BONUS
					else : acc += self._STD_DAY*self._SUN_TIME_BONUS
				
				elif shift == 'n' :
					# Working on a regular day
					acc += self._STD_DAY*self._NIGHT_TIME_BONUS
					
			self._offHours[k] = acc
		
		return acc
		
		
	def plotOffHours(self):
		'''
		Returns a FigureCanvasGTK3Agg object that displays a graphical representation
		of self._offHours
		'''
		(t, val) = self.orderDict(self._offHours)
		
		#plt.xkcd(scale=1, length=100, randomness=2)
		f = plt.figure(figsize=(6,4), dpi=100)
		a = f.add_subplot(111)
		z = np.zeros(len(t))
		a.fill_between(t, z, val, np.array(val) > 0.0, color='green', alpha=.25, interpolate=True)
		a.fill_between(t, z, val, np.array(val) < 0.0, color='red', alpha=.25, interpolate=True)
		a.grid(True)
		f.autofmt_xdate()
		
		# Generate the ticks
		ticks = list()
		tick_labels = list()
		ticks.append(t[0])
		tick_labels.append(dt.strftime(t[0], "%b %y").decode("utf-8"))	# avoids problems with the accentuated months
		
		curr_month = t[0].month
		for d in t:
			if d.month != curr_month :
				curr_month = d.month
				ticks.append(dt(day=1,month=curr_month, year=d.year))
				tick_labels.append(dt.strftime(d, "%b %y").decode("utf-8"))
		
		a.set_xticks(ticks)
		a.set_xticklabels(tick_labels)
		
		canvas = FigureCanvas(f)  # a gtk.DrawingArea
		canvas.show()
		
		return canvas
		
