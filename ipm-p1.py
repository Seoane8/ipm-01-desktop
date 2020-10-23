#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
import gettext
from pathlib import Path

from presenter import Presenter
from model import Model
from view import View

if __name__ == '__main__':
	locale.setlocale(locale.LC_ALL, '')
	LOCALE_DIR = Path(__file__).parent / "locale"
	locale.bindtextdomain('Intervals', LOCALE_DIR)
	gettext.bindtextdomain('Intervals', LOCALE_DIR)
	gettext.textdomain('Intervals')

	controller = Presenter()
	controller.set_model(Model())
	controller.set_view(View())
	controller.main()

