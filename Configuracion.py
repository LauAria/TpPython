# usar elemento Spin para seleccionar la cantidad de sustantivos, adjetivos o verbos que se van a poner en la sopa de letras

import PySimpleGUI as sg

#Constantes
palabras = ['casa', 'auto', 'grande', 'rapido', 'juega', 'corre']

sustantivos = ['casa', 'auto']
adjetivos = ['grande', 'rapido']
verbos = ['juega', 'corre']
tipografias = ['Helvética', 'Futura', 'Avant Garde', 'Garamond', 'Bodoni', 'Franklin Gothic', 'Myriad', 'Bickham Script', 'Avenir', 'Trajan']

descripcionSustantivos = {}
descripcionAdjetivos = {}
descripcionVerbos = {}



definiciones = ['dice hola', 'dice como', 'dico estas']

menu_def = [['Abrir', ['Juego', 'Configuración']], ['Seleccionar', ['Tipografia']]]

#funciones

def abrirVentanaSustantivo(palabra, descripcion, reporte):
	#docstring
	palabra = ''
	descripcion = ''
	reporte = ''
	ventanaSustantivo = sg.Window('Seleccionar palabra').Layout(pidePalabra)

	while True:
		button, values = ventanaSustantivo.Read()
		if (button == 'ok'):
			#Aqui compruebo que la palabra sea la deseada (sustantivo, adjetivo o verbo) y devuelvo el reporte y descripcion,
			#en caso de que la palabra no sea válida devuelvo un string vacio
			palabra = values['palabraIngresada']
			break
		else:
			break
	ventanaSustantivo.Close()
	return (palabra, descripcion, reporte)

def abrirVentanaAdjetivo(palabra, descripcion, reporte):
	#docstring
	palabra = ''
	descripcion = ''
	reporte = ''
	ventanaAdjetivo = sg.Window('Seleccionar palabra').Layout(pidePalabra)

	while True:
		button, values = ventanaAdjetivo.Read()
		if (button == 'ok'):
			#Aqui compruebo que la palabra sea la deseada (sustantivo, adjetivo o verbo) y devuelvo el reporte y descripcion,
			#en caso de que la palabra no sea válida devuelvo un string vacio
			palabra = values['palabraIngresada']
			break
		else:
			break
	ventanaAdjetivo.Close()
	return (palabra, descripcion, reporte)

def abrirVentanaVerbo(palabra, descripcion, reporte):
	#docstring
	palabra = ''
	descripcion = ''
	reporte = ''
	ventanaVerbo = sg.Window('Seleccionar palabra').Layout(pidePalabra)

	while True:
		button, values = ventanaVerbo.Read()
		if (button == 'ok'):
			#Aqui compruebo que la palabra sea la deseada (sustantivo, adjetivo o verbo) y devuelvo el reporte y descripcion,
			#en caso de que la palabra no sea válida devuelvo un string vacio
			palabra = values['palabraIngresada']
			break
		else:
			break
	ventanaVerbo.Close()
	return (palabra, descripcion, reporte)

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

	#inicializo las variables para poder llamar a las funciones (no estoy seguro que las funciones devuelvan el dato, creo que se pasa por valor)
	palabra = ''
	descripcion = ''
	reporte = ''
	#botones de agregado
	if (button == 'agregarSustantivo'):
		palabra, descripcion, reporte = abrirVentanaSustantivo(palabra, descripcion, reporte) #abre una ventana que pide un sustantivo y si es correcto (comprobando con pattern y wiktionary) la devuelve
		if (palabra != ''):
			if (reporte != ''):
				sg.Popup(reporte)
			palabras.append(palabra)
			sustantivos.append(palabra)
			descripcionSustantivos[palabra] = descripcion
			window.FindElement('listboxSustantivos').Update(values = sustantivos)
			window.FindElement('spinSustantivos').Update(values = list(map(lambda x: x + 1, (range(len(sustantivos))))))


	elif (button == 'agregarAdjetivo'):
		palabra, descripcion, reporte = abrirVentanaAdjetivo(palabra, descripcion, reporte)
		if (palabra != ''):
			if (reporte != ''):
				sg.Popup(reporte)
			palabras.append(palabra)
			adjetivos.append(palabra)
			descripcionAdjetivos[palabra] = descripcion
			window.FindElement('listboxAdjetivos').Update(values = adjetivos)
			window.FindElement('spinAdjetivos').Update(values = list(map(lambda x: x + 1, (range(len(adjetivos))))))

	elif (button == 'agregarVerbo'):
		palabra, descripcion, reporte = abrirVentanaVerbo(palabra, descripcion, reporte)
		if (palabra != ''):
			if (reporte != ''):
				sg.Popup(reporte)
			palabras.append(palabra)
			verbos.append(palabra)
			descripcionVerbos[palabra] = descripcion
			window.FindElement('listboxVerbos').Update(values = verbos)
			window.FindElement('spinVerbos').Update(values = list(map(lambda x: x + 1, (range(len(verbos))))))
		
	#botones de borrado

	elif (button == 'eliminarSustantivo'):
		try:
			palabra = values['listboxSustantivos'][0]
			palabras.remove(palabra)
			sustantivos.remove(palabra)
			#del descripcionSustantivos[palabra] ;lo comento por ahora porque todavia no lo estoy cargando
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
			palabras.remove(palabra)
			adjetivos.remove(palabra)
			#del descripcionAdjetivos[palabra] ;lo comento por ahora porque todavia no lo estoy cargando
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
			palabras.remove(palabra)
			verbos.remove(palabra)
			#del descripcionVerbos[palabra] ;lo comento por ahora porque todavia no lo estoy cargando
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