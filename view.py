#!/usr/bin/env python3

import locale
import gettext

_ = gettext.gettext
N_ = gettext.ngettext

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class View:

    def main(cls):
    	Gtk.main()

    def buil_view(self):
        interv_active = None
		ad_active = None
		url = "http://127.0.0.1:5000/"
		notes = [_('do'),_('do♯/re♭'),_('re'),_('re♯/mi♭'),_('mi'),_('fa')
				,_('fa♯/sol♭'),_('sol'),_('sol♯/la♭'),_('la'),_('la♯/si♭'),_('si')]
		intervals = {}

		def __init__(self):
			Gtk.Window.__init__(self, title=_("Intervalos"))

			self.set_default_size(500,400)
			self.set_border_width(10)

			vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
			hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

			self.spinner = Gtk.Spinner()

			self.intervals_combo = Gtk.ComboBoxText()
			self.intervals_combo.set_entry_text_column(0)
			self.intervals_combo.connect("changed", self.connect_intervals_combo_changed)
			threading.Thread(target=self.get_intervals, daemon=True).start()
			hbox.pack_start(self.intervals_combo, True, True, 0)

			# Create Asc and Des buttons
			button = Gtk.ToggleButton(label = "Asc")
			button.connect("toggled", self.connect_dir_button_togled, "Asc")
			hbox.pack_start(button, True, True, 10)
			button = Gtk.ToggleButton(label = "Des")
			button.connect("toggled", self.connect_dir_button_togled, "Des")
			hbox.pack_start(button, True, True, 0)

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
			selection = tree.get_selection()
			selection.connect("changed", self.connect_link_selection)

			vbox.add(hbox)
			vbox.pack_start(self.spinner, False, False, 10)
			vbox.pack_start(self.tittle, False, False, 10)
			vbox.pack_start(self.notes_distance, False, False, 10)
			vbox.add(tree)

			self.add(vbox)

    def show_all(self):
        self.win.show_all()

    def connect_dir_button_togled(self, fun):
		self.win.connect('on_dir_button_toggled', fun)

    def connect_interval_combo_changed(self, fun):
		self.win.connect('on_intervals_combo_changed', fun)

    def connect_link_selection(self, fun):
        self.win.connect('on_link_selection', fun)


    def show_waiting(self, b):
        if b:
            self.spinner.start()
        else:
            self.spinner.stop()


    def show_error(self):
		dialog = Gtk.MessageDialog(parent = self,
									message_type = Gtk.MessageType.ERROR,
									buttons = Gtk.ButtonsType.CLOSE,
									text = _("Error en la conexión con la red, inténtelo más tarde"))
		dialog.run()
		dialog.destroy()
		Gtk.main_quit()

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