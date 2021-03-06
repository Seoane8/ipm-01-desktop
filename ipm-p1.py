#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen
import json
import gi
import locale
import gettext

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GObject
from pathlib import Path

_ = gettext.gettext


class ComboBoxWindow(Gtk.Window):
	locale.setlocale(locale.LC_ALL, '')
	LOCALE_DIR = Path(__file__).parent / "locale"
	locale.bindtextdomain('Intervals', LOCALE_DIR)
	gettext.bindtextdomain('Intervals', LOCALE_DIR)
	gettext.textdomain('Intervals')
	interv_active = None
	ad_active = None
	url = "http://127.0.0.1:5000/"
	notes = [_('do'),_('do♯/re♭'),_('re'),_('re♯/mi♭'),_('mi'),_('fa'),_('fa♯/sol♭'),_('sol'),_('sol♯/la♭'),_('la'),_('la♯/si♭'),_('si')]

	def __init__(self):
		Gtk.Window.__init__(self, title=_("Intervalos"))

		self.set_default_size(500,400)
		self.set_border_width(10)

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

		# Create intervals ComboBox
		self.intervals=self.get_intervals()
		intervals_combo = Gtk.ComboBoxText()
		intervals_combo.set_entry_text_column(0)
		intervals_combo.connect("changed", self.on_intervals_combo_changed)
		for interval in self.intervals.keys():
			intervals_combo.append_text(interval)

		hbox.pack_start(intervals_combo, True, True, 0)
		
		# Create Asc and Des buttons
		button = Gtk.ToggleButton(label = "Asc")
		button.connect("toggled", self.on_asc_des_button_toggled, "Asc")
		hbox.pack_start(button, True, True, 10)
		button = Gtk.ToggleButton(label = "Des")
		button.connect("toggled", self.on_asc_des_button_toggled, "Des")
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
		selection.connect("changed", self.on_link_selection)

		vbox.add(hbox)
		vbox.pack_start(self.tittle, False, False, 10)
		vbox.pack_start(self.notes_distance, False, False, 10)
		vbox.add(tree)

		self.add(vbox)

	def get_intervals(self):
		# Get intervals and distance
		req = Request(self.url+'intervals')
		response =  urlopen(req)
		data = response.read()
		data = json.loads(data)
		intervals = data["data"]

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
		
		# Add intervals names 
		for i in intervals.keys():
			intervals[i] = [intervals[i], int_name[i]]
		return intervals

	def on_asc_des_button_toggled(self, button, name):
		if (button.get_active()):
			if self.ad_active is not None:
				self.ad_active.set_active(False)
			self.ad_active = button
			if self.interv_active is not None:
				self.change_view()
		else:
			self.ad_active = None
	
	def on_intervals_combo_changed(self, combo):
		self.interv_active = combo.get_active_text()
		if self.interv_active is not None:
			if self.ad_active is not None:
				self.change_view()
	
	def change_view(self):
		# Store interval info
		interval = self.intervals[self.interv_active]
		asc_des = self.ad_active.get_label()

		# Get interval songs
		req = Request(self.url+'songs/'+self.interv_active+'/'+asc_des.lower())
		response =  urlopen(req)
		data = response.read()
		data = json.loads(data)
		data = data["data"]
		
		# Change interval name
		self.tittle.set_markup('<span size="x-large" weight="ultrabold">'
								+ interval[1]
								+ ' '+(_("ascendente") if asc_des=='Asc' else _("descendente"))
								+ '</span>')

		# Calculate distance
		distance = interval[0]
		num_dist = 0
		for i in distance.split('T'):
			if len(i) == 1:
				num_dist += int(i)*2
			elif len(i) == 2:
				num_dist += int(i[0])
		if (asc_des=='Des'):
			num_dist *= -1
		# Change notes distance example
		self.notes_distance.set_label(_('De "')+self.notes[0]
										+ _('" a "')+self.notes[num_dist%12]
										+ '" ('+str(abs(num_dist))
										+' '+(_('Semitono') if abs(num_dist)==1 else _('Semitonos'))+')')

		# Change songs list
		self.songs_liststore.clear()
		for song in data:
			if (song[1] != ""):
				name = '<span underline="single">'+song[0]+'</span>'
			else:
				name = song[0]
			self.songs_liststore.append([name, song[1], song[2]])

	def on_link_selection(self, selection):
		# Open url link if exists
		model, treeiter = selection.get_selected()
		if ((treeiter is not None) and (model[treeiter][1] != "")):
			import webbrowser
			webbrowser.open(model[treeiter][1])


win = ComboBoxWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()