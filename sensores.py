import PySimpleGUI as sg
import json

#importar sensor de datosTemperatura.json
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

    if (button == 'mostrarLugar'):
        window.FindElement('Tlugar').Update('Lugar: ' + values['inputCombo'])
        window.FindElement('Ttemp').Update('Temperatura: ' + int(sensor[values['inputCombo']]['temperatura']))
        window.FindElement('Thum').Update('Humedad: ' + int(sensor[values['inputCombo']]['temperatura']))

    #elif (button == 'actualizarLugar'):
    else:
        break

window.close()
#guardar los datos en el json
