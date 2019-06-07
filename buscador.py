import PySimpleGUI as sg
import string
import pattern.es as pattes

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
		#Si no encuentra el articulo en Wiktionary devuelve encontrado como False
		encontrado = False
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

#--------------------------------------------------------------------------------------------------------------
def segunPattern(palabra, tipo):

	tipo = tipo.lower()
	tipo = tipo.capitalize()

	#Tipo de palabras segun Pattern
	clasifSustantivos = ['NN', 'NNS', 'NNP', 'NNPS']
	clasifAdjetivos = ['JJ', 'JJR', 'JJS']
	clasifVerbos = ['MD', 'VB', 'VBZ', 'VBP', 'VBD', 'VBN', 'VBG']

	#con el .parse obtengo una lista con propiedades de la palabra y me guardo el tipo (propiedades[1])
	propiedades = pattes.parse(palabra)
	propiedades = propiedades.split('/')
	clasificacion = propiedades[1]

	#pregunto si coincide
	if(clasificacion in clasifSustantivos):
		resultado = 'Sustantivo'
	elif(clasificacion in clasifAdjetivos):
		resultado = 'Adjetivo'
	elif(clasificacion in clasifVerbos):
		resultado = 'Verbo'

	if (resultado == tipo):
		return True
	else:
		return False

#----------------------------------------------------------------------------------------------------------------

def prepararPalabra(palabra, tipo):

	reporte = ''
	definicion = ''

	#Busco la palabra en Wiktionary o en Pattern
	resultadoWik = segunWiktionary(palabra, tipo)
	resultadoPat = segunPattern(palabra, tipo)

	#Segun los resultados que me arrojen las funciones genero el reporte
	if(resultadoWik[0]):
		if(resultadoPat):
			reporte = 'Tanto el Wikcionario como Pattern aprobaron la palabra.'
			sg.Popup(reporte, title = 'reporte')
		else:
			reporte = 'El Wikcionario aprobó la palabra, pero Pattern no.'
			sg.Popup(reporte, title = 'reporte')

		#Si Wiktionary aprueba la palabra uso la definicion de esa pagina
		definicion = resultadoWik[1]
	else:
		if (resultadoPat):
			#Si solo Pattern aprueba la palabra se pide una descripcion
			reporte = 'El Wikcionario no aprobó la palabra, pero Pattern si.'
			sg.Popup(reporte, title = 'reporte')
			definicion = sg.PopupGetText('Por favor ingrese una definicion de la palabra: ' + palabra, title = 'Ingreso de descripcion')
			while(definicion == None):
				definicion = sg.PopupGetText('No se escribió una definición. Por favor ingrese una definicion de la palabra: ' + palabra, title = 'Ingreso de descripcion')
			definicion = definicion + ' (descripcion brindada por el profesor)'
		else:
			#En caso de que la palabra no se apruebe por ninguno de los dos sistemas la descripcion queda en blanco
			reporte = 'Ni el Wikcionario ni Pattern aprobaron la palabra.'
			sg.Popup(reporte, title = 'reporte')

	return reporte, definicion

print(prepararPalabra('carrera', 'sustantivo'))
