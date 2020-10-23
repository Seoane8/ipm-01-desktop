#!/usr/bin/env python3

import locale
import gettext

_ = gettext.gettext
N_ = gettext.ngettext

class Presenter:

    def main(self):
        pass

    def set_view(self, view):
        pass

    def set_model(self, model):
        pass

    def on_dir_button_toggled(self, button):
        pass

    def on_intervals_combo_changed(self, combo):
        pass

    def on_link_selection(self, selection):
        pass

    def set_songs(err, songs):
        pass

    def set_intervals(err, songs):
        pass