
def SopaDeLetras():
    import PySimpleGUI as sg
    import random
    import string

    coordenadas = []
    aux = -1
    sizeSopa = 50*10 #EL 10 ES EL RESULTADO DE LO GRANDE QUE VA A SER LA SOPA DE LETRAS
    size = int((50*10)/50) #EL 10 ES EL RESULTADO DE LO GRANDE QUE VA A SER LA SOPA DE LETRAS
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
            lista[2] = lista[2]+50 #AUMENTA LA COORDENADA top_left
            lista[0] = lista[0]+50 #AUMENTA LA COORDENADA top_right
            aux = x

    layout = [
    			[sg.Graph(canvas_size=(sizeSopa, sizeSopa), graph_bottom_left=(0,0), graph_top_right=(sizeSopa, sizeSopa), background_color='white',
                key='graph',enable_events=True,change_submits=False,drag_submits=True)],
                [sg.Submit('Salir')]
             ]

    window = sg.Window('Sopa de letras', layout).Finalize()

    graph = window.FindElement('graph')

    letras = {} #CREO UN DICCIONARIO QUE TIENE COMO CLAVES LAS COORDENADAS CONCATENADAS COMO STRING Y EL VALOR ES LA LETRA
    for x in coordenadas:
        letter = random.choice(string.ascii_uppercase)
        graph.DrawRectangle((x[0],x[1]), (x[2],x[3]), fill_color='white', line_color='black') #DIBUJA EL RECTANGULO EN LA POSICION ADECUADA
        graph.DrawText('{}'.format(letter),(x[2]+25,x[3]+25)) #ESCRIBE LA LETRA EN LA POSICION
        letras[str(x[0])+str(x[1])+str(x[2])+str(x[3])] = letter

    letrasPresionadas = set() #CONJUNTO CON LAS COORDENDAS DE LAS LETRAS PRESIONADAS CONCATENADAS COMO STRING
    interacciones = 0
    while True:
        button, values = window.Read()
        if button is None or button == 'Salir':
            break
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
                        graph.DrawRectangle((x1,y1), (x2,y2), fill_color='green', line_color='black')
                        letrasPresionadas.add(str(x1)+str(y1)+str(x2)+str(y2))
                    graph.DrawText('{}'.format(letras[str(x1)+str(y1)+str(x2)+str(y2)]),(x2+25,y2+25))
            except IndexError:
                pass
SopaDeLetras()
