import json
from os import getcwd
from os.path import join

try: #EXCEPCION POR SI NO SE GENERO NINGUN ARCHIVO DE CONFIGURACION
    archivo = join(join(getcwd(),'Archivos'),'datosConfig.json')#LA RUTA DEL ARCHIVO
    config = open(archivo, 'r', encoding="utf8") #ABRE EL ARCHIVO EN MODO LECTURA
    data = json.load(config) #LEE LOS DATOS Y LOS GUARDA EN DATA
    Defecto = False #VARIABLE PARA SABER SI USAR VALORES POR DEFECTO O NO
except FileNotFoundError:
    Defecto = True #VARIABLE PARA SABER SI USAR VALORES POR DEFECTO O NO

def SopaDeLetras(sustantivos=['PROFESOR','CASA'],verbos=['CORRER','LLOVER'],adjetivos=['GORDO','FEO'],orientacion='Horizontal',
Csus='#2E64FE',Cver='#FE2E2E',Cadj='#01DF3A',tipografia='Calibri',mayus='Mayusculas'):
    import PySimpleGUI as sg
    from Funciones.funcionesSopa import PalabraMasLarga,AcomodarPalabrasHorizontales,AcomodarPalabrasVerticales,dibujarSopaDeLetras

    ##########################################################################################################################################################################
    #####   CREA LA ESTRUCTURA diccionarioCoordenadas QUE TIENE TODAS LAS COORDENADAS DE TODOS LOS CUADRADOS, CON SU POSICION COMO CLAVE; E INICIALIZACION DE VARIABLES  #####
    ##########################################################################################################################################################################

    InfoMax = PalabraMasLarga(sustantivos,verbos,adjetivos) #DEVUELVE UNA LISTA CON EL NUMERO DE LA PALABRA MAS LARGA Y LA CANTIDAD DE PALABRAS
    Palabras = {Csus: sustantivos,Cver: verbos,Cadj: adjetivos} #JUNTO TODAS LAS PALABRAS EN ESTE DICCIONARIO SEPARADAS SEGUN SU COLOR
    cantPalabras = [] #GUARDA LA CANTIDAD DE PALABRAS SEGUN TIPO, 0=SUSTANTIVOS, 1=VERBOS, 2=ADJETIVOS
    for i in Palabras:
        cantPalabras.append(len(Palabras[i]))
    diccionarioCoordenadas = {} #DICCIONARIO CON LAS CLAVES COMO SI FUERAN LAS POSICIONES EN LA MATRIZ
    aux = -1
    tamañoDeSopa = InfoMax[0]+(int(InfoMax[1]/2))+1 #ES EL RESULTADO DE LO GRANDE QUE VA A SER LA SOPA DE LETRAS
    sizeSopa = 50*tamañoDeSopa #TAMAÑO DE LA GRILLA DONDE SE VA A GRAFICAR
    size = int((50*tamañoDeSopa)/50) #LONGITUD DE LA SOPA POR CUADRADO
    alto_fin = sizeSopa+49
    alto_inicio = sizeSopa
    for x in range(size): #VALOR DE COLUMNAS
        limite = x
        for i in range(size): #VALOR DE FILAS
            if (aux < limite):
                top_right = 50
                alto_fin = alto_fin-50
                top_left = 1
                alto_inicio = alto_inicio-50
                lista = [top_right,alto_fin,top_left,alto_inicio] #LISTA DE COORDENADAS
            diccionarioCoordenadas[(x,i)] = (lista[0],lista[1],lista[2],lista[3]) #AGREGA LAS COORDENADAS
            lista[2] = lista[2]+50 #AUMENTA LA COORDENADA top_left
            lista[0] = lista[0]+50 #AUMENTA LA COORDENADA top_right
            aux = x

    ##################################################
    #####                 INTERFAZ               #####
    ##################################################

    layout = [
                [sg.Text('Cantidad de sustantivos: '+str(cantPalabras[0]),font=(tipografia, 11))],
                [sg.Text('Cantidad de verbos: '+str(cantPalabras[1]),font=(tipografia, 11))],
                [sg.Text('Cantidad de adjetivos: '+str(cantPalabras[2]),font=(tipografia, 11))],
    			[sg.Graph(canvas_size=(sizeSopa, sizeSopa), graph_bottom_left=(0,0), graph_top_right=(sizeSopa, sizeSopa), background_color='white',
                key='graph',enable_events=True,change_submits=False,drag_submits=False)],
                [sg.Submit('Comprobar',button_color=('black','white')),sg.Text('',size=(11,1)),sg.Submit('Pintar sustantivos',button_color=('black',Csus),key='sus'),
                    sg.Submit('Pintar verbos',button_color=('black',Cver),key='ver'),sg.Submit('Pintar adjetivos',button_color=('black',Cadj),key='adj')],
                [sg.Submit('Salir')]
             ]

    window = sg.Window('Sopa de letras', layout).Finalize()

    graph = window.FindElement('graph')


    ##################################################
    #####   ACOMODA LA POSICION DE LAS PALABRAS  #####
    ##################################################

    posicion = [] #LISTA CON LAS LETRAS Y SUS POSICIONES EN LA SOPA DE LETRAS

    repetidas = {} #DICCIONARIO CON LA COORDENADA DE ALTO O ANCHO COMO CLAVE, ESTO PARA PROCESAR TANTO LAS REPETIDAS EN LAS HORIZONTALES COMO LAS VERTICALES

    if (orientacion == 'Horizontal'):
        AcomodarPalabrasHorizontales(posicion,repetidas,Palabras,tamañoDeSopa)
    else:
        AcomodarPalabrasVerticales(posicion,repetidas,Palabras,tamañoDeSopa)

    ##################################################
    #####         CREA LA SOPA DE LETRAS         #####
    ##################################################

    letras = {} #CREO UN DICCIONARIO QUE TIENE COMO CLAVES LAS COORDENADAS CONCATENADAS COMO STRING Y EL VALOR ES LA LETRA
    letrasSeleccionadas = {} #CREO UN DICCIONARIO QUE TIENE COMO CLAVES LA POSICION DE LA LETRA, ESTE SERVIRA PARA COMPROBAR LA SOPA

    dibujarSopaDeLetras(tamañoDeSopa,mayus,graph,tipografia,orientacion,posicion,letras,letrasSeleccionadas,diccionarioCoordenadas)

    ##################################################
    #####           EVENTOS EN LA INTERFAZ       #####
    ##################################################

    letrasPresionadas = set() #CONJUNTO CON LAS COORDENDAS DE LAS LETRAS PRESIONADAS CONCATENADAS COMO STRING
    interacciones = 0 #VARIABLE AUXILIAR PARA NO DETECTAR EL SEGUNDO EVENTO AL SOLTAR EL CLICK
    while True:
        button, values = window.Read()
        if button is None or button == 'Salir':
            break
        #### SELECCION DE COLOR ####
        if (button == 'sus'):
            ColorSelect = Csus
        if (button == 'ver'):
            ColorSelect = Cver
        if (button == 'adj'):
            ColorSelect = Cadj
        ############################
        if (button == 'graph'):
            try:
                interacciones = interacciones+1
                if (interacciones%2 != 0):
                    #FILTRA SEGUN EL CLICK QUE SE HIZO, EN QUE CUADRADO DE LA SOPA SE HIZO CLICK
                    coor = list(filter(lambda x : (values['graph'][0] <= x[1][0]) and (values['graph'][0] >= x[1][2]) and (values['graph'][1] <= x[1][1])
                     and (values['graph'][1] >= x[1][3]),diccionarioCoordenadas.items()))
                    #SE GUARDA LAS COORDENADAS
                    posX = coor[0][0][0]
                    posY = coor[0][0][1]
                    x1 = coor[0][1][0]
                    y1 = coor[0][1][1]
                    x2 = coor[0][1][2]
                    y2 = coor[0][1][3]
                    if (str(posX)+str(posY) in letrasPresionadas): #SI ESA COORDENADA QUE SE PRESIONO YA FUE PRESIONADA ANTES
                        graph.DrawRectangle((x1,y1), (x2,y2), fill_color='white', line_color='black') #DIBUJA OTRA VEZ EL RECTANGULO BLANCO
                        letrasPresionadas.remove(str(posX)+str(posY)) #BORRA LA LETRA PRESIONADA
                        ok = list(filter(lambda x : (posX,posY) == x,letrasSeleccionadas.keys()))
                        if (ok != []):
                            letrasSeleccionadas[(posX,posY)][1] = False
                    else:
                        try:
                            graph.DrawRectangle((x1,y1), (x2,y2), fill_color=ColorSelect, line_color='black') #SI NO FUE PRESIONADA DIBUJA SEGUN EL COLOR SELECCIONADO
                            letrasPresionadas.add(str(posX)+str(posY)) #AGREGA LA COORDENADA COMO PRESIONADA
                            ok = list(filter(lambda x : (posX,posY) == x and ColorSelect == letrasSeleccionadas[x][2],letrasSeleccionadas.keys()))
                            if (ok != []):
                                letrasSeleccionadas[(posX,posY)][1] = True
                        except NameError:
                            sg.Popup('Elegi un color antes de empezar a jugar',title='ERROR')
                    graph.DrawText('{}'.format(letras[str(x1)+str(y1)+str(x2)+str(y2)]),(x2+25,y2+25),font=tipografia) #ESCRIBE LA LETRA QUE PETERNECIA A ESA COORDENADA
            except IndexError:
                pass
        if (button == 'Comprobar'):
            comprobar = list(map(lambda x : x[1],letrasSeleccionadas.values()))
            if (False in comprobar):
                sg.Popup('La sopa no se completo correctamente',title='INCORRECTO')
            else:
                sg.Popup('La sopa se completo correctamente',title='EUREKA')

if (Defecto):
    SopaDeLetras()
else:
    SopaDeLetras(orientacion=data['orientacion'],tipografia=data['tipografia'],mayus=data['mayus'],Csus=data['colorSustantivos'],Cadj=data['colorAdjetivos'],
    Cver=data['colorVerbos'],sustantivos=data['sustantivosElegidos'],verbos=data['verbosElegidos'],adjetivos=data['adjetivosElegidos'])
