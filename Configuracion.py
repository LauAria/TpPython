#Funciones que pueden ser útiles para el manejo de ventanas window.Refresh(), windows(keep_on_top = True), window.Disable() window.Disappear(), Reappear() window.Hide(), UnHide()

import PySimpleGUI as sg
import buscador
import random
import json

#Constantes

datos = {}
datos['orientacion'] = 'Horizontal'
datos['tipografia'] = 'Arial'
datos['mayus'] = 'Mayusculas'
datos['cantSustantivos'] = 0
datos['cantAdjetivos'] = 0
datos['cantVerbos'] = 0
datos['colorSustantivos'] = '#00ff00'
datos['colorAdjetivos'] = '#0000ff'
datos['colorVerbos'] = '#ff0000'
datos['sustantivos'] = []
datos['adjetivos'] = []
datos['verbos'] = []
tipografias = ['Garamond', 'Helvetica', 'Courier', 'Fixedsys', 'Times', 'Verdana']

datos['definicionSustantivos'] = {}
datos['definicionAdjetivos'] = {}
datos['definicionVerbos'] = {}

menu_def = [['Abrir', ['Juego', 'Configuración']], ['Seleccionar', ['Tipografia']]]

#funciones

def filtrarSegunCantidad(lista, dic, cant):
	"""funcion que toma la lista de palabras, elige una cantidad de palabras random
	y las devuelve en una lista nueva, tambien actualiza el diccionario para que solo
	queden las claves de la lista"""

	listaRan = []
	dicRan = {}

	for x in range(int(cant)):
		elem = random.choice(lista)
		listaRan.append(elem)
		lista.remove(elem)

	for palabra in listaRan:
		dicRan[palabra] = dic[palabra]

	return listaRan, dicRan

def pedirDefinicion():
	definicion = sg.PopupGetText('Por favor ingrese una definicion de la palabra: ' + palabra, title = 'Ingreso de descripcion')
	while(definicion == None):
		definicion = sg.PopupGetText('No se escribió una definición. Por favor ingrese una definicion de la palabra: ' + palabra, title = 'Ingreso de descripcion')
	definicion = definicion + ' (descripcion brindada por el profesor)'
	return definicion

#layouts

pidePalabra = [
				[sg.T('Ingrese la palabra:'), sg.InputText('', key = 'palabraIngresada')],
				[sg.Button('Ok', key = 'ok'), sg.Button('Cancelar', key = 'cancelar')]
			]

column1 = [
			[sg.T('Sustantivos', font = ('Arial', 12), key = 'tituloSustantivos')],
			[sg.Button('Agregar sustantivo', key = 'agregarSustantivo')],
			[sg.Listbox(values = datos['sustantivos'], size=(15, 6), key = 'listboxSustantivos'), sg.T('Cantidad: '), sg.Spin(values = list(map(lambda x: x + 1, (range(len(datos['sustantivos']))))), key = 'spinSustantivos', initial_value = '0')],
			[sg.Button('Eliminar sustantivo', key = 'eliminarSustantivo')],
			[sg.T('-----------------------')],
			[sg.ColorChooserButton('Seleccionar color', key = 'colorSustantivos'), sg.B('Cargar color', key = 'cargarColorSustantivos')],
			[sg.T('-----------------------')],
			[sg.B('Cargar cantidad', key = 'cantSustantivos')],
			[sg.T('Cargado!', visible = False, key = 'cargadoSustantivos')]
		]

column2 = [
			[sg.T('Adjetivos', font = ('Arial', 12), key = 'tituloAdjetivos')],
			[sg.Button('Agregar adjetivos', key = 'agregarAdjetivo')],
			[sg.Listbox(values = datos['adjetivos'], size=(15, 6), key = 'listboxAdjetivos'), sg.T('Cantidad: '), sg.Spin(values = list(map(lambda x: x + 1, (range(len(datos['adjetivos']))))), key = 'spinAdjetivos', initial_value = '0')],
			[sg.Button('Eliminar adjetivos', key = 'eliminarAdjetivo')],
			[sg.T('-----------------------')],
			[sg.ColorChooserButton('Seleccionar color', key = 'colorAdjetivos'), sg.B('Cargar color', key = 'cargarColorAdjetivos')],
			[sg.T('-----------------------')],
			[sg.B('Cargar cantidad', key = 'cantAdjetivos')],
			[sg.T('Cargado!', visible = False, key = 'cargadoAdjetivos')]
		]

column3 = [
			[sg.T('Verbos', font = ('Arial', 12), key = 'tituloVerbos')],
			[sg.Button('Agregar verbos', key = 'agregarVerbo')],
			[sg.Listbox(values = datos['verbos'], size=(15, 6), key = 'listboxVerbos'), sg.T('Cantidad: '), sg.Spin(values = list(map(lambda x: x + 1, (range(len(datos['verbos']))))), key = 'spinVerbos', initial_value = '0')],
			[sg.Button('Eliminar verbos', key = 'eliminarVerbo')],
			[sg.T('-----------------------')],
			[sg.ColorChooserButton('Seleccionar color', key = 'colorVerbos'), sg.B('Cargar color', key = 'cargarColorVerbos')],
			[sg.T('-----------------------')],
			[sg.B('Cargar cantidad', key = 'cantVerbos')],
			[sg.T('Cargado!', visible = False, key = 'cargadoVerbos')]
		]

columnaTipografia = [
				[sg.InputCombo(values = tipografias, default_value='Helvetica',size=(20, 1), readonly=True, key = 'InputComboTipografias'), sg.B('Cargar', key = 'cargarTipo')]
			  ]


columnaMayus = [
					[sg.B('Mayúsculas', key = 'mayus')],
					[sg.B('Minúsculas', key = 'minus')],
			   ]


columnaOrientacion = [
						[sg.B('Horizontal', key = 'Bhorizontal')],
						[sg.B('Vertical', key = 'Bvertical')],
						[sg.T('Orientación actual: Horizontal', key = 'orientacionActual')]
			 		  ]


layoutTipografia = [
		 				[sg.T('Tipografia, orientación y mayus', font = ('Arial', 20))],
		 				[sg.Column(columnaTipografia, key = 'columnaTipografia'), sg.Column(columnaMayus, key = 'columnaMayus'),
						sg.Column(columnaOrientacion, key = 'columnaOrientacion')],
						[sg.T('TEXTO DE MUESTRA', font = ('Arial', 18), key = 'textoPrueba')],
						[sg.B('Listo', font = ('Arial', 13))]
				   ]

layoutPrincipal = [
		 			[sg.Menu(menu_def)],
		 			[sg.T('Configuración', font = ('Arial', 20))],
		 			[sg.Column(column1, key = 'columnaSustantivos'), sg.Column(column2, key = 'columnaAdjetivos'), sg.Column(column3, key = 'columnaVerbos')]
				]



window = sg.Window('Programa').Layout(layoutPrincipal)


while True:
	button, values = window.Read()

	#botones de agregado
	if (button == 'agregarSustantivo'):

		#Pop up para ingresar la palabra
		palabra = sg.PopupGetText('Ingrese el sustantivo:', title = 'Ingreso de palabra', font = ('Arial', 12))

		#compruebo que se haya ingresado una palabra
		if(palabra != None):

			#Busco la palabra en Wiktionary y Pattern e imprimo el reporte
			reporte, definicion = buscador.consultarPalabra(palabra, 'Sustantivo')

			sg.Popup(reporte, title = 'reporte')

			if(reporte != 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):

				#Si existe la palabra pero solo en Pattern pido una definicion
				if(reporte == 'El Wikcionario no aprobó la palabra, pero Pattern si.' or reporte == 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):
					definicion = pedirDefinicion()

				#Cargo todos los datos
				datos['sustantivos'].append(palabra)
				datos['definicionSustantivos'][palabra] = definicion
				window.FindElement('listboxSustantivos').Update(values = datos['sustantivos'])
				window.FindElement('spinSustantivos').Update(values = list(map(lambda x: x + 1, (range(len(datos['sustantivos']))))))


	elif (button == 'agregarAdjetivo'):
		palabra = sg.PopupGetText('Ingrese el adjetivo:', title = 'Ingreso de palabra', font = ('Arial', 12))
		if(palabra != None):
			reporte, definicion = buscador.consultarPalabra(palabra, 'Adjetivo')

			sg.Popup(reporte, title = 'reporte')

			if(reporte != 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):
				if(reporte == 'El Wikcionario no aprobó la palabra, pero Pattern si.' or reporte == 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):
					definicion = pedirDefinicion()

				datos['adjetivos'].append(palabra)
				datos['definicionAdjetivos'][palabra] = definicion
				window.FindElement('listboxAdjetivos').Update(values = datos['adjetivos'])
				window.FindElement('spinAdjetivos').Update(values = list(map(lambda x: x + 1, (range(len(datos['adjetivos']))))))

	elif (button == 'agregarVerbo'):
		palabra = sg.PopupGetText('Ingrese el verbo:', title = 'Ingreso de palabra', font = ('Arial', 12))
		if(palabra != None):
			reporte, definicion = buscador.consultarPalabra(palabra, 'Verbo')

			sg.Popup(reporte, title = 'reporte')

			if(reporte != 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):
				if(reporte == 'El Wikcionario no aprobó la palabra, pero Pattern si.' or reporte == 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):
					definicion = pedirDefinicion()

				datos['verbos'].append(palabra)
				datos['definicionVerbos'][palabra] = definicion
				window.FindElement('listboxVerbos').Update(values = datos['verbos'])
				window.FindElement('spinVerbos').Update(values = list(map(lambda x: x + 1, (range(len(datos['verbos']))))))

	#botones de borrado

	elif (button == 'eliminarSustantivo'):
		try:
			palabra = values['listboxSustantivos'][0]
			datos['sustantivos'].remove(palabra)
			#del definicionSustantivos[palabra] ;lo comento por ahora porque todavia no lo estoy cargando
			window.FindElement('listboxSustantivos').Update(values = datos['sustantivos'])
			if (len(datos['sustantivos']) == 0):
				window.FindElement('spinSustantivos').Update(values = [0])
			else:
				window.FindElement('spinSustantivos').Update(values = list(map(lambda x: x + 1, (range(len(datos['sustantivos']))))))
		except IndexError:
			sg.Popup('No hay palabra que eliminar')

	elif (button == 'eliminarAdjetivo'):
		try:
			palabra = values['listboxAdjetivos'][0]
			datos['adjetivos'].remove(palabra)
			#del definicionAdjetivos[palabra] ;lo comento por ahora porque todavia no lo estoy cargando
			window.FindElement('listboxAdjetivos').Update(values = datos['adjetivos'])
			if (len(datos['adjetivos']) == 0):
				window.FindElement('spinAdjetivos').Update(values = [0])
			else:
				window.FindElement('spinAdjetivos').Update(values = list(map(lambda x: x + 1, (range(len(datos['adjetivos']))))))
		except IndexError:
			sg.Popup('No hay palabra que eliminar')

	elif (button == 'eliminarVerbo'):
		try:
			palabra = values['listboxVerbos'][0]
			datos['verbos'].remove(palabra)
			#del definicionVerbos[palabra] ;lo comento por ahora porque todavia no lo estoy cargando
			window.FindElement('listboxVerbos').Update(values = datos['verbos'])
			if (len(datos['verbos']) == 0):
				window.FindElement('spinVerbos').Update(values = [0])
			else:
				window.FindElement('spinVerbos').Update(values = list(map(lambda x: x + 1, (range(len(datos['verbos']))))))
		except IndexError:
			sg.Popup('No hay palabra que eliminar')

	#Selectores de color
	elif (button == 'cargarColorSustantivos'):
		colorElegido = values['colorSustantivos']
		if(colorElegido != '' and colorElegido != 'None'):
			#saco algunos colores que son muy claros y no se llega a leer bien
			if(colorElegido == '#ffffff' or colorElegido == '#c0c0c0' or colorElegido == '#ffff80' or colorElegido == '#ffff00' or colorElegido == '#80ffff' or colorElegido == '#00ffff'):
				sg.Popup('El color elegido es muy claro y puede dificultar la legibilidad del texto, elija un color mas oscuro')
			else:
				window.FindElement('tituloSustantivos').Update(text_color = colorElegido)
				window.FindElement('cargarColorSustantivos').Update(button_color= ('white',colorElegido))
				datos['colorSustantivos'] = colorElegido
		else:
			sg.Popup('Tiene que elegir un color antes.')

	elif (button == 'cargarColorAdjetivos'):
		colorElegido = values['colorAdjetivos']
		if(colorElegido != '' and colorElegido != 'None'):
			#saco algunos colores que son muy claros y no se llega a leer bien
			if(colorElegido == '#ffffff' or colorElegido == '#c0c0c0' or colorElegido == '#ffff80' or colorElegido == '#ffff00' or colorElegido == '#80ffff' or colorElegido == '#00ffff'):
				sg.Popup('El color elegido es muy claro y puede dificultar la legibilidad del texto, elija un color mas oscuro')
			else:
				window.FindElement('tituloAdjetivos').Update(text_color = colorElegido)
				window.FindElement('cargarColorAdjetivos').Update(button_color= ('white',colorElegido))
				datos['colorAdjetivos'] = colorElegido
		else:
			sg.Popup('Tiene que elegir un color antes.')


	elif (button == 'cargarColorVerbos'):
		colorElegido = values['colorVerbos']
		if(colorElegido != '' and colorElegido != 'None'):
			#saco algunos colores que son muy claros y no se llega a leer bien
			if(colorElegido == '#ffffff' or colorElegido == '#c0c0c0' or colorElegido == '#ffff80' or colorElegido == '#ffff00' or colorElegido == '#80ffff' or colorElegido == '#00ffff'):
				sg.Popup('El color elegido es muy claro y puede dificultar la legibilidad del texto, elija un color mas oscuro')
			else:
				window.FindElement('tituloVerbos').Update(text_color = colorElegido)
				window.FindElement('cargarColorVerbos').Update(button_color= ('white',colorElegido))
				datos['colorVerbos'] = colorElegido
		else:
			sg.Popup('Tiene que elegir un color antes.')


		#Falta que ande el boton "cargar cantidad", para evitar se rompa siempre comprobar que la cantidad de palabras seleccionadas exista
	elif (button == 'cantSustantivos'):
		datos['cantSustantivos'] = values['spinSustantivos']
		window.FindElement('cargadoSustantivos').Update(visible = True)

	elif (button == 'cantAdjetivos'):
		datos['cantAdjetivos'] = values['spinAdjetivos']
		window.FindElement('cargadoAdjetivos').Update(visible = True)

	elif (button == 'cantVerbos'):
		datos['cantVerbos'] = values['spinVerbos']
		window.FindElement('cargadoVerbos').Update(visible = True)

	elif (button == 'Tipografia'):
		window.Hide()
		windowTipografia = sg.Window('Programa').Layout(layoutTipografia)
		while True:
			buttonT, valuesT = windowTipografia.Read()

			if(buttonT == 'mayus'):
				windowTipografia.FindElement('textoPrueba').Update('Texto de muestra'.upper())
				datos['mayus'] = 'Mayusculas'

			elif(buttonT == 'minus'):
				windowTipografia.FindElement('textoPrueba').Update('Texto de muestra'.lower())
				datos['mayus'] = 'Minusculas'

			elif(buttonT == 'Bhorizontal'):
				windowTipografia.FindElement('orientacionActual').Update('Orientación actual: Horizontal')
				datos['orientacion'] = 'Horizontal'

			elif(buttonT == 'Bvertical'):
				windowTipografia.FindElement('orientacionActual').Update('Orientación actual: Vertical')
				datos['orientacion'] = 'Vertical'

			elif(buttonT == 'cargarTipo'):
				datos['tipografia'] = valuesT['InputComboTipografias']
				windowTipografia.FindElement('textoPrueba').Update(font = (datos['tipografia'], 18))

			else:
				break

		windowTipografia.Close()
		window.UnHide()

	else:
		break

datos['sustantivosElegidos'], datos['definicionSustantivos'] = filtrarSegunCantidad(datos['sustantivos'], datos['definicionSustantivos'], datos['cantSustantivos'])
datos['adjetivosElegidos'], datos['definicionAdjetivos'] = filtrarSegunCantidad(datos['adjetivos'], datos['definicionAdjetivos'], datos['cantAdjetivos'])
datos['verbosElegidos'], datos['definicionVerbos'] = filtrarSegunCantidad(datos['verbos'], datos['definicionVerbos'], datos['cantVerbos'])

archivo = open('datosConfig.json', 'w')
json.dump(datos, archivo, indent = 4)

#Falta pasar todos los botones que son iguales a funciones para que queda mas lindo el codigo
