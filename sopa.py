
def SopaDeLetras():
    import PySimpleGUI as sg
    import random
    import string

    letras = []
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
            letras.append([lista[0],lista[1],lista[2],lista[3]]) #AGREGA LAS COORDENADAS
            lista[2] = lista[2]+50 #AUMENTA LA COORDENADA top_left
            lista[0] = lista[0]+50 #AUMENTA LA COORDENADA top_right
            aux = x

    layout = [
                [sg.Submit('OK')],
    			[sg.Graph(canvas_size=(sizeSopa, sizeSopa), graph_bottom_left=(0,0), graph_top_right=(sizeSopa, sizeSopa), background_color='white',
                key='graph',drag_submits=True)],
                [sg.Submit('Salir')]
             ]

    window = sg.Window('Coordenadas', layout).Finalize()

    graph = window.FindElement('graph')

    while True:
        button, values = window.Read()
        if button is None or button == 'Salir':
            break
        if (button == 'OK'):
            for x in letras:
                letter = random.choice(string.ascii_uppercase)
                graph.DrawRectangle((x[0],x[1]), (x[2],x[3]), fill_color='white', line_color='black') #DIBUJA EL RECTANGULO EN LA POSICION ADECUADA
                graph.DrawText('{}'.format(letter),(x[2]+25,x[3]+25)) #ESCRIBE LA LETRA EN LA POSICION

SopaDeLetras()
