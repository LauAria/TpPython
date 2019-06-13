#Funciones que pueden ser útiles para el manejo de ventanas window.Refresh(), windows(keep_on_top = True), window.Disable() window.Disappear(), Reappear() window.Hide(), UnHide()

import PySimpleGUI as sg
import buscador
import random
import os
import json

#Constantes
#valores por defecto para el json (por si se cierra el programa sin completar los datos)
try:
    archivo = open (os.path.join(os.getcwd(),"Archivos","datosConfig.json"), "r")
    datos = json.load(archivo)
    archivo.close()
except:
    sg.Popup('No se pudo importar la configuración', title = 'Aviso')
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
    datos['definicionTodosSustantivos'] = {}
    datos['definicionTodosAdjetivos'] = {}
    datos['definicionTodosVerbos'] = {}
    datos['definicionSustantivos'] = {}
    datos['definicionAdjetivos'] = {}
    datos['definicionVerbos'] = {}

listaNula = ['0']
tipografias = ['Garamond', 'Helvetica', 'Courier', 'Fixedsys', 'Times', 'Verdana']

#funciones

def abrirVentanaTipografia(window):
    """funcion que esconde la ventana actual (pasada por parámetro), y abre la ventana que nos permite elegir
    el formato de palabra y la orientación de la sopa de letras"""

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
    """Funcion que carga el color elegido al tipo que se le pasa como parámetro, comprobando que no sea muy claro"""

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
    """funcion que agrega una palabra a la lista del tipo que le pasemos. Usa funciones de otro .py para
    comprobar que la palabra existe y es del tipo especificado"""

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
            datos['definicionTodos' + tipoCS][palabra] = definicion
            global window
            global values
            window.FindElement('listbox' + tipoCS).Update(values = datos[tipoS])
            window.FindElement('spin' + tipoCS).Update(values = list(map(lambda x: x + 1, (range(len(datos[tipoS]))))))

def eliminar(tipo):
    """funcion que elimina una palabra ya cargada, se le pasa el tipo para saber de cual lista borrar"""

    #me guardo el tipo en diferentes formatos
    tipoC = tipo.capitalize()
    tipoS = tipo + 's'
    tipoCS = tipoC + 's'

    try:
        global values
        palabra = values['listbox' + tipoCS][0]
        global datos
        datos[tipoS].remove(palabra)
        del datos['definicionTodos' + tipoCS][palabra]
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

    lista = lista[:]
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
            [sg.Listbox(values = datos['sustantivos'], size=(15, 6), key = 'listboxSustantivos'), sg.T('Cantidad: '),
            sg.Spin(values = listaNula + list(map(lambda x: x + 1, (range(len(datos['sustantivos']))))), key = 'spinSustantivos', initial_value = datos['cantSustantivos'])],
            [sg.Button('Eliminar sustantivo', key = 'eliminarSustantivo')],
            [sg.T('-----------------------')],
            [sg.B('Cargar cantidad', key = 'cantSustantivos')],
            [sg.T('Cargado!', visible = False, key = 'cargadoSustantivos')],
            [sg.T('-----------------------')],
            [sg.ColorChooserButton('Seleccionar color', key = 'colorSustantivos'), sg.B('Cargar color', key = 'cargarColorSustantivos')]
        ]

column2 = [
            [sg.T('Adjetivos', font = ('Arial', 12), key = 'tituloAdjetivos')],
            [sg.Button('Agregar adjetivos', key = 'agregarAdjetivo')],
            [sg.Listbox(values = datos['adjetivos'], size=(15, 6), key = 'listboxAdjetivos'), sg.T('Cantidad: '),
            sg.Spin(values = listaNula + list(map(lambda x: x + 1, (range(len(datos['adjetivos']))))), key = 'spinAdjetivos', initial_value = datos['cantAdjetivos'])],
            [sg.Button('Eliminar adjetivos', key = 'eliminarAdjetivo')],
            [sg.T('-----------------------')],
            [sg.B('Cargar cantidad', key = 'cantAdjetivos')],
            [sg.T('Cargado!', visible = False, key = 'cargadoAdjetivos')],
            [sg.T('-----------------------')],
            [sg.ColorChooserButton('Seleccionar color', key = 'colorAdjetivos'), sg.B('Cargar color', key = 'cargarColorAdjetivos')]

        ]

column3 = [
            [sg.T('Verbos', font = ('Arial', 12), key = 'tituloVerbos')],
            [sg.Button('Agregar verbos', key = 'agregarVerbo')],
            [sg.Listbox(values = datos['verbos'], size=(15, 6), key = 'listboxVerbos'), sg.T('Cantidad: '),
            sg.Spin(values = listaNula + list(map(lambda x: x + 1, (range(len(datos['verbos']))))), key = 'spinVerbos', initial_value = datos['cantVerbos'])],
            [sg.Button('Eliminar verbos', key = 'eliminarVerbo')],
            [sg.T('-----------------------')],
            [sg.B('Cargar cantidad', key = 'cantVerbos')],
            [sg.T('Cargado!', visible = False, key = 'cargadoVerbos')],
            [sg.T('-----------------------')],
            [sg.ColorChooserButton('Seleccionar color', key = 'colorVerbos'), sg.B('Cargar color', key = 'cargarColorVerbos')]
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
                     [sg.T('Configuración', font = ('Arial', 20))],
                     [sg.Column(column1, key = 'columnaSustantivos'), sg.Column(column2, key = 'columnaAdjetivos'),
                      sg.Column(column3, key = 'columnaVerbos')],
                     [sg.T('-------------------------------------------')],
                     [sg.B('Configurar formato y orientación', key = 'config')],
                     [sg.B('Guardar configuración', key = 'guardar')]
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

    #cargar cantidad elegida
    elif (button == 'cantSustantivos'):
        datos['cantSustantivos'] = values['spinSustantivos']
        window.FindElement('cargadoSustantivos').Update(visible = True)

    elif (button == 'cantAdjetivos'):
        datos['cantAdjetivos'] = values['spinAdjetivos']
        window.FindElement('cargadoAdjetivos').Update(visible = True)

    elif (button == 'cantVerbos'):
        datos['cantVerbos'] = values['spinVerbos']
        window.FindElement('cargadoVerbos').Update(visible = True)

    #abrir ventaja de tipografia, mayus y minus y vertical o horizontal
    elif (button == 'config'):
        abrirVentanaTipografia(window)

    #compruebo que la cantidad de palabras sea mayor a 3 y menor a 10, si cumple con esto cierro la ventana
    elif (button == 'guardar'):
        if(int(datos['cantSustantivos']) + int(datos['cantAdjetivos']) + int(datos['cantVerbos']) > 10):
            sg.Popup('La cantidad de palabras seleccionadas es muy grande, disminuya la cantidad.', title = 'Advertencia')
            window.FindElement('cargadoSustantivos').Update(visible = False)
            window.FindElement('cargadoAdjetivos').Update(visible = False)
            window.FindElement('cargadoVerbos').Update(visible = False)
        elif(int(datos['cantSustantivos']) + int(datos['cantAdjetivos']) + int(datos['cantVerbos']) < 3):
            sg.Popup('La cantidad de palabras seleccionadas es muy chica, aumente la cantidad.', title = 'Advertencia')
            window.FindElement('cargadoSustantivos').Update(visible = False)
            window.FindElement('cargadoAdjetivos').Update(visible = False)
            window.FindElement('cargadoVerbos').Update(visible = False)
        else:
            #Elijo sustantivos, adjetivos y verbos
            datos['sustantivosElegidos'], datos['definicionSustantivos'] = filtrarSegunCantidad(datos['sustantivos'], datos['definicionTodosSustantivos'], datos['cantSustantivos'])
            datos['adjetivosElegidos'], datos['definicionAdjetivos'] = filtrarSegunCantidad(datos['adjetivos'], datos['definicionTodosAdjetivos'], datos['cantAdjetivos'])
            datos['verbosElegidos'], datos['definicionVerbos'] = filtrarSegunCantidad(datos['verbos'], datos['definicionTodosVerbos'], datos['cantVerbos'])

            #Creo el path
            path = os.path.join(os.getcwd(), 'Archivos')
            path = os.path.join(path, 'datosConfig.json')

            #Escribo el json
            archivo = open(path, 'w')
            json.dump(datos, archivo, indent = 4)
            archivo.close()
            sg.Popup('Cambios guardados!', title = 'Aviso')
            break

    else:
        sg.Popup('No se guardaron los cambios!', title = 'Advertencia')
        break
