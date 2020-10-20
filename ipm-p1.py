#!/usr/bin/env python3

from urllib.request import Request, urlopen
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class IntervalWindow(Gtk.Window):
    url = "http://127.0.0.1:5000/"
    interv_active = None
    ad_active = None

    def __init__(self):

        self.intervals = self.get_intervals()

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

        for i in self.intervals.keys():
            button = Gtk.ToggleButton(label = i)
            button.connect("toggled", self.on_interv_button_toggled, i)
            hbox1.pack_start(button, True, False, 0)

        button = Gtk.ToggleButton(label = "Asc")
        button.connect("toggled", self.on_asc_des_button_toggled, "Asc")
        hbox2.pack_start(button, True, False, 0)
        button = Gtk.ToggleButton(label = "Des")
        button.connect("toggled", self.on_asc_des_button_toggled, "Des")
        hbox2.pack_start(button, True, False, 0)

        self.tittle = Gtk.Label(label = "")

        self.songs_liststore = Gtk.ListStore(str, str, str)

        tree = Gtk.TreeView(self.songs_liststore)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer, text=0)
        tree.append_column(column)
        column = Gtk.TreeViewColumn("Link", renderer, text=1)
        tree.append_column(column)
        column = Gtk.TreeViewColumn("Favorite", renderer, text=2)
        tree.append_column(column)

        vbox.add(hbox1)
        vbox.add(hbox2)
        vbox.pack_start(self.tittle, False, False, 10)
        vbox.add(tree)

        self.add(vbox)

    def get_intervals(self):
        req = Request(self.url+'intervals')
        response =  urlopen(req)
        data = response.read()
        data = json.loads(data)
        data = data["data"]
        int_name= {}
        intervals= {}
        int_name["2m"]= "Segunda menor"
        int_name["2M"]= "Segunda mayor"
        int_name["3m"]= "Tercera menor"
        int_name["3M"]= "Tercera mayor"
        int_name["4j"]= "Cuarta justa"
        int_name["4aum"]= "Cuarta aumentada"
        int_name["5j"]= "Quinta justa"
        int_name["6m"]= "Sexta menor"
        int_name["6M"]= "Sexta mayor"
        int_name["7m"]= "Séptima menor"
        int_name["7M"]= "Séptima mayot"
        int_name["8a"]= "Octava"
        for i in data.keys():
            intervals[i] = [data[i], int_name[i]]
        return intervals

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

        asc_des = "ascendente" if asc_des=='Asc' else "descendente"
        
        self.tittle.set_label(self.intervals[interval][-1]+' '+asc_des)
        self.songs_liststore.clear()
        for song in data:
            self.songs_liststore.append(song)

win = IntervalWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()

