"""
engine para setear donde buscar
1° setear lenguaje
2° aplicar un search (argumento lo que quiero buscar), devuelve un articulo
le puede pedir algo al articulo (article.sections por ejemplo devuelve una lista de objetos)
en el titulo de la seccion tenemos informacion de si es adjetivo, sustantivo, o verbo

articulo --> seccion ---> titulo

dir(objeto) devuelve una lista de lo que podes pedir

"""

import PySimpleGUI as sg
import string

def segunWiktionary(palabra, tipo):
	"""Funcion que busca en Wiktionary la palabra ingresada,
	devuelve (None, '') si no se encontró la palabra en Wiktionary
	devuelve (False, '') si se encontró la palabra pero no coincide el tipo (Sustantivo, adjetivo o verbo)
	devuelve (True, 'la definicion de la palabra') si se encontró la palabra y coincidió el tipo"""


	import pattern.web as patweb

	tipo = tipo.lower()
	tipo = tipo.capitalize()
	palabra = palabra.lower()
	descripcion = ''

	#Lista de titulos de secciones
	tipoSustantivo = ['Sustantivo femenino', 'Sustantivo masculino', 'Sustantivo propio', 'Forma sustantiva']

	tipoAdjetivo = ['Forma adjetiva', 'Adjetivo']

	tipoVerbo = ['Forma verbal', 'Verbo', 'Verbo intransitivo', 'Verbo transitivo']

	#Se elige la lista correspondiente al tipo seleccionado
	if (tipo == 'Sustantivo'):
		tipoElegido = tipoSustantivo
	elif (tipo == 'Adjetivo'):
		tipoElegido = tipoAdjetivo
	elif (tipo == 'Verbo'):
		tipoElegido = tipoVerbo

	#Se busca el articulo segun la palabra que le pasamos y se guardan los titulos de las secciones de ese articulo
	engine = patweb.Wiktionary(license=None, throttle=5.0, language='es')
	query = palabra
	article = engine.search(query,
	   start = 1,               # Starting page.
	   count = 10,              # Results per page.
	   size = None,
	   language= 'Español',             # Image size: TINY | SMALL | MEDIUM | LARGE
	   cached = True)


	if(article == None):
		#Si no encuentra el articulo en Wiktionary devuelve encontrado como None
		encontrado = None
	else:
		#Si se encontró el artículo
		#Recorre todas las secciones y pregunta si alguna es del tipoElegido, si la encuentra la guarda para luego sacar la definicion
		encontrado = False
		seccion = None
		for section in article.sections:
			if (encontrado == False and section.title in tipoElegido):
				encontrado = True
				seccion = section

		#Si la palabra es del tipo especificado
		if (encontrado == True):
			#divide las secciones por renglón
			listaContenido = seccion.content.split('\n')

			print(listaContenido) #borra

			#Busca el elemento de la lista que contiene la definicion y se guarda la posicion en la variable pos
			posActual = 0
			pos = 0
			for x in listaContenido:
				if (x != '') and (x[0] in string.digits and pos == 0):
					pos = posActual
				posActual += 1

			listaContenido = listaContenido[pos:]

			if (len (listaContenido) > 1):
				descripcion = '\n'.join(listaContenido)
			else:
				descripcion = listaContenido[0]


	return (encontrado, descripcion)

x = segunWiktionary('carrera', 'sustantivo')

print(x)

sg.Popup(x[1])
