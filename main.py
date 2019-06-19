import json
from os import getcwd
from os.path import join
import PySimpleGUI as sg
from Funciones.sopa import SopaDeLetras

try: #EXCEPCION POR SI NO SE GENERO NINGUN ARCHIVO DE CONFIGURACION
    archivo = join(join(getcwd(),'Archivos'),'datosConfig.json')#LA RUTA DEL ARCHIVO
    config = open(archivo, 'r', encoding="utf8") #ABRE EL ARCHIVO EN MODO LECTURA
    data = json.load(config) #LEE LOS DATOS Y LOS GUARDA EN DATA
    #EJECUTA LA SOPA DE LETRAS CON LOS DATOS DEL JSON
    SopaDeLetras(orientacion=data['orientacion'],tipografia=data['tipografia'],mayus=data['mayus'],Csus=data['colorSustantivos'],
    Cadj=data['colorAdjetivos'],Cver=data['colorVerbos'],sustantivos=data['sustantivosElegidos'],verbos=data['verbosElegidos'],
    adjetivos=data['adjetivosElegidos'],ayuda=data['ayuda'],defSustantivos=data['definicionSustantivos'],defVerbos=data['definicionVerbos'],defAdjetivos=data['definicionAdjetivos'])
    #----------------------------------------------------------------------------------------------------------------------------#
    config.close() #CIERRO EL ARCHIVO
except FileNotFoundError:
    sg.Popup('La configuración no existe','Configurar el juego antes de iniciar',title="ERROR")
except KeyError:
    sg.Popup('Cargar una configuración del juego antes de iniciar',title="ERROR")
