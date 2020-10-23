#!/usr/bin/env python3

import locale
import gettext

_ = gettext.gettext
N_ = gettext.ngettext

class Model:
    active_interval = None
    active_direction = None
    notes = None
    url = None
    intervals = None

    def intervals_request(fun):
        pass

    def songs_request(fun):
        pass

    def get_notes(distance):
        pass

    def get_intervals():
        pass

    def get_interval():
        pass

    def get_direction():
        pass

    def set_interval(interval):
        pass
    
    def set_direction(direction):
        pass