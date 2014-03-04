# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('compdaysrecorder')

from gi.repository import Gtk # pylint: disable=E0611

from compdaysrecorder import CompdaysrecorderWindow

from compdaysrecorder_lib import set_up_logging, get_version

def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs compdaysrecorder_lib also)"))
    (options, args) = parser.parse_args()

    set_up_logging(options)

def main():
    'constructor for your class instances'
    parse_options()

    # Run the application.    
    window = CompdaysrecorderWindow.CompdaysrecorderWindow()
    window.show()
    Gtk.main()
