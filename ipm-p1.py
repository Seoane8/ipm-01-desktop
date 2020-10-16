#!/usr/bin/env python3

from urllib.request import Request, urlopen
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class IntervalWindow(Gtk.Window):
    def __init__(self):

        self.url = "http://127.0.0.1:5000/"
        self.interv_active = None
        self.ad_active = None

        req = Request(self.url+'intervals')
        response =  urlopen(req)
        data = response.read()
        data = json.loads(data)
        data = data["data"]
        intervals = data.keys()

        Gtk.Window.__init__(self, title = "Intervalos")

        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,)
        hbox1 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        hbox2 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        
        hbox1.set_margin_end(20)
        hbox1.set_margin_start(20)
        hbox1.set_margin_top(10)
        hbox1.set_margin_bottom(5)
        hbox2.set_margin_end(200)
        hbox2.set_margin_start(200)
        hbox2.set_margin_top(5)
        hbox2.set_margin_bottom(5)

        for i in intervals:
            button = Gtk.ToggleButton(label = i)
            button.connect("toggled", self.on_interv_button_toggled, i)
            hbox1.pack_start(button, True, True, 0)

        button = Gtk.ToggleButton(label = "Asc")
        button.connect("toggled", self.on_asc_des_button_toggled, "Asc")
        hbox2.pack_start(button, True, True, 0)
        button = Gtk.ToggleButton(label = "Des")
        button.connect("toggled", self.on_asc_des_button_toggled, "Des")
        hbox2.pack_start(button, True, True, 0)

        self.tittle = Gtk.Label(label = "")

        vbox.add(hbox1)
        vbox.add(hbox2)
        vbox.pack_start(self.tittle, True, True, 10)

        self.add(vbox)


    def on_interv_button_toggled(self, button, name):
        if(button.get_active()):    
            if (self.interv_active):
                self.interv_active.set_active(False)
            self.interv_active = button
            if(self.ad_active):
                self.change_view()
        else:
            self.interv_active = None

    def on_asc_des_button_toggled(self, button, name):
        if (button.get_active()):
            if (self.ad_active):
                self.ad_active.set_active(False)
            self.ad_active = button
            if(self.interv_active):
                self.change_view()
        else:
            self.ad_active = None
        

    def change_view(self):
        interval = self.interv_active.get_label()
        asc_des = self.ad_active.get_label()
        req = Request(self.url+'songs/'+interval+'/'+asc_des.lower())
        response =  urlopen(req)
        data = response.read()
        data = json.loads(data)
        data = data["data"]
        
        self.tittle.set_label(interval+' '+asc_des)

win = IntervalWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()

