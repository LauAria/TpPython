
##################################################
#####             SOPA DE LETRAS             #####
##################################################

def SopaDeLetras(orientacion='',Csus='',Cver='',Cadj='',tipografia='',mayus='',ayuda='',sustantivos=[],verbos=[],adjetivos=[],defSustantivos={},defVerbos={},defAdjetivos={}):
    import PySimpleGUI as sg
    import random
    from Funciones.funcionesSopa import PalabraMasLarga,AcomodarPalabrasHorizontales,AcomodarPalabrasVerticales,dibujarSopaDeLetras

    ##########################################################################################################################################################################
    #####   CREA LA ESTRUCTURA diccionarioCoordenadas QUE TIENE TODAS LAS COORDENADAS DE TODOS LOS CUADRADOS, CON SU POSICION COMO CLAVE; E INICIALIZACION DE VARIABLES  #####
    ##########################################################################################################################################################################

    InfoMax = PalabraMasLarga(sustantivos,verbos,adjetivos) #DEVUELVE UNA LISTA CON EL NUMERO DE LA PALABRA MAS LARGA Y LA CANTIDAD DE PALABRAS
    Palabras = {Csus: sustantivos,Cver: verbos,Cadj: adjetivos} #JUNTO TODAS LAS PALABRAS EN ESTE DICCIONARIO SEPARADAS SEGUN SU COLOR
    # PONE LAS PALABRAS EN MINUSCULAS O MAYUSCULAS SEGUN CORRESPONDA
    for i in Palabras:
        if (mayus == 'Mayusculas'):
            lista = list(map(lambda x : x.upper(),Palabras[i]))
        else:
            lista = list(map(lambda x : x.lower(),Palabras[i]))
        Palabras[i] = lista
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

    #### BOTON DE AYUDA HABILITADO O DESHABILITADO ####
    if (ayuda == 'Sin ayuda'):
        menuAyuda = sg.Submit('Ayuda',button_color=('black','white'),key='ayuda',size=(10,1),disabled=True)
    else:
        menuAyuda = sg.Submit('Ayuda',button_color=('black','white'),key='ayuda',size=(10,1))

    #### CONFIGURAR STRINGS PARA MOSTRAR AYUDA ####
    #Juntos los datos y los diccionarios y mezclo la lista para que las ayudas no sigan un patrón
    listaTotal = sustantivos + adjetivos + verbos
    random.shuffle(listaTotal)

    dicTotal = dict(defSustantivos)
    dicTotal.update(defVerbos)
    dicTotal.update(defAdjetivos)


    palabrasStr = '\n'.join(listaTotal)
    definicionesStr = ''
    for x in dicTotal.keys():
        definicionesStr = definicionesStr + 'DEFINICION: \n\n'
        definicionesStr = definicionesStr + dicTotal[x]
        definicionesStr = definicionesStr + '\n--------------------------------\n'

    ##################################################
    #####                 INTERFAZ               #####
    ##################################################

    layout = [
                [sg.Text('Palabras en: '+str(orientacion),font=(tipografia, 11),size=(25,1)),menuAyuda],
                [sg.Text('_'  *int(sizeSopa/7))],
                [sg.Text('Cantidad de sustantivos: '+str(cantPalabras[0]),font=(tipografia, 11)),sg.Text('Cantidad de verbos: '+str(cantPalabras[1]),font=(tipografia, 11))],
                [sg.Text('Cantidad de adjetivos: '+str(cantPalabras[2]),font=(tipografia, 11))],
    			[sg.Graph(canvas_size=(sizeSopa, sizeSopa), graph_bottom_left=(0,0), graph_top_right=(sizeSopa, sizeSopa), background_color='white',
                key='graph',enable_events=True,change_submits=False,drag_submits=False)],
                [sg.Submit('Pintar sustantivos',button_color=('black',Csus),key='sus'),sg.Submit('Pintar verbos',button_color=('black',Cver),key='ver'),
                    sg.Submit('Pintar adjetivos',button_color=('black',Cadj),key='adj'),sg.Submit('Comprobar',button_color=('black','white'))],
                [sg.Submit('Salir',button_color=('white','black'))]
             ]

    window = sg.Window('Sopa de letras', layout).Finalize()

    graph = window.FindElement('graph')


    ##################################################
    #####   ACOMODA LA POSICION DE LAS PALABRAS  #####
    ##################################################

    posicion = [] #LISTA CON LAS LETRAS Y SUS POSICIONES EN LA SOPA DE LETRAS
    CopyPosicion = [] #PARA HACER UNA COPIA DE POSICION
    repetidas = {} #DICCIONARIO CON LA COORDENADA DE ALTO O ANCHO COMO CLAVE, ESTO PARA PROCESAR TANTO LAS REPETIDAS EN LAS HORIZONTALES COMO LAS VERTICALES

    if (orientacion == 'Horizontal'):
        AcomodarPalabrasHorizontales(posicion,repetidas,Palabras,tamañoDeSopa)
    else:
        AcomodarPalabrasVerticales(posicion,repetidas,Palabras,tamañoDeSopa)

    ##################################################
    #####         CREA LA SOPA DE LETRAS         #####
    ##################################################

    CopyPosicion = list(map(lambda x : x.copy(),posicion)) #UNA COPIA DE POSICION, PORQUE ESTA VA A SER MODIFICADA
    letras = {} #CREO UN DICCIONARIO QUE TIENE COMO CLAVES LAS COORDENADAS CONCATENADAS COMO STRING Y EL VALOR ES LA LETRA
    letrasSeleccionadas = {} #CREO UN DICCIONARIO QUE TIENE COMO CLAVES LA POSICION DE LA LETRA, ESTE SERVIRA PARA COMPROBAR LA SOPA

    dibujarSopaDeLetras(tamañoDeSopa,mayus,graph,tipografia,orientacion,CopyPosicion,letras,letrasSeleccionadas,diccionarioCoordenadas)

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
        ####       AYUDA       ####
        if (button == 'ayuda'):
            window.Hide()
            if (ayuda == 'Mostrar definiciones'):
                sg.PopupScrolled(definicionesStr, size=(100, 30), title='Definiciones')
            else:
                sg.PopupScrolled(palabrasStr, size=(20, 20), title='Lista de palabras')
        window.UnHide()
        ###########################
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
                        ok = list(filter(lambda x : (posX,posY) == x,letrasSeleccionadas.keys())) #GUARDA LA LETRA QUE PERTENECE AL DE UNA PALABRA
                        if (ok != []):
                            letrasSeleccionadas[(posX,posY)][1] = False #PONE EN FALSE LA LETRA SELECCIONADA QUE PERTENECE A UNA PALABRA VALIDA
                    else:
                        try:
                            graph.DrawRectangle((x1,y1), (x2,y2), fill_color=ColorSelect, line_color='black') #SI NO FUE PRESIONADA DIBUJA SEGUN EL COLOR SELECCIONADO
                            letrasPresionadas.add(str(posX)+str(posY)) #AGREGA LA COORDENADA PRESIONADA
                            ok = list(filter(lambda x : (posX,posY) == x and ColorSelect == letrasSeleccionadas[x][2],letrasSeleccionadas.keys())) #GUARDA LA LETRA QUE PERTENECE AL DE UNA PALABRA
                            if (ok != []):
                                letrasSeleccionadas[(posX,posY)][1] = True #PONE EN TRUE LA LETRA SELECCIONADA QUE PERTENECE A UNA PALABRA VALIDA
                        except NameError:
                            sg.Popup('Elegí un color antes de empezar a jugar',title='ERROR')
                    graph.DrawText('{}'.format(letras[str(x1)+str(y1)+str(x2)+str(y2)]),(x2+25,y2+25),font=tipografia) #ESCRIBE LA LETRA QUE PETERNECIA A ESA COORDENADA
            except IndexError:
                pass
        if (button == 'Comprobar'):
            palabrasAcertadas = []
            palabrasErradas = []
            aux = list(map(lambda x : x.copy(),posicion)) #UNA COPIA DE LA LISTA ORIGINAL, ESTA SE VA A MODIFICAR
            letrasErradas = letrasPresionadas.copy() #UNA COPIA DEL CONJUNTO CON LAS COORDENADAS CONCATENADAS DE LAS LETRAS PRESIONADAS
            for i in aux: #ITERO POR CADA SUBLISTA DE AUX
                ok = True
                for j in range(len(i[0])): #ITERO LA CANTIDAD DE VECES SEGUN LA LONGITUD DE LA PALABRA
                    if (letrasSeleccionadas[(i[1],i[2])][1] == False): #ME FIJO SI EN ESA POSICION NO SE HIZO CLICK
                        ok = False
                    else:
                        letrasErradas.remove(str(i[1])+str(i[2])) #BORRA EN LA ESTRUCTURA LA COORDENADA QUE PERTENECE A UNA PALABRA SELECCIONADA
                    if (orientacion == 'Horizontal'): #SI ES HORIZONTAL, SUMO SU VALOR DE X PARA AVANZAR Y FIJARME LA POSICION DE SU SIGUIENTE LETRA
                        i[2] = i[2]+1
                    else: #SI ES VERTICAL, SUMO SU VALOR DE Y PARA AVANZAR Y FIJARME LA POSICION DE SU SIGUIENTE LETRA
                        i[1] = i[1]+1
                if (ok):
                    palabrasAcertadas.append(i[0]) #AGREGO LA PALABRA SI ESTAN TODOS SUS CARACTERES SELECCIONADOS
                else:
                    palabrasErradas.append(i[0]) #AGREGO LA PALABRA SI NO ESTAN TODOS SUS CARACTERES SELECCIONADOS
            if (palabrasErradas == []) and (letrasErradas == set()): #SI LA LISTA DE PALABRAS ERRADAS TIENE ALGO, LA SOPA NO SE COMPLETO
                sg.Popup('La sopa se completó correctamente',title='FELICIDADES')
            elif (palabrasErradas == []):
                cantidad = len(letrasErradas)
                sg.Popup('Las palabras fueron marcadas correctamente, pero hay marcadas '+str(cantidad)+' letras de más',title='INCORRECTO')
            elif (letrasErradas == set()):
                cantidad = len(palabrasErradas)
                sg.Popup('La sopa no se completó correctamente','Faltan marcar correctamente: '+str(cantidad)+' palabras',title='INCORRECTO')
            else:
                cantidadPalabras = len(palabrasErradas)
                cantidadLetras = len(letrasErradas)
                sg.Popup('La sopa no se completó correctamente','Faltan marcar correctamente: '+str(cantidadPalabras)+' palabras',
                'Hay marcadas '+str(cantidadLetras)+' letras de más',title="INCORRECTO")
