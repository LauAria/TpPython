import PySimpleGUI as sg
import json
from os import getcwd
from os.path import join

""" MODULOS PARA LA MATRIZ DE LED """
#from luma.led_matrix.device import max7219
#from luma.core.interface.serial import spi, noop
#from luma.core.render import canvas
#from luma.core.virtual import viewport
#from luma.core.legacy import text, show_message
#from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

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

### CLASE SENDOR SONIDO ###
"""class Sonido:
    def __init__(self, canal=22):
        self._canal = canal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._canal, GPIO.IN)
        # Desactivo las warnings por tener más de un circuito en la GPIO
        GPIO.setwarnings(False)
        GPIO.add_event_detect(self._canal, GPIO.RISING)
    def evento_detectado(self, funcion, temp, hum):
        if GPIO.event_detected(self._canal):
            funcion(temp, hum)"""

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
            [sg.T('Seleccionar lugar a mostrar: ')],
            [sg.InputCombo(list(sensor.keys()), key = 'inputCombo')],
            [sg.B('Salir')]
        ]

window = sg.Window('Temperatura y humedad').Layout(layout)

#sonido = Sonido()
while True:
    button, values = window.Read(timeout = 0)
    
    if button is None or button == 'Salir':
        break

    """ DETECTA SONIDO Y LO MUESTRA EN EL LED CON LA FUNCION MOSTRAR """
    try:
        print() #borrar
        #sonido.evento_detectado(mostrar, sensor[values['inputCombo']]['temperatura'], sensor[values['inputCombo']]['humedad'])
    except KeyError:
        sg.Popup('Seleccionar antes el lugar', title = 'Advertencia')


#Cierra la ventana y el archivo JSON
window.Close()
datosJson.close()
