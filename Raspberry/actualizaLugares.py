import PySimpleGUI as sg
import json
import time
from os import getcwd
from os.path import join
from datetime import date

def crearLayout (lugar):
    """Crea el layout que muestra mientras actualiza los datos"""

    layoutNuevo = [
                    [sg.T('Actualizando datos para: ')],
                    [sg.T(lugar, font = ('Arial', 15))],
                    [sg.T('Tiempo hasta la proxima actualizacion: 60', key = 'textoTiempo')],
                    [sg.ProgressBar(60, orientation='h', size=(20, 20), key='progressbar')],
                    [sg.Button('Parar')]
                ]
    return layoutNuevo

""" MODULO PARA EL SENSOR DE TEMPERATURA """
#import Adafruit_DHT

### CLASE SENSOR TEMPERATURA ###
"""class Temperatura:
    def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
        # Usamos el DHT11 que es compatible con el DHT12
        self._sensor = sensor
        self._data_pin = pin
    def datos_sensor(self):
        humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
        return {'temperatura': temperatura, 'humedad': humedad}"""

try:
    archivo = join(getcwd(),'Archivos','datosTemperatura.json')#LA RUTA DEL ARCHIVO
    datosJson = open(archivo, 'r', encoding="utf8") #ABRE EL ARCHIVO EN MODO LECTURA
    sensor = json.load(datosJson) #LEE LOS DATOS Y LOS GUARDA EN SENSOR
except FileNotFoundError:
    sensor = {"lugar ejemplo": [
    {
        "fecha": "2019-07-15",
        "temperatura": 1,
        "humedad": 70
    }
    ]
    }

layout = [
            [sg.T('Seleccionar lugar actual: ')],
            [sg.InputCombo(list(sensor.keys()), readonly = True, key = 'inputCombo', default_value=""), sg.B('Seleccionar'), sg.B('Eliminar')],
            [sg.Input(size=(20,1),do_not_clear=False, key = 'inputAgregar'),sg.B('Agregar')],
            [sg.T("-" * 60)],
            [sg.T('Seleccione un lugar: ', font = ('Arial', 15))],
            [sg.T('-', size = (10,1),font = ('Arial', 20), key = 'textoLugar')],
            [sg.T("")],
            [sg.B('Tomar temperatura y humedad', key = 'actualizar')],
            [sg.B('Salir')]
        ]


window = sg.Window('Temperatura y humedad').Layout(layout)

while True:
    button, values = window.Read()

    if button is None or button == 'Salir':
        break

    if (button == 'Eliminar'):
        try:
            del sensor[values['inputCombo']]
        except KeyError:
            sg.Popup('Seleccionar antes el lugar a eliminar', title = 'Advertencia')
        window.FindElement('inputCombo').Update(values = list(sensor.keys()))

    elif (button == 'Agregar'):

        #Valores en blanco
        datos = {}
        datos['temperatura'] = 0
        datos['humedad'] = 0
        datos['fecha'] = ""

        sensor[values['inputAgregar']] = [datos] #Carga los datos en el diccionario
        window.FindElement('inputCombo').Update(values = list(sensor.keys()))


    elif (button == 'actualizar'):
        window.Hide()

        try:
            #temp = Temperatura() #Descomentar

            #Apenas entra actualiza los datos
            datos = {} #Borrar
            #datos = temp.datos_sensor() #Descomentar
            datos['fecha'] = str(date.today())
            datos['temperatura'] = 10 #Borrar
            datos['humedad'] = 50 #Borrar

            #Lo agrega al json
            sensor[values['inputCombo']].append(datos)

            #Si tiene mas de 10 registros elimina el registro más viejo
            if (len(sensor[values['inputCombo']]) > 10):
                del sensor[values['inputCombo']][0]

            #Luego, abre una interfaz y va actualizando los datos cada minuto
            #interfaz
            layoutActualizar = crearLayout(values['inputCombo'])
            windowActualizar = sg.Window('Actualizando datos...').Layout(layoutActualizar)

            segundo_inicial = time.time() #Inicio contador de tiempo

            while True:

                button2, values2 = windowActualizar.Read(timeout = 0)

                segundo_actual = int(time.time() - segundo_inicial) #Actualizo la diferencia entre el segundo que empezó y el segundo actual

                windowActualizar.FindElement('progressbar').UpdateBar(segundo_actual)
                windowActualizar.FindElement('textoTiempo').Update('Tiempo hasta la proxima actualizacion: ' +  str(60 - segundo_actual))

                if(segundo_actual == 60):
                    #Si pasaron 60 segundos actualiza los datos
                    datos = {} #Borrar
                    #datos = temp.datos_sensor() #Descomentar
                    datos['fecha'] = str(date.today())
                    datos['temperatura'] = 20 #Borrar
                    datos['humedad'] = 70 #Borrar
                    sensor[values['inputCombo']].append(datos)
                    if (len(sensor[values['inputCombo']]) > 10):
                        del sensor[values['inputCombo']][0]

                    segundo_inicial = time.time() #Reinicio contador de tiempo

                if button2 is None or button2 == 'Parar':
                    break

            windowActualizar.Close()
        except KeyError:
            sg.Popup('El lugar seleccionado ya fue borrado previamente, por favor ingrese uno nuevo o eliga otro.', title = 'Advertencia')
        window.UnHide()

    elif (button == 'Seleccionar'):
        window.FindElement('textoLugar').Update(values['inputCombo'])


#Cierra la ventana y el archivo JSON
window.Close()
#Como no nos funcionó el modo lectura/escritura (r+)
#decidimos cerrar el archivo de lectura y abrirlo de nuevo para escribirlo
datosJson.close()

#Vuelve a abrir el Json para guardar los cambios
datosJson = open(archivo, 'w', encoding = "utf8")
json.dump(sensor, datosJson, indent = 4)
datosJson.close()
