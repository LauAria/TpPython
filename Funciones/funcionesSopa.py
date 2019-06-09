
###################################################################################################
#####   DEVUELVE UNA LISTA CON LA LONGITUD DE LA PALABRA MAS LARGA Y LA CANTIDAD DE PALABRAS  #####
###################################################################################################

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

###################################################################################################

###################################################################################################################################################################################
#####                                                 ACOMODA LA POSICION DE LAS PALABRAS HORIZONTALES                                                                        #####
###################################################################################################################################################################################

def AcomodarPalabrasHorizontales(posicion,repetidas,Palabras,tamañoDeSopa):
    import random
    for i in Palabras:
        ancho = random.choice(range(tamañoDeSopa-len(i))) #UN NUMERO RANDOM PARA LA POSICION EN LA FILA, TENIENDO EN CUENTA EL LARGO DE LA PALABRA
        alto = random.choice(range(tamañoDeSopa)) #UN NUMERO RANDOM PARA LA POSICION DE Y EN LA SOPA DE LETRAS, TIENE EN CUENTA LO GRANDE DE LA PALABRA
        if (alto in repetidas.keys()): #SE FIJA SI YA HAY UNA PALABRA EN LA MISMA FILA
            aux = alto #SE GUARDA VALOR DE Y REPETIDO
            if (len(repetidas[alto]) > 2): #SI YA HAY 2 PALABRAS EN LA MISMA FILA, BUSCA OTRA
                while (alto in repetidas.keys()):
                    alto = random.choice(range(tamañoDeSopa))
            else:
                espacioDerecha = tamañoDeSopa-(repetidas[alto][0]+repetidas[alto][1]) #ESPACIO A LA DERECHA DE LA PLABRA QUE ESTA EN LA MISMA FILA
                espacioIzquierda = repetidas[alto][1] #ESPACIO A LA IZQUIERDA DE LA PALABRA QUE ESTA EN LA MISMA FILA
                if (len(i) < espacioIzquierda): #SI HAY ESPACIO A LA IZQUIERDA PARA QUE ENTRE LA PALABRA
                    if (espacioIzquierda-len(i)-1 > 0):
                        ancho = random.choice(range(0,espacioIzquierda-len(i)-1)) #EL NUEVO VALOR EN LA MISMA FILA, A LA IZQUIERDA
                    else:
                        ancho = 0
                elif (len(i) < espacioDerecha) and (tamañoDeSopa-len(i) > repetidas[alto][1]+repetidas[alto][0]+1): #SI HAY ESPACIO A LA DERECHA PARA QUE ENTRE LA PALABRA
                    ancho = random.choice(range(repetidas[alto][1]+repetidas[alto][0]+1,tamañoDeSopa-len(i))) #EL NUEVO VALOR EN LA MISMA FILA, A LA DERECHA
                else:
                    while (alto in repetidas.keys()): #SI NO HAY LUGAR EN NINGUN LADO, BUSCA UN NUEVO VALOR DE Y
                        alto = random.choice(range(tamañoDeSopa))
                if (aux == alto): #SI SE INSERTA EN LA MISMA FILA, SE AGREGA AL DICCIONARIO QUE HAY OTRA EN LA MISMA FILA
                    repetidas[alto].append(len(i))
                    repetidas[alto].append(ancho)
                else:
                    repetidas[alto] = [len(i),alto]
        else:
            repetidas[alto] = [len(i),ancho] #AGREGA AL DICCIONARIO EN QUE LUGAR SE GUARDO LA PALABRA
        posicion.append([i,alto,ancho]) #AGERGA A LA LISTA LA PALABRA, Y LA POSICION

###################################################################################################################################################################################

###################################################################################################################################################################################
#####                                                 ACOMODA LA POSICION DE LAS PALABRAS VERTICALES                                                                          #####
###################################################################################################################################################################################

def AcomodarPalabrasVerticales(posicion,repetidas,Palabras,tamañoDeSopa):
    import random
    for i in Palabras:
        alto = random.choice(range(tamañoDeSopa-len(i))) #UN NUMERO RANDOM PARA LA POSICION EN LA FILA, TENIENDO EN CUENTA EL LARGO DE LA PALABRA
        ancho = random.choice(range(tamañoDeSopa)) #UN NUMERO RANDOM PARA LA POSICION DE Y EN LA SOPA DE LETRAS, TIENE EN CUENTA LO GRANDE DE LA PALABRA
        if (ancho in repetidas.keys()): #SE FIJA SI YA HAY UNA PALABRA EN LA MISMA FILA
            aux = ancho #SE GUARDA VALOR DE Y REPETIDO
            if (len(repetidas[ancho]) > 2): #SI YA HAY 2 PALABRAS EN LA MISMA FILA, BUSCA OTRA
                while (ancho in repetidas.keys()):
                    ancho = random.choice(range(tamañoDeSopa))
            else:
                espacioAbajo = tamañoDeSopa-(repetidas[ancho][0]+repetidas[ancho][1]) #ESPACIO A LA DERECHA DE LA PLABRA QUE ESTA EN LA MISMA FILA
                espacioArriba = repetidas[ancho][1] #ESPACIO A LA IZQUIERDA DE LA PALABRA QUE ESTA EN LA MISMA FILA
                if (len(i) < espacioArriba): #SI HAY ESPACIO A LA IZQUIERDA PARA QUE ENTRE LA PALABRA
                    if (espacioArriba-len(i)-1 > 0): #SI HAY MAS DE UN ESPACIO DE DONDE SE PUEDE ELEGIR RANDOM
                        alto = random.choice(range(0,espacioArriba-len(i)-1)) #EL NUEVO VALOR EN LA MISMA FILA, A LA IZQUIERDA
                    else:
                        alto = 0
                elif (len(i) < espacioAbajo) and (tamañoDeSopa-len(i) > repetidas[ancho][1]+repetidas[ancho][0]+1): #SI HAY ESPACIO A LA DERECHA PARA QUE ENTRE LA PALABRA
                    alto = random.choice(range(repetidas[ancho][1]+repetidas[ancho][0]+1,tamañoDeSopa-len(i))) #EL NUEVO VALOR EN LA MISMA FILA, A LA DERECHA
                else:
                    while (ancho in repetidas.keys()): #SI NO HAY LUGAR EN NINGUN LADO, BUSCA UN NUEVO VALOR DE Y
                        ancho = random.choice(range(tamañoDeSopa))
                if (aux == ancho): #SI SE INSERTA EN LA MISMA FILA, SE AGREGA AL DICCIONARIO QUE HAY OTRA EN LA MISMA FILA
                    repetidas[ancho].append(len(i))
                    repetidas[ancho].append(alto)
                else:
                    repetidas[ancho] = [len(i),alto]
        else:
            repetidas[ancho] = [len(i),alto] #AGREGA AL DICCIONARIO EN QUE LUGAR SE GUARDO LA PALABRA
        posicion.append([i,alto,ancho]) #AGERGA A LA LISTA LA PALABRA, Y LA POSICION
                                                                                                                                                                             
###################################################################################################################################################################################
