#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
import gettext

_ = gettext.gettext
N_ = gettext.ngettext

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class View:
    def main_quit(cls=None, w=None):
        Gtk.main_quit()

    def main(cls):
    	Gtk.main()

    def build_view(self):
        #Create Intervals ComboBox
        self.intervals_combo = Gtk.ComboBoxText()
        self.intervals_combo.set_entry_text_column(0)

        # Create Asc and Des buttons
        self.asc_button = Gtk.ToggleButton(label = "Asc")
        self.des_button = Gtk.ToggleButton(label = "Des")

        self.spinner = Gtk.Spinner()

        self.tittle = Gtk.Label(label = "")

        self.notes_distance = Gtk.Label(label = "")

        self.songs_liststore = Gtk.ListStore(str, str, str)

        # Create TreeView with songs list as model
        tree = Gtk.TreeView(self.songs_liststore)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(_("Titulo"), renderer, markup=0)
        tree.append_column(column)
        column = Gtk.TreeViewColumn(_("Favorita"), renderer, text=2)
        tree.append_column(column)

        # Select row action
        self.selection = tree.get_selection()

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.pack_start(self.intervals_combo, True, True, 0)
        hbox.pack_start(self.asc_button, True, True, 10)
        hbox.pack_start(self.des_button, True, True, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.add(hbox)
        vbox.pack_start(self.spinner, False, False, 10)
        vbox.pack_start(self.tittle, False, False, 10)
        vbox.pack_start(self.notes_distance, False, False, 10)
        vbox.add(tree)
        
        self.win = Gtk.Window(title=_("Intervalos"))
        self.win.set_default_size(500,400)
        self.win.set_border_width(10)
        self.win.connect('destroy', self.main_quit)
        self.win.add(vbox)

    def show_all(self):
        self.win.show_all()

    def connect_dir_button_toggled(self, fun):
        self.asc_button.connect('toggled', fun)
        self.des_button.connect('toggled', fun)

    def connect_intervals_combo_changed(self, fun):
        self.intervals_combo.connect('changed', fun)

    def connect_link_selection(self, fun):
        self.selection.connect('changed', fun)


    def show_waiting(self, b):
        if b:
            self.spinner.start()
        else:
            self.spinner.stop()


    def show_error(self):
        dialog = Gtk.MessageDialog(parent = self.win,
									message_type = Gtk.MessageType.ERROR,
									buttons = Gtk.ButtonsType.CLOSE,
									text = _("Error en la conexión con la red, inténtelo más tarde"))

        GLib.idle_add(self.raise_error, dialog)

    def raise_error(self, dialog):
        dialog.run()
        dialog.destroy()
        self.main_quit()

    def show_need_entry(self):
        self.tittle.set_label("")
        self.songs_liststore.clear()
        self.notes_distance.set_label(_("Seleccione un intervalo"))

    def deactivate(self, button):
        if button == self.asc_button.get_label():
            self.asc_button.set_active(False)
        elif button == self.des_button.get_label():
            self.des_button.set_active(False)

    def update_view(self, **kwargs):
        for name, value in kwargs.items():
            if name == 'tittle':
                self.tittle.set_markup(value)
            elif name == 'notes_distance':
                self.notes_distance.set_label(value)
            elif name == 'songs':
                GLib.idle_add(self.add_songs, value)
            elif name == 'intervals':
                GLib.idle_add(self.add_intervals, value)
            else:
                raise TypeError(f"update_view() got an unexpected keyword argument '{name}'")
    
    def add_songs(self, songs):
        self.songs_liststore.clear()
        self.show_waiting(False)
        for song in songs:
            self.songs_liststore.append(song)

    def add_intervals(self, intervals):
        self.show_waiting(False)
        for interval in intervals:
            self.intervals_combo.append_text(interval)
        self.show_need_entry()