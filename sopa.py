
def SopaDeLetras(sustantivos=['NOSOTROS','ELLOS'],verbos=['CORRER','LLOVER'],adjetivos=['GORDO'],horizontal=True,Csus='#2E64FE',Cver='#FE2E2E',Cadj='#01DF3A'):
    import PySimpleGUI as sg
    import random
    import string

    def PalabraMasLarga(sus,verbos,adjetivos):
        info = [-1,0]
        for x in sus:
            info[1] = info[1]+1
            if (len(x) > info[0]):
                info[0] = len(x)
        for x in verbos:
            info[1] = info[1]+1
            if (len(x) > info[0]):
                info[0] = len(x)
        for x in adjetivos:
            info[1] = info[1]+1
            if (len(x) > info[0]):
                info[0] = len(x)
        return info

    InfoMax = PalabraMasLarga(sustantivos,verbos,adjetivos) #DEVUELVE UNA LISTA CON EL NUMERO DE LA PALABRA MAS LARGA Y LA CANTIDAD DE PALABRAS
    Palabras = sustantivos+verbos+adjetivos #JUNTO TODAS LAS PALABRAS EN ESTA LISTA
    coordenadas = []
    diccionarioCoordenadas = {} #DICCIONARIO CON LAS CLAVES COMO SI FUERAN LAS POSICIONES EN LA MATRIZ
    aux = -1
    tamañoDeSopa = InfoMax[0]+(int(InfoMax[1]/2)) #ES EL RESULTADO DE LO GRANDE QUE VA A SER LA SOPA DE LETRAS
    sizeSopa = 50*tamañoDeSopa
    size = int((50*tamañoDeSopa)/50)
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
            coordenadas.append([lista[0],lista[1],lista[2],lista[3]]) #AGREGA LAS COORDENADAS
            diccionarioCoordenadas[(x,i)] = (lista[0],lista[1],lista[2],lista[3])
            lista[2] = lista[2]+50 #AUMENTA LA COORDENADA top_left
            lista[0] = lista[0]+50 #AUMENTA LA COORDENADA top_right
            aux = x

    layout = [
    			[sg.Graph(canvas_size=(sizeSopa, sizeSopa), graph_bottom_left=(0,0), graph_top_right=(sizeSopa, sizeSopa), background_color='white',
                key='graph',enable_events=True,change_submits=False,drag_submits=False)],
                [sg.Submit('Comprobar'),sg.Text('',size=(11,1)),sg.Submit('Pintar sustantivos',button_color=('black',Csus),key='sus'),
                    sg.Submit('Pintar verbos',button_color=('black',Cver),key='ver'),sg.Submit('Pintar adjetivos',button_color=('black',Cadj),key='adj')],
                [sg.Submit('Salir')]
             ]

    window = sg.Window('Sopa de letras', layout).Finalize()

    graph = window.FindElement('graph')



    posicion = [] #LISTA CON LAS LETRAS Y SUS POSICIONES EN LA SOPA DE LETRAS

    repetidasAncho = {}

    repetidasAlto = {}

    ##################################################
    #####   ACOMODA LA POSICION DE LAS PALABRAS  #####
    ##################################################

    if (horizontal):
        for i in Palabras:
            ancho = random.choice(range(tamañoDeSopa-len(i)))
            alto = random.choice(range(tamañoDeSopa))
            ok = False
            while (ok == False):
                if (alto in repetidasAlto.keys()):
                    cantidad = len(repetidasAlto[alto])
                    for j in range(1,cantidad,2):
                        espacioDerecha = tamañoDeSopa-(repetidasAlto[alto][j]+repetidasAlto[alto][j-1])
                        if (repetidasAlto[alto][j] > len(i)):
                            ok = True
                            rangoNuevo = repetidasAlto[alto][j]-1
                        else:
                            ok = False
                        if (espacioDerecha > len(i)):
                            ok = True
                            rangoNuevo = espacioDerecha-1
                        else:
                            ok = False
                    if (ok):
                        ancho = random.choice(range(tamañoDeSopa)-len(i))
                        repetidasAlto[alto].append(len(i))
                        repetidasAlto[alto].append(ancho)
                    else:
                        alto = random.choice(range(tamañoDeSopa))
                else:
                    repetidasAlto[alto] = [len(i),ancho]
                    ok = True
            else:
                repetidasAncho[ancho] = [len(i),alto]
            posicion.append([i,ancho,alto])
    print(posicion)


    ##################################################
    #####         CREA LA SOPA DE LETRAS         #####
    ##################################################

    letras = {} #CREO UN DICCIONARIO QUE TIENE COMO CLAVES LAS COORDENADAS CONCATENADAS COMO STRING Y EL VALOR ES LA LETRA

    x = 0
    y = 0
    for x in diccionarioCoordenadas.values():
        print(x)
    for i in coordenadas:
        letter = random.choice(string.ascii_uppercase)
        graph.DrawRectangle((i[0],i[1]), (i[2],i[3]), fill_color='white', line_color='black') #DIBUJA EL RECTANGULO EN LA POSICION ADECUADA
        #if (horizontal):
            #if (i[1] )
        graph.DrawText('{}'.format(letter),(i[2]+25,i[3]+25)) #ESCRIBE LA LETRA EN LA POSICION
        letras[str(i[0])+str(i[1])+str(i[2])+str(i[3])] = letter

    letrasPresionadas = set() #CONJUNTO CON LAS COORDENDAS DE LAS LETRAS PRESIONADAS CONCATENADAS COMO STRING
    interacciones = 0
    while True:
        button, values = window.Read()
        if button is None or button == 'Salir':
            break
        if (button == 'sus'):
            ColorSelect = Csus
        if (button == 'ver'):
            ColorSelect = Cver
        if (button == 'adj'):
            ColorSelect = Cadj
        if (button == 'graph'):
            try:
                interacciones = interacciones+1
                if (interacciones%2 != 0):
                    coor = list(filter(lambda x : (values['graph'][0] <= x[0]) and (values['graph'][0] >= x[2]) and (values['graph'][1] <= x[1]) and (values['graph'][1] >= x[3]),coordenadas))
                    x1 = coor[0][0]
                    y1 = coor[0][1]
                    x2 = coor[0][2]
                    y2 = coor[0][3]
                    if (str(x1)+str(y1)+str(x2)+str(y2) in letrasPresionadas):
                        graph.DrawRectangle((x1,y1), (x2,y2), fill_color='white', line_color='black')
                        letrasPresionadas.remove(str(x1)+str(y1)+str(x2)+str(y2))
                    else:
                        try:
                            graph.DrawRectangle((x1,y1), (x2,y2), fill_color=ColorSelect, line_color='black')
                            letrasPresionadas.add(str(x1)+str(y1)+str(x2)+str(y2))
                        except NameError:
                            sg.Popup('Elegi un color antes de empezar a jugar')
                    graph.DrawText('{}'.format(letras[str(x1)+str(y1)+str(x2)+str(y2)]),(x2+25,y2+25))
            except IndexError:
                pass

SopaDeLetras()
