"""
engine para setear donde buscar
1° setear lenguaje
2° aplicar un search (argumento lo que quiero buscar), devuelve un articulo
le puede pedir algo al articulo (article.sections por ejemplo devuelve una lista de objetos)
en el titulo de la seccion tenemos informacion de si es adjetivo, sustantivo, o verbo

articulo --> seccion ---> titulo

dir(objeto) devuelve una lista de lo que podes pedir

"""

def segunPattern(palabra, tipo):

	import pattern.web as patweb

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



	try:

		titulos = []
		for section in article.sections:
		     titulos.append(section.title)

		#Se recorre la lista de tipos y se pregunta si alguno coincide con los titulos

		encontrado = False

		print(tipoElegido) #borrar
		print(titulos) #borrar

		for x in tipoElegido:
			if(not encontrado == True):
				encontrado = (x in titulos)

	except AttributeError:

		#En caso de ser una palabra random devuelve None
		encontrado = None;

	return encontrado


print(segunPattern('gradísimo', 'Adjetivo'))
