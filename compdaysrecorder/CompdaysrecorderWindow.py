# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('compdaysrecorder')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('compdaysrecorder')

from Recorder import Recorder

from compdaysrecorder_lib import Window
from compdaysrecorder.AboutCompdaysrecorderDialog import AboutCompdaysrecorderDialog
from compdaysrecorder.PreferencesCompdaysrecorderDialog import PreferencesCompdaysrecorderDialog

# See compdaysrecorder_lib.Window.py for more details about how this class works
class CompdaysrecorderWindow(Window):
    __gtype_name__ = "CompdaysrecorderWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(CompdaysrecorderWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutCompdaysrecorderDialog
        self.PreferencesDialog = PreferencesCompdaysrecorderDialog

        # Code for other initialization actions should be added here.
        
        self.recorder = Recorder()
        self.testButton = self.builder.get_object("testButton")
        
        # Calendar
        self.calendar = self.builder.get_object("calendar")
        
        # Date label
        self.dateLabel = self.builder.get_object("dateLabel")
        
        # Radio buttons
        self.aRadioButton = self.builder.get_object("aRadioButton")
        self.dRadioButton = self.builder.get_object("dRadioButton")
        self.nRadioButton = self.builder.get_object("nRadioButton")
        self.oRadioButton = self.builder.get_object("oRadioButton")
        self.hRadioButton = self.builder.get_object("hRadioButton")
        
        # Spin button
        self.extraSpinButton = self.builder.get_object("extraSpinButton")
        
        # Edit and Save buttons
        self.editButton = self.builder.get_object("editButton")
        self.saveButton = self.builder.get_object("saveButton")
        
    def whoIsActive(self):
        if (self.dRadioButton.get_active()) : return 'd'
        elif (self.aRadioButton.get_active()) : return 'a'
        elif (self.nRadioButton.get_active()) : return 'n'
        elif (self.oRadioButton.get_active()) : return 'o'
        else : return 'h'
        
    def enableEdition(self, boolean):
        if boolean :
            self.dRadioButton.set_sensitive(True)
            self.aRadioButton.set_sensitive(True)
            self.nRadioButton.set_sensitive(True)
            self.oRadioButton.set_sensitive(True)
            self.hRadioButton.set_sensitive(True)
            self.extraSpinButton.set_sensitive(True)
        else :
            self.dRadioButton.set_sensitive(False)
            self.aRadioButton.set_sensitive(False)
            self.nRadioButton.set_sensitive(False)
            self.oRadioButton.set_sensitive(False)
            self.hRadioButton.set_sensitive(False)
            self.extraSpinButton.set_sensitive(False)
            
        
    def on_testButton_clicked(self, widget):
        self.recorder.findLastEntry()

    def on_calendar_daySelected(self, widget):
        # Parse the date selected
        year, month, day = self.calendar.get_date()
        dateStr = "{0:02d}{1:02d}{2:04d}".format(day, month+1, year)
        
        self.dateLabel.set_text("{0:02d}/{1:02d}/{2:04d}".format(day, month+1, year))
        
        # Do we already have an entry for this date ?
        r = self.recorder.findEntry(dateStr)
        if (r != -1):
            # The entry already exist.
            #self.calendar.mark_day(day)
            tmp = r['shift']
            if (tmp=='d') : self.dRadioButton.set_active(True)
            elif (tmp=='a') : self.aRadioButton.set_active(True)
            elif (tmp=='n') : self.nRadioButton.set_active(True)
            elif (tmp=='o') : self.oRadioButton.set_active(True)
            else : self.hRadioButton.set_active(True)
            
            self.extraSpinButton.set_value(r['extra'])
            
            # Disable editing.
            self.enableEdition(False)
        else :
            # Enable edition
            self.enableEdition(True)
            
    def on_editButton_clicked(self, widget):
        # Toggle edit mode
        self.enableEdition(True)
        
    def on_saveButton_clicked(self, widget):
        year, month, day = self.calendar.get_date()
        dateStr = "{0:02d}{1:02d}{2:04d}".format(day, month+1, year)
        
        shift = self.whoIsActive()
        
        extra = int(self.extraSpinButton.get_value())
        
        self.recorder.writeEntry(dateStr, shift, extra)
        self.enableEdition(False)
        
