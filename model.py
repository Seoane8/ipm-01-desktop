#!/usr/bin/env python3

from urllib.request import Request, urlopen
import locale
import gettext
import json

_ = gettext.gettext

class Model:
    active_interval = None
    active_direction = None
    notes = notes = [_('do'),_('do♯/re♭'),_('re'),_('re♯/mi♭'),_('mi'),_('fa')
			,_('fa♯/sol♭'),_('sol'),_('sol♯/la♭'),_('la'),_('la♯/si♭'),_('si')]
    url = "http://127.0.0.1:5000/"
    intervals = {}

    def intervals_request(self, fun):
        try:
            # Get intervals and distance
            req = Request(self.url+'intervals')
            response =  urlopen(req)
            data = response.read()
            data = json.loads(data)

            # Defines a dict with the intervals names
            int_name = {"2m": _("Segunda menor"),
                        "2M": _("Segunda mayor"),
                        "3m": _("Tercera menor"),
                        "3M": _("Tercera mayor"),
                        "4j": _("Cuarta justa"),
                        "4aum": _("Cuarta aumentada"),
                        "5j": _("Quinta justa"),
                        "6m": _("Sexta menor"),
                        "6M": _("Sexta mayor"),
                        "7m": _("Séptima menor"),
                        "7M": _("Séptima mayor"),
                        "8a": _("Octava")}

            for i in data['data'].keys():
                self.intervals[i] = [data['data'][i], int_name[i]]

            fun(False, self.intervals.keys())
        except Exception as e:
            fun(True, None)

    def songs_request(self, fun):
        # Get interval songs
        try:
            req = Request(self.url+'songs/'+self.interv_active+'/'
                            +self.ad_active.get_label().lower())
            response =  urlopen(req)
            data = response.read()
            data = json.loads(data)
            fun(False, data['data'])
        except Exception as e:
            fun(False, None)

    def get_notes(self, distance):
        num_dist = 0
        for i in distance.split('T'):
            if len(i) == 1:
                num_dist += int(i)*2
            elif len(i) == 2:
                num_dist += int(i[0])
        if (self.active_direction=='Des'):
            num_dist *= -1
        return num_dist

    def get_intervals(self):
        return self.intervals

    def get_interval(self):
        return self.active_direction

    def get_direction(self):
        return self.active_direction

    def set_interval(self, interval):
        self.interval = interval
    
    def set_direction(self, direction):
        self.direction = direction