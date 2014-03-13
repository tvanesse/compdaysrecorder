# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('compdaysrecorder')

from gi.repository import Gtk, Gdk # pylint: disable=E0611
import logging
logger = logging.getLogger('compdaysrecorder')

from Recorder import Recorder

from datetime import date

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
        
        # The status label
#        self.statusLabel = self.builder.get_object("statusLabel")

        # Code for other initialization actions should be added here.
        self.recorder = Recorder()
        self.testButton = self.builder.get_object("testButton")
        
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
        
        # Edit, Save and Delete buttons
        self.editButton = self.builder.get_object("editButton")
        self.saveButton = self.builder.get_object("saveButton")
        self.deleteButton = self.builder.get_object("deleteButton")
        
        # Calendar
        self.calendar = self.builder.get_object("calendar")
        r = self.recorder.findLastEntry()
        _ = r['date']
        self.calendar.select_month(month=_.month - 1, year=_.year)
        self.calendar.select_day(_.day)
        self.dateLabel.set_text("{0:02d}/{1:02d}/{2:04d}".format(_.day, _.month, _.year))
        tmp = r['shift']
        if (tmp=='d') : self.dRadioButton.set_active(True)
        elif (tmp=='a') : self.aRadioButton.set_active(True)
        elif (tmp=='n') : self.nRadioButton.set_active(True)
        elif (tmp=='o') : self.oRadioButton.set_active(True)
        else : self.hRadioButton.set_active(True)
        self.extraSpinButton.set_value(r['extra'])
        self.enableEdition(False)
        
        # Plot area
        self.plotArea = self.builder.get_object("plotArea")
        self.displayPlotArea = self.builder.get_object("displayPlotArea")
        self.upArrow = self.builder.get_object("upArrow")
        self.downArrow = self.builder.get_object("downArrow")
        self.plot = self.recorder.plotOffHours()
        self.plotArea.add(self.plot)
        
        # compDaysLabel
        self.compDaysLabel = self.builder.get_object("compDaysLabel")
        self.updateCompDays()
        
    def on_displayPlotArea_toggled(self, widget):
        if self.displayPlotArea.get_active() :
            self.plot = self.recorder.plotOffHours()
            self.plotArea.set_visible(True)
            self.plotArea.show()
            self.displayPlotArea.set_image(self.upArrow)
        else :
#            self.plotArea.set_visible(False)
            self.plotArea.hide()
            self.displayPlotArea.set_image(self.downArrow)
            
        
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
            self.editButton.set_sensitive(False)
            self.saveButton.set_sensitive(True)
            self.deleteButton.set_sensitive(False)
        else :
            self.dRadioButton.set_sensitive(False)
            self.aRadioButton.set_sensitive(False)
            self.nRadioButton.set_sensitive(False)
            self.oRadioButton.set_sensitive(False)
            self.hRadioButton.set_sensitive(False)
            self.extraSpinButton.set_sensitive(False)
            self.editButton.set_sensitive(True)
            self.saveButton.set_sensitive(False)
            self.deleteButton.set_sensitive(True)
            
    def updateCompDays(self) :
        off = self.recorder.computeOffHours()
        if off< 0 :
            self.compDaysLabel.override_color(0, Gdk.RGBA(1,0,0,1))
        else :
            self.compDaysLabel.override_color(0, Gdk.RGBA(0,1,0,1))
        self.compDaysLabel.set_text(str(off/8))
            
        
    def on_testButton_clicked(self, widget):
        print("You know nothing John Snow")

    def on_calendar_daySelected(self, widget):
        # Parse the date selected
        year, month, day = self.calendar.get_date()
        dateObj = date(year, month+1, day)
        
        self.dateLabel.set_text("{0:02d}/{1:02d}/{2:04d}".format(day, month+1, year))
        
        # Do we already have an entry for this date ?
        r = self.recorder.findEntry(dateObj)
        if (r != -1):
            # The entry already exist.
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
        dateObj = date(year, month+1, day)
        
        shift = self.whoIsActive()
        
        extra = int(self.extraSpinButton.get_value())
        
        self.recorder.writeEntry(dateObj, shift, extra)
        self.enableEdition(False)
        self.updateCompDays()
        
    def on_deleteButton_clicked(self, widget):
        year, month, day = self.calendar.get_date()
        dateObj = date(year, month+1, day)
        self.recorder.removeEntry(dateObj)
        self.enableEdition(True)
        self.updateCompDays()
        
