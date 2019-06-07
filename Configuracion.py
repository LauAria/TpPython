# usar elemento Spin para seleccionar la cantidad de sustantivos, adjetivos o verbos que se van a poner en la sopa de letras

import PySimpleGUI as sg
import buscador

#Constantes

sustantivos = ['casa', 'auto']
adjetivos = ['grande', 'rapido']
verbos = ['juega', 'corre']
tipografias = ['Helvética', 'Futura', 'Avant Garde', 'Garamond', 'Bodoni', 'Franklin Gothic', 'Myriad', 'Bickham Script', 'Avenir', 'Trajan']

definicionSustantivos = {}
definicionAdjetivos = {}
definicionVerbos = {}



definiciones = ['dice hola', 'dice como', 'dico estas']

menu_def = [['Abrir', ['Juego', 'Configuración']], ['Seleccionar', ['Tipografia']]]

#funciones

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
			[sg.Listbox(values = sustantivos, size=(15, 6), key = 'listboxSustantivos'), sg.T('Cantidad: '), sg.Spin(values = list(map(lambda x: x + 1, (range(len(sustantivos))))), key = 'spinSustantivos', initial_value = '0')],
			[sg.Button('Eliminar sustantivo', key = 'eliminarSustantivo')],
			[sg.T('-----------------------')],
			[sg.ColorChooserButton('Seleccionar color', key = 'colorSustantivos'), sg.B('Cargar color', key = 'cargarColorSustantivos')],
			[sg.T('-----------------------')],
			[sg.B('Cargar cantidad')]
		]

column2 = [
			[sg.T('Adjetivos', font = ('Arial', 12), key = 'tituloAdjetivos')],
			[sg.Button('Agregar adjetivos', key = 'agregarAdjetivo')],
			[sg.Listbox(values = adjetivos, size=(15, 6), key = 'listboxAdjetivos'), sg.T('Cantidad: '), sg.Spin(values = list(map(lambda x: x + 1, (range(len(adjetivos))))), key = 'spinAdjetivos', initial_value = '0')],
			[sg.Button('Eliminar adjetivos', key = 'eliminarAdjetivo')],
			[sg.T('-----------------------')],
			[sg.ColorChooserButton('Seleccionar color', key = 'colorAdjetivos'), sg.B('Cargar color', key = 'cargarColorAdjetivos')],
			[sg.T('-----------------------')],
			[sg.B('Cargar cantidad')]
		]

column3 = [
			[sg.T('Verbos', font = ('Arial', 12), key = 'tituloVerbos')],
			[sg.Button('Agregar verbos', key = 'agregarVerbo')],
			[sg.Listbox(values = verbos, size=(15, 6), key = 'listboxVerbos'), sg.T('Cantidad: '), sg.Spin(values = list(map(lambda x: x + 1, (range(len(verbos))))), key = 'spinVerbos', initial_value = '0')],
			[sg.Button('Eliminar verbos', key = 'eliminarVerbo')],
			[sg.T('-----------------------')],
			[sg.ColorChooserButton('Seleccionar color', key = 'colorVerbos'), sg.B('Cargar color', key = 'cargarColorVerbos')],
			[sg.T('-----------------------')],
			[sg.B('Cargar cantidad')]
		]

columnaTipografia = [
				[sg.InputCombo(values = tipografias, size=(20, 1)), sg.B('Cargar', key = 'cargarTipo')]
			  ]


columnaMayus = [
					[sg.B('Mayúsculas', key = 'mayus')],
					[sg.B('Minúsculas', key = 'minus')],
					[sg.T('Texto de muestra', font = ('Arial', 12), key = 'textoPrueba')]
			   ]


columnaHorientacion = [
						[sg.B('Horizontal', key = 'Bhorizontal')],
						[sg.B('Vertical', key = 'Bvertical')],
						[sg.T('Horientación actual: horizontal')]
			 		  ]


layoutTipografia = [
		 				[sg.T('Tipografia, horientación y mayus', font = ('Arial', 20))],
		 				[sg.Column(columnaTipografia, key = 'columnaTipografia'), sg.Column(columnaMayus, key = 'columnaMayus'), sg.Column(columnaHorientacion, key = 'columnaHorientacion')]
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
				sustantivos.append(palabra)
				definicionSustantivos[palabra] = definicion
				window.FindElement('listboxSustantivos').Update(values = sustantivos)
				window.FindElement('spinSustantivos').Update(values = list(map(lambda x: x + 1, (range(len(sustantivos))))))


	elif (button == 'agregarAdjetivo'):
		palabra = sg.PopupGetText('Ingrese el adjetivo:', title = 'Ingreso de palabra', font = ('Arial', 12))
		if(palabra != None):
			reporte, definicion = buscador.consultarPalabra(palabra, 'Adjetivo')

			sg.Popup(reporte, title = 'reporte')

			if(reporte != 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):
				if(reporte == 'El Wikcionario no aprobó la palabra, pero Pattern si.' or reporte == 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):
					definicion = pedirDefinicion()

				adjetivos.append(palabra)
				definicionAdjetivos[palabra] = definicion
				window.FindElement('listboxAdjetivos').Update(values = adjetivos)
				window.FindElement('spinAdjetivos').Update(values = list(map(lambda x: x + 1, (range(len(adjetivos))))))

	elif (button == 'agregarVerbo'):
		palabra = sg.PopupGetText('Ingrese el verbo:', title = 'Ingreso de palabra', font = ('Arial', 12))
		if(palabra != None):
			reporte, definicion = buscador.consultarPalabra(palabra, 'Verbo')

			sg.Popup(reporte, title = 'reporte')

			if(reporte != 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):
				if(reporte == 'El Wikcionario no aprobó la palabra, pero Pattern si.' or reporte == 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):
					definicion = pedirDefinicion()

				verbos.append(palabra)
				definicionVerbos[palabra] = definicion
				window.FindElement('listboxVerbos').Update(values = verbos)
				window.FindElement('spinVerbos').Update(values = list(map(lambda x: x + 1, (range(len(verbos))))))

	#botones de borrado

	elif (button == 'eliminarSustantivo'):
		try:
			palabra = values['listboxSustantivos'][0]
			sustantivos.remove(palabra)
			#del definicionSustantivos[palabra] ;lo comento por ahora porque todavia no lo estoy cargando
			window.FindElement('listboxSustantivos').Update(values = sustantivos)
			if (len(sustantivos) == 0):
				window.FindElement('spinSustantivos').Update(values = [0])
			else:
				window.FindElement('spinSustantivos').Update(values = list(map(lambda x: x + 1, (range(len(sustantivos))))))
		except IndexError:
			sg.Popup('No hay palabra que eliminar')

	elif (button == 'eliminarAdjetivo'):
		try:
			palabra = values['listboxAdjetivos'][0]
			adjetivos.remove(palabra)
			#del definicionAdjetivos[palabra] ;lo comento por ahora porque todavia no lo estoy cargando
			window.FindElement('listboxAdjetivos').Update(values = adjetivos)
			if (len(adjetivos) == 0):
				window.FindElement('spinAdjetivos').Update(values = [0])
			else:
				window.FindElement('spinAdjetivos').Update(values = list(map(lambda x: x + 1, (range(len(adjetivos))))))
		except IndexError:
			sg.Popup('No hay palabra que eliminar')

	elif (button == 'eliminarVerbo'):
		try:
			palabra = values['listboxVerbos'][0]
			verbos.remove(palabra)
			#del definicionVerbos[palabra] ;lo comento por ahora porque todavia no lo estoy cargando
			window.FindElement('listboxVerbos').Update(values = verbos)
			if (len(verbos) == 0):
				window.FindElement('spinVerbos').Update(values = [0])
			else:
				window.FindElement('spinVerbos').Update(values = list(map(lambda x: x + 1, (range(len(verbos))))))
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
		else:
			sg.Popup('Tiene que elegir un color antes.')


		#Falta que ande el boton "cargar cantidad", para evitar se rompa siempre comprobar que la cantidad de palabras seleccionadas exista

	elif (button == 'Tipografia'):
		windowTipografia = sg.Window('Programa').Layout(layoutTipografia)



	else:
		break
