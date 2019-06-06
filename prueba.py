"""
engine para setear donde buscar
1° setear lenguaje
2° aplicar un search (argumento lo que quiero buscar), devuelve un articulo
le puede pedir algo al articulo (article.sections por ejemplo devuelve una lista de objetos)
en el titulo de la seccion tenemos informacion de si es adjetivo, sustantivo, o verbo

articulo --> seccion ---> titulo

dir(objeto) devuelve una lista de lo que podes pedir

"""
from pattern.web import Wikia

print(dir(Wikia))

article = Wikia().search(query = 'cat')

print(article)

#article = Wikia().search('cat')

#seccion = article.sections

#print(type(seccion))

#print(seccion)

#print(dir(seccion))