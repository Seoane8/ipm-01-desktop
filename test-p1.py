#!/usr/bin/env python3

import sys
import textwrap
from collections import namedtuple

import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi

import e2e

def show(text):
	print(textwrap.dedent(text))

def show_passed():
	print('\033[92m', "    Passed", '\033[0m')

def show_not_passed(e):
	print('\033[91m', "    Not passsed", '\033[0m')
	print(textwrap.indent(str(e), "    "))


Ctx = namedtuple("Ctx", "path process app")

def given_he_lanzado_la_aplicacion(ctx):
	process, app = e2e.run(ctx.path)
	assert app is not None
	return Ctx(path = ctx.path, process = process, app = app)

def when_pulso_el_boton_3M(ctx):
	gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'menu item' and node.get_name() == '3M')
	item = next(gen, None)
	assert item is not None
	e2e.do_action(item, 'click')
	return ctx

def when_pulso_el_boton_Asc(ctx):
	gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'toggle button' and node.get_name() == 'Asc')
	boton = next(gen, None)
	assert boton is not None
	e2e.do_action(boton, 'click')
	return ctx

def when_he_realizado_la_seleccion_intervalo(ctx):
	gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'label' and node.get_text(0, -1).startswith("Tercera mayor ascendente"))
	label = next(gen, None)
	assert label and label.get_text(0, -1) == "Tercera mayor ascendente", label.get_text(0, -1)
	return ctx

def when_he_realizado_la_seleccion_tonos(ctx):
	gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'label' and node.get_text(0, -1).startswith("De"))
	label = next(gen, None)
	assert label and label.get_text(0, -1) == 'De "do" a "mi" (4 Semitonos)', label.get_text(0, -1)
	return ctx

def when_he_realizado_la_seleccion_resultado1(ctx):
	gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'table cell' and node.get_name() == 'La primavera (Vivaldi)')
	resultado = next(gen, None)
	assert resultado is not None
	return ctx

if __name__ == '__main__':
	sut_path = sys.argv[1]
	initial_ctx = Ctx(path= sut_path, process= None, app= None)
	
	ctx = initial_ctx

	show("""
		GIVEN he lanzado la aplicacion
		WHEN selecciono 3M en el deplegable
		AND WHEN pulso el boton Asc
		THEN Muestra 'Tercera mayor ascendente'
		AND Muestra 'De "do" a "mi" (4 Semitonos)'
		AND Muestra 'La primavera (Vivaldi)'
	""")


	try:
		ctx = given_he_lanzado_la_aplicacion(ctx)
		ctx = when_pulso_el_boton_Asc(ctx)
		ctx = when_pulso_el_boton_3M(ctx)
		ctx = when_he_realizado_la_seleccion_intervalo(ctx)
		ctx = when_he_realizado_la_seleccion_tonos(ctx)
		ctx = when_he_realizado_la_seleccion_resultado1(ctx)

		show_passed()
	except Exception as e:
		show_not_passed(e)
	e2e.stop(ctx.process)



