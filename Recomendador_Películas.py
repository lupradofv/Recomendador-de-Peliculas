import regex as re
import pandas as pd
import sys, signal

def salida(signal,frame):
    print('\n¡Gracias por utilizar el recomendador de películas!')
    sys.exit(0)

def buscar_pelicula(pelicula, peliculas):
    existe = False
    for i in peliculas.keys():
        encontrada = i
        i = re.sub('[0-9]+', '', i)
        i = i.replace("()", '')
        i = i.strip()
        if pelicula == i:
            existe = True
            genre = peliculas.get(encontrada)
            return genre, True
            
    if not existe:
        print('La película no se encuentra en el sistema. Introduzca una nueva búsqueda.')
        return None, False

# generamos una lista con todas las películas del mismo género (buscamos en los valores del dict)
def buscar_similar(genre, peliculas):
    p = 0
    similares = []
    for i in peliculas.values():
        if genre == i:
            similares.append(p)
            p+=1
        else:
            p+=1

    return similares

def generar_lista(peliculas):
    lista_peliculas = []
    for i in peliculas.keys():
        lista_peliculas.append(i)

    return lista_peliculas

if __name__=='__main__':

    signal.signal(signal.SIGINT, salida)
    """ETL.
    Extraer:
    ----------
    Cargar los datos del archivo csv mediante la librería pandas.
    """

    movies_df = pd.read_csv('movies.csv')
    """
    Trasformar:
    ----------
    peliculas : diccionario
        Generar un diccionario con los títulos como claves 
        junto con el género como valor.
    pelicula : string
        Procesar la entrada por pantalla para asegurar:
            - Formato de título
            - Formato idéntico al de los datos cargados
            - Existencia en el csv de películas
    """
    num_pelis=len(movies_df)
    peliculas = dict()
    # Generar un diccionario: pelicula, género
    i = 0
    while i < num_pelis:
        peliculas[movies_df['title'][i]] = movies_df['genres'][i]
        i +=1

    existe = False
    while not existe:
        pelicula = input('Introduce la película:')
        pelicula = pelicula.title()
        pelicula = re.sub('[0-9]+', '', pelicula)
        genre,existe = buscar_pelicula(pelicula, peliculas)
    
    recomendadas = buscar_similar(genre, peliculas)

    lista_peliculas = generar_lista(peliculas)

    print('El género de la película',pelicula,'es',genre)
    rec = lista_peliculas[recomendadas[0]]
    print(rec)
    i = 1
    fin = False
    while not fin:
        f = input('¿Le gustaría solicitar otra recomendación? (S/N)?')
        si = ['s','S']
        if f in si:
            rec = lista_peliculas[recomendadas[i]]
            print(rec)
            i += 1
            if i == len(recomendadas):
                print('No existen más peliculas similares en el sistema.')
                fin = True
        else:
            print('Gracias por utilizar el sistema de recomendación.')
            fin = True