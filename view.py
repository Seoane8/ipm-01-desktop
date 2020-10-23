#!/usr/bin/env python3

import locale
import gettext

_ = gettext.gettext
N_ = gettext.ngettext

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class View:

    def main():
        pass

    def buil_view(self):
        pass

    def show_all(self):
        pass

    def connect_dir_button_togled(self, fun):
        pass

    def connect_interval_combo_changed(self, fun):
        pass

    def connect_link_selection(self, fun):
        pass

    def show_waiting(self, b):
        if b:
            self.spinner.start()
        else:
            self.spinner.stop()

    def show_error(self):
        pass

    def show_need_entry(self):
        self.tittle.set_label("")
        self.songs_liststore.clear()
        self.notes_distance.set_label(_("Seleccione un intervalo"))

    def update_view(self, **kwargs):
         for name, value in kwargs.items():
            if name == 'tittle':
                self.tittle.set_markup(value)
            elif name == 'notes_distance':
                self.notes_distance.set_label(value)
            elif name == 'songs':
                for song in value:
                    self.songs_liststore.append(song)
            elif name == 'intervals':
                for interval in value:
                    self.intervals_combo.append_text(interval)
            else:
                raise TypeError(f"update_view() got an unexpected keyword argument '{name}'")