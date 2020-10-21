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
	gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'toggle button' and node.get_name() == '3M')
	boton = next(gen, None)
	assert boton is not None
	e2e.do_action(boton, 'click')
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
	assert label and label.get_text(0, -1) == "De 'do' a 'mi'", label.get_text(0, -1)
	return ctx

def when_he_realizado_la_seleccion_resultado1(ctx):
	gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'ListStore')
	ListStore = next(gen, None)
	#assert ListStore and ListStore.get_selection().startswith == "La primavera (Vivaldi)", label.get_selection

if __name__ == '__main__':
	sut_path = sys.argv[1]
	initial_ctx = Ctx(path= sut_path, process= None, app= None)

	show("""
		GIVEN he lanzado la aplicacion
		""")
	ctx = initial_ctx
	try:
		ctx = given_he_lanzado_la_aplicacion(ctx)
		show_passed()
	except Exception as e:
		show_not_passed(e)
	
	show("""
		GIVEN he lanzado la aplicacion
		WHEN pulso el boton	3M
		AND WHEN pulso el boton Asc
		""")

	try:
		ctx = when_pulso_el_boton_3M(ctx)
		ctx = when_pulso_el_boton_Asc(ctx)
		show_passed()
	except Exception as e:
		show_not_passed(e)

	show("""
		THEN Muestra los resultados apropiados
	""")


	try:
		ctx = when_he_realizado_la_seleccion_intervalo(ctx)
		#ctx = when_he_realizado_la_seleccion_resultado1(ctx)

		show_passed()
	except Exception as e:
		show_not_passed(e)
	e2e.stop(ctx.process)



