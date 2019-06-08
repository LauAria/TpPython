#Funciones que pueden ser útiles para el manejo de ventanas window.Refresh(), windows(keep_on_top = True), window.Disable() window.Disappear(), Reappear() window.Hide(), UnHide()

import PySimpleGUI as sg
import buscador
import random
import json

#Constantes
#valores por defecto para el json (por si se cierra el programa sin completar los datos)
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
datos['definicionSustantivos'] = {}
datos['definicionAdjetivos'] = {}
datos['definicionVerbos'] = {}


tipografias = ['Garamond', 'Helvetica', 'Courier', 'Fixedsys', 'Times', 'Verdana']
menu_def = [['Abrir', ['Juego', 'Configuración']], ['Seleccionar', ['Tipografia']]]

#funciones

def abrirVentanaTipografia(window):
    window.Hide()
    global layoutTipografia
    global datos
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

def cargarColor(tipo):

    #me guardo el tipo en diferentes formatos
    tipoC = tipo.capitalize()
    tipoS = tipo + 's'
    tipoCS = tipoC + 's'

    global values
    colorElegido = values['color' + tipoCS]
    if(colorElegido != '' and colorElegido != 'None'):
        #saco algunos colores que son muy claros y no se llega a leer bien
        if(colorElegido == '#ffffff' or colorElegido == '#c0c0c0' or colorElegido == '#ffff80' or colorElegido == '#ffff00' or colorElegido == '#80ffff' or colorElegido == '#00ffff'):
            sg.Popup('El color elegido es muy claro y puede dificultar la legibilidad del texto, elija un color mas oscuro')
        else:
            global window
            window.FindElement('titulo' + tipoCS).Update(text_color = colorElegido)
            window.FindElement('cargarColor' + tipoCS).Update(button_color= ('white',colorElegido))
            datos['color' + tipoCS] = colorElegido
    else:
        sg.Popup('Tiene que elegir un color antes.')

def agregar(tipo):

    #me guardo el tipo en diferentes formatos
    tipoC = tipo.capitalize()
    tipoS = tipo + 's'
    tipoCS = tipoC + 's'

    #Pop up para ingresar la palabra
    palabra = sg.PopupGetText('Ingrese el ' + tipo + ':', title = 'Ingreso de palabra', font = ('Arial', 12))

    #compruebo que se haya ingresado una palabra
    if(palabra != None):

        #Busco la palabra en Wiktionary y Pattern e imprimo el reporte
        reporte, definicion = buscador.consultarPalabra(palabra, tipoC)

        sg.Popup(reporte, title = 'reporte')

        if(reporte != 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):

            #Si existe la palabra pero solo en Pattern pido una definicion
            if(reporte == 'El Wikcionario no aprobó la palabra, pero Pattern si.' or reporte == 'Ni el Wikcionario ni Pattern aprobaron la palabra.'):
                definicion = pedirDefinicion(palabra)

            #Cargo todos los datos
            global datos
            datos[tipoS].append(palabra)
            datos['definicion' + tipoCS][palabra] = definicion
            global window
            global values
            window.FindElement('listbox' + tipoCS).Update(values = datos[tipoS])
            window.FindElement('spin' + tipoCS).Update(values = list(map(lambda x: x + 1, (range(len(datos[tipoS]))))))

def eliminar(tipo):

    #me guardo el tipo en diferentes formatos
    tipoC = tipo.capitalize()
    tipoS = tipo + 's'
    tipoCS = tipoC + 's'

    try:
        global values
        palabra = values['listbox' + tipoCS][0]
        global datos
        datos[tipoS].remove(palabra)
        del datos['definicion' + tipoCS][palabra]
        global window
        window.FindElement('listbox' + tipoCS).Update(values = datos[tipoS])
        if (len(datos[tipoS]) == 0):
            window.FindElement('spin' + tipoCS).Update(values = [0])
        else:
            window.FindElement('spin' + tipoCS).Update(values = list(map(lambda x: x + 1, (range(len(datos[tipoS]))))))
    except IndexError:
        sg.Popup('No hay palabra que eliminar')


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

def pedirDefinicion(palabra):
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
        agregar('sustantivo')

    elif (button == 'agregarAdjetivo'):
        agregar('adjetivo')

    elif (button == 'agregarVerbo'):
        agregar('verbo')

    #botones de borrado

    elif (button == 'eliminarSustantivo'):
        eliminar('sustantivo')

    elif (button == 'eliminarAdjetivo'):
        eliminar('adjetivo')

    elif (button == 'eliminarVerbo'):
        eliminar('verbo')

    #Selectores de color
    elif (button == 'cargarColorSustantivos'):
        cargarColor('sustantivo')

    elif (button == 'cargarColorAdjetivos'):
        cargarColor('adjetivo')

    elif (button == 'cargarColorVerbos'):
        cargarColor('verbo')

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
        abrirVentanaTipografia(window)

    else:
        break

datos['sustantivosElegidos'], datos['definicionSustantivos'] = filtrarSegunCantidad(datos['sustantivos'], datos['definicionSustantivos'], datos['cantSustantivos'])
datos['adjetivosElegidos'], datos['definicionAdjetivos'] = filtrarSegunCantidad(datos['adjetivos'], datos['definicionAdjetivos'], datos['cantAdjetivos'])
datos['verbosElegidos'], datos['definicionVerbos'] = filtrarSegunCantidad(datos['verbos'], datos['definicionVerbos'], datos['cantVerbos'])

archivo = open('datosConfig.json', 'w')
json.dump(datos, archivo, indent = 4)

#Falta pasar todos los botones que son iguales a funciones para que queda mas lindo el codigo
