#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
import gettext
import threading

_ = gettext.gettext

class Presenter:

    def main(self):
        self.view.show_waiting(True)
        threading.Thread(target=self.set_intervals, daemon=True).start()
        self.view.show_all()
        self.view.main()

    def set_view(self, view):
        self.view = view
        self.view.build_view()
        self.view.connect_dir_button_toggled(self.on_dir_button_toggled)
        self.view.connect_intervals_combo_changed(self.on_intervals_combo_changed)
        self.view.connect_link_selection(self.on_link_selection)

    def set_model(self, model):
        self.model = model

    def on_dir_button_toggled(self, button):
        active_button = self.model.get_direction()
        active_interval = self.model.get_interval()

        if (button.get_active()):
            if active_button is not None:
                self.view.deactivate(active_button)
            self.model.set_direction(button.get_label())
            if active_interval is not None:
                self.set_tittle_distance(active_interval, button.get_label())
        else:
            self.view.show_need_entry()
            self.model.set_direction(None)


    def on_intervals_combo_changed(self, combo):
        active_interval = combo.get_active_text()
        active_direction = self.model.get_direction()
        self.model.set_interval(active_interval)

        if active_direction is None:
            self.view.show_need_entry()
            return
        
        self.set_tittle_distance(active_interval, active_direction)

    def on_link_selection(self, tree, treeiter, path):
		# Open url link if exists
        model = tree.get_model()
        if ((treeiter is not None) and (model[treeiter][1] != "")):
            import webbrowser
            threading.Thread(target=webbrowser.open, daemon=True, args=(model[treeiter][1], )).start()

    def set_songs(self):
        try:
            toret = []
            for song in self.model.songs_request():
                if song[1] != "":
                    name = '<span underline="single">'+song[0]+'</span>'
                else:
                    name = song[0]
                toret.append([name, song[1], song[2]])
            self.view.update_view(songs = toret)
        except Exception:
            self.view.show_error()

    def set_intervals(self):
        try:
            self.view.update_view(intervals = self.model.intervals_request())
        except Exception:
            self.view.show_error()
        

    def set_tittle_distance(self, active_interval, active_direction):
        self.view.show_waiting(True)
        threading.Thread(target=self.set_songs, daemon=True).start()
        interval = self.model.get_intervals()[active_interval]
        distance, note1, note2 = self.model.get_notes(interval[0], active_direction)

        tittle = ('<span size="x-large" weight="ultrabold">' 
                + interval[1] 
                + ' '+(_("ascendente") if active_direction=='Asc' else _("descendente"))
                + '</span>')
        notes_distance = (_('De "')+_(note1)
                        + _('" a "')+_(note2)
                        + '" ('+str(distance)
                        +' '+(_('Semitono') if distance==1 else _('Semitonos'))+')')

        self.view.update_view(tittle = tittle, notes_distance = notes_distance)