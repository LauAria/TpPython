import PySimpleGUI as sg
import json
from os import getcwd
from os.path import join

### MODULOS PARA LA MATRIZ DE LED ###
#from luma.led_matrix.device import max7219
#from luma.core.interface.serial import spi, noop
#from luma.core.render import canvas
#from luma.core.virtual import viewport
#from luma.core.legacy import text, show_message
#from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

### MODULOS PARA EL SENSOR DE TEMPERATURA ###



### CLASE MATRIZ ###
class Matriz:
    def __init__(self, numero_matrices=1, orientacion=0,rotacion=0, ancho=8, alto=8):
        self.font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT,LCD_FONT]
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, width=ancho, height=alto, cascaded=numero_matrices, rotate=rotacion)
    def mostrar_mensaje(self, msg, delay=0.1, font=1):
        show_message(self.device, msg, fill="white",font=proportional(self.font[font]),scroll_delay=delay)

archivo = join(getcwd(),'Archivos','datosTemperatura.json')#LA RUTA DEL ARCHIVO
print(archivo)
datos = open(archivo, 'r', encoding="utf8") #ABRE EL ARCHIVO EN MODO LECTURA
sensor = {}

layout = [
            [sg.T('Seleccionar lugar: ')],
            [sg.InputCombo(sensor.keys(), key = 'inputCombo')],
            [sg.B('Actualizar temperatura', key = 'actualizarLugar'), sg.B('Mostrar', key = 'mostrarLugar')],
            [sg.T('Lugar: - ', key = 'Tlugar', font = ('Arial', 20))],
            [sg.T('Temperatura: - ', key = 'Ttemp'), sg.T('Humedad: - ', key = 'Thum')]
        ]

window = sg.Window('Temperatura y humedad').Layout(layout)

while True:
    button, values = window.Read()
    if button is None or button == 'Salir':
        break
    if (button == 'actualizarLugar'):
        print('entro')
    if (button == 'mostrarLugar'):
        window.FindElement('Tlugar').Update('Lugar: ' + values['inputCombo'])
        window.FindElement('Ttemp').Update('Temperatura: ' + int(sensor[values['inputCombo']]['temperatura']))
        window.FindElement('Thum').Update('Humedad: ' + int(sensor[values['inputCombo']]['temperatura']))


window.close()
#guardar los datos en el json
