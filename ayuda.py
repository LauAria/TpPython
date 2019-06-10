datos = {
    "orientacion": "Horizontal",
    "tipografia": "Courier",
    "mayus": "Mayusculas",
    "cantSustantivos": "1",
    "cantAdjetivos": "2",
    "cantVerbos": "1",
    "colorSustantivos": "#00ff00",
    "colorAdjetivos": "#0000a0",
    "colorVerbos": "#ff0080",
    "sustantivos": [
        "asdasda",
        "auto"
    ],
    "adjetivos": [],
    "verbos": [
        "correr",
        "tocar"
    ],
    "definicionSustantivos": {
        "pan": "1 Gastronom\u00eda.Masa a base de harina y agua endurecida por cocci\u00f3n al horno.\n* Hip\u00f3nimos: baguete, perruna, peso de artifara, sopa.\n* Ejemplo: No me gusta el pan de centeno.\n\n2 Gastronom\u00eda.Masa sobada y delicado de aceite o manteca, usada en la elaboraci\u00f3n de pasteles y empanadas.\n\n3Otra masa de esta forma.\n* Ejemplo:\n\n\u00abPan de higos, de jab\u00f3n, de sal\u00bb\n\n4Sustento diario.\n* Ejemplo: Trabajo para ganarme el pan.\n\n5 Gastronom\u00eda.Trigo.\n* Ejemplo:\n\n\u201cSe convert\u00edan en el destino preferente del terrazgo, al igual que los ejidos y bald\u00edos concejiles donde se cultivaban pan y legumbres tras largas barbecheras\u201d.Lanza, Ram\u00f3n (1991). Poblaci\u00f3n y crecimiento econ\u00f3mico de Cantabria en antiguo r\u00e9gimen. Santander: Servicio de Publicaciones. Universidad de Cantabria, p\u00e1g. 179.\n\n6Hoja muy fina de oro, plata o de otros metales, que se usa para que una superficie tenga aspecto de oro o plata.\n\n7\u00d3rgano sexual femenino.\n* \u00c1mbito: El Salvador, Nicaragua."
    },
    "definicionAdjetivos": {
        "feo": "1Que carece de belleza o hermosura. [1]\n* Sin\u00f3nimos: antiest\u00e9tico, bagarto, horrible\n* Ant\u00f3nimos: bello, bonito, hermoso, lindo\n\n2De aspecto deplorable, que causa mala impresi\u00f3n.\n* Sin\u00f3nimos: de mal augurio, de mala educaci\u00f3n, deplorable, malo\n\n3Que causa horror o aversi\u00f3n. [1]\n* Sin\u00f3nimos: desagradable, horroroso\n\n4En los juegos de naipes, carta que no da buen juego.",
        "lindo": "1Que es agradable a la vista o al \u00e1nimo, con un toque de ternura. [2]\n* Sin\u00f3nimos: agraciado, bello, bonito, hermoso, primoroso.\n\n2Que provoca un sentimiento de ternura por su gracia.\n* Relacionados: exquisito, primoroso.\n* Derivado: lindeza, lindura."
    },
    "definicionVerbos": {
        "jugar": "1Realizar actividades divertidas\n* Sin\u00f3nimo: divertirse.\n* Ejemplos:\n\n\"Ni\u00f1os, id a jugar.\"\n\n2No tomar un asunto en serio o tratar a una persona sin la debida consideraci\u00f3n y respeto que se merece.\n* Ejemplo:\n\n\"No juegues con tu salud, mira que lo que ten\u00edas era muy grave.\""
    },
    "sustantivosElegidos": [
        "pan"
    ],
    "adjetivosElegidos": [
        "feo",
        "lindo"
    ],
    "verbosElegidos": [
        "jugar"
    ]
}

import PySimpleGUI as sg
import random

#Juntos los datos y los diccionarios y mezclo la lista para que las ayudas no sigan un patrón
listaTotal = datos['sustantivosElegidos'] + datos['adjetivosElegidos'] + datos['verbosElegidos']
random.shuffle(listaTotal)

dicTotal = dict(datos['definicionSustantivos'])
dicTotal.update(datos['definicionAdjetivos'])
dicTotal.update(datos['definicionVerbos'])


palabrasStr = '\n'.join(listaTotal)
definicionesStr = ''
for x in dicTotal.keys():
    definicionesStr = definicionesStr + 'DEFINICION: \n\n'
    definicionesStr = definicionesStr + dicTotal[x]
    definicionesStr = definicionesStr + '\n--------------------------------\n'


menu_def = [['Ayuda', ['Lista de palabras', 'Definiciones']]]

layout = [
            [sg.Menu(menu_def)],
            [sg.T('Nada', font = ('Arial', 50))]
         ]

window = sg.Window('prueba', resizable=True).Layout(layout)


while True:
    button, values = window.Read()

    if (button == 'Definiciones'):
        sg.PopupScrolled(definicionesStr, size=(100, 30), location=(250, 150), title='Definiciones')

    elif (button == 'Lista de palabras'):
        sg.PopupScrolled(palabrasStr, size=(20, 20), location=(250, 150), title='Lista de palabras')

    else:
        break
