#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen
import json
import locale
import gettext

_ = gettext.gettext

class Model:
    active_interval = None
    active_direction = None
    notes = notes = [('do'), ('do♯/re♭'),('re'),('re♯/mi♭'),('mi'),('fa'),('fa♯/sol♭'),('sol'),('sol♯/la♭'),('la'),('la♯/si♭'),('si')]
    url = "http://127.0.0.1:5000/"
    intervals = {}

    def intervals_request(self):
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

        return self.intervals.keys()

    def songs_request(self):
        # Get interval songs
        req = Request(self.url+'songs/'+self.active_interval+'/'
                        +self.active_direction.lower())
        response =  urlopen(req)
        data = response.read()
        data = json.loads(data)
        return data['data']

    def get_notes(self, distance, direction):
        num_dist = 0
        for i in distance.split('T'):
            if len(i) == 1:
                num_dist += int(i)*2
            elif len(i) == 2:
                num_dist += int(i[0])
        if (direction=='Des'):
            num_dist *= -1
        return abs(num_dist), self.notes[0], self.notes[num_dist%len(self.notes)]

    def get_intervals(self):
        return self.intervals

    def get_interval(self):
        return self.active_interval

    def get_direction(self):
        return self.active_direction

    def set_interval(self, interval):
        self.active_interval = interval
    
    def set_direction(self, direction):
        self.active_direction = direction