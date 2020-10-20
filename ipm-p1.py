#!/usr/bin/env python3

from urllib.request import Request, urlopen
import json
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GObject


class ComboBoxWindow(Gtk.Window):
    interv_active = None
    ad_active = None
    url = "http://127.0.0.1:5000/"

    def __init__(self):
        Gtk.Window.__init__(self, title="Intervalos")

        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.intervals=self.get_intervals()
        intervals_combo = Gtk.ComboBoxText()
        intervals_combo.set_entry_text_column(0)
        intervals_combo.connect("changed", self.on_currency_combo_changed)
        for interval in self.intervals.keys():
            intervals_combo.append_text(interval)

        hbox.pack_start(intervals_combo, True, True, 0)
        
        button = Gtk.ToggleButton(label = "Asc")
        button.connect("toggled", self.on_asc_des_button_toggled, "Asc")
        hbox.pack_start(button, True, True, 10)
        button = Gtk.ToggleButton(label = "Des")
        button.connect("toggled", self.on_asc_des_button_toggled, "Des")
        hbox.pack_start(button, True, True, 0)

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

        vbox.add(hbox)
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

    def on_asc_des_button_toggled(self, button, name):
        if (button.get_active()):
            if (self.ad_active):
                self.ad_active.set_active(False)
            self.ad_active = button
            if(self.interv_active):
                self.change_view()
        else:
            self.ad_active = None
    
    def on_currency_combo_changed(self, combo):
        self.interv_active = combo.get_active_text()
        if self.interv_active is not None:
            if(self.ad_active):
                self.change_view()
    
    def change_view(self):
        interval = self.interv_active
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


win = ComboBoxWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()