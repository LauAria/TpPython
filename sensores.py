import PySimpleGUI as sg
import json
from os import getcwd
from os.path import join
from datetime import date

""" MODULOS PARA LA MATRIZ DE LED """
#from luma.led_matrix.device import max7219
#from luma.core.interface.serial import spi, noop
#from luma.core.render import canvas
#from luma.core.virtual import viewport
#from luma.core.legacy import text, show_message
#from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

""" MODULO PARA EL SENSOR DE TEMPERATURA """
#import Adafruit_DHT

""" MODULO PARA EL SENSOR DE SONIDO """
#import RPi.GPIO as GPIO


### CLASE MATRIZ ###
"""class Matriz:
    def __init__(self, numero_matrices=1, orientacion=0,rotacion=0, ancho=8, alto=8):
        self.font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT,LCD_FONT]
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, width=ancho, height=alto, cascaded=numero_matrices, rotate=rotacion)
    def mostrar_mensaje(self, msg, delay=0.1, font=1):
        show_message(self.device, msg, fill="white",font=proportional(self.font[font]),scroll_delay=delay)"""

### CLASE SENSOR TEMPERATURA ###
"""class Temperatura:
    def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
        # Usamos el DHT11 que es compatible con el DHT12
        self._sensor = sensor
        self._data_pin = pin
    def datos_sensor(self):
        humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
        return {'temperatura': temperatura, 'humedad': humedad}"""

### CLASE SENDOR SONIDO ###
"""class Sonido:
    def __init__(self, canal=22):
        self._canal = canal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._canal, GPIO.IN)
        # Desactivo las warnings por tener más de un circuito en la GPIO
        GPIO.setwarnings(False)
        GPIO.add_event_detect(self._canal, GPIO.RISING)
    def evento_detectado(self, funcion):
        if GPIO.event_detected(self._canal):
            funcion()"""

### MUESTRA LOS VALORES EN EL LED ###
#def mostrar(temp,hum):
"""Muestra los datos parados como parametros en dos matrices leds"""
    #matriz = Matriz(numero_matrices=2, ancho=16)
    #matriz.mostrar_mensaje(str(temp) + ' ' + str(hum), delay=0.3)

try:
    archivo = join(getcwd(),'Archivos','datosTemperatura.json')#LA RUTA DEL ARCHIVO
    datosJson = open(archivo, 'r', encoding="utf8") #ABRE EL ARCHIVO EN MODO LECTURA
    sensor = json.load(datosJson) #LEE LOS DATOS Y LOS GUARDA EN SENSOR
except FileNotFoundError:
    sensor = {}

layout = [
            [sg.T('Seleccionar lugar: ')],
            [sg.InputCombo(list(sensor.keys()), key = 'inputCombo'),sg.B('Eliminar')],
            [sg.Input(size=(20,1),do_not_clear=False),sg.B('Agregar')],
            [sg.B('Actualizar temperatura', key = 'actualizarLugar'), sg.B('Mostrar', key = 'mostrarLugar')],
            [sg.T('Lugar: - ', key = 'Tlugar', font = ('Arial', 20),size=(15,1))],
            [sg.T('Temperatura: - ', key = 'Ttemp',size=(15,1)), sg.T('Humedad: - ', key = 'Thum',size=(15,1))]
        ]

window = sg.Window('Temperatura y humedad').Layout(layout)

#sonido = Sonido()
while True:
    button, values = window.Read()
    if button is None or button == 'Salir':
        break
    if (button == 'Eliminar'):
        try:
            sensor.pop(values['inputCombo'])
        except KeyError:
            sg.Popup('Seleccionar antes el lugar', title = 'Advertencia')
    if (button == 'Agregar'):
        datos = {}

        """ DETECTA EL VALOR DEL SENSOR """
        #temp = Temperatura()
        #datos = temp.datos_sensor()

        datos['temperatura'] = 50 #ESTE DATO NO SE CARGA A MANO
        datos['humedad'] = 100 #ESTE DATO NO SE CARGA A MANO
        datos['fecha'] = str(date.today())
        sensor[values[0]] = datos #AGREGAR EL VALOR EN EL LUGAR CORRECTO
    if (button == 'actualizarLugar'):
        try:
            datos = {}

            """ DETECTA EL VALOR DEL SENSOR """
            #temp = Temperatura()
            #datos = temp.datos_sensor()

            datos['temperatura'] = 50 #ESTE DATO NO SE CARGA A MANO
            datos['humedad'] = 100 #ESTE DATO NO SE CARGA A MANO
            datos['fecha'] = str(date.today())
            sensor[values['inputCombo']] = datos #ACTUALIZA EL VALOR EN EL LUGAR CORRECTO
        except KeyError:
            sg.Popup('Seleccionar antes el lugar', title = 'Advertencia')

    """ DETECTA SONIDO Y LO MUESTRA EN EL LED CON LA FUNCION MOSTRAR """
    try:
        print() #borrar
        #sonido.evento_detectado(mostrar(sensor[values['inputCombo']]['temperatura'],sensor[values['inputCombo']]['humedad']))
    except KeyError:
        sg.Popup('Seleccionar antes el lugar', title = 'Advertencia')

    ### ESTA PARTE CON EL SENSOR SE TIENE QUE BORRAR ###
    if (button == 'mostrarLugar'):
        window.FindElement('Tlugar').Update('Lugar: '+ values['inputCombo'])
        window.FindElement('Ttemp').Update('Temperatura: ' + str(sensor[values['inputCombo']]['temperatura']))
        window.FindElement('Thum').Update('Humedad: ' + str(sensor[values['inputCombo']]['humedad']))


#Cierra la ventana y el archivo JSON
window.Close()
#Como no nos funcionó el modo lectura/escritura (r+)
#decidimos cerrar el archivo de lectura y abrirlo de nuevo para escribirlo
datosJson.close()

#Vuelve a abrir el Json para guardar los cambios
datosJson = open(archivo, 'w', encoding="utf8")
json.dump(sensor,datosJson,indent=4)
datosJson.close()
