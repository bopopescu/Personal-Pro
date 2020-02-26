from bokeh.plotting import figure, show

from borracho import BorrachoTradicional
from campo import Campo
from coordenadas import Coordenada

def caminata(campo, borracho, pasos, graph):
    inicio = campo.obtener_coordenada(borracho)
    ubicaciones_x,ubicaciones_y = [],[]

    for _ in range(pasos):
        ubicar = campo.mover_borracho(borracho)

        if graph:
            ubicaciones_x.append(ubicar.x)
            ubicaciones_y.append(ubicar.y)

    if graph:        
        graficar_pasos(ubicaciones_x, ubicaciones_y) 

    return inicio.distancia(campo.obtener_coordenada(borracho))


def simular_caminata(pasos, numero_de_intentos, tipo_de_borracho):
    borracho = tipo_de_borracho(nombre = 'Juan')
    origen = Coordenada(0,0)
    distancias = []

    for idx in range(numero_de_intentos):

        if idx == 0:
            campo = Campo()
            campo.anadir_borracho(borracho, origen)
            caminata(campo, borracho, pasos, graph = True)

        campo = Campo()
        campo.anadir_borracho(borracho, origen)
        simulacion_caminata = caminata(campo, borracho, pasos, graph = False)
        distancias.append(round(simulacion_caminata, 1))
        
    return distancias

def graficar(x, y):
    grafica = figure(title='Camino aleatorio', x_axis_label ='pasos', y_axis_label = 'distancia')
    grafica.line(x,y,legend_label='distancia media')
    show(grafica)

def graficar_pasos(x, y):
    grafica = figure(title=f'Camino aleatorio con {len(x):,} pasos', x_axis_label ='X', y_axis_label = 'Y')
    grafica.line(x,y,legend_label='Recorrido')
    show(grafica)     


def main(distancias_de_caminata, numero_de_intentos, tipo_de_borracho):
    distancias_media_por_caminata = []

    for pasos in distancias_de_caminata:
        distancias = simular_caminata(pasos, numero_de_intentos, tipo_de_borracho)
        distancia_media = round(sum(distancias)/len(distancias),4)
        distancia_maxima = max(distancias)
        distancia_minima = min(distancias)

        distancias_media_por_caminata.append(distancia_media)

        print(f'\n{tipo_de_borracho.__name__} caminata aleatoria de {pasos} pasos.')
        print(f'Media = {distancia_media}')
        print(f'Max = {distancia_maxima}')
        print(f'Min = {distancia_minima}')
    graficar(distancias_de_caminata, distancias_media_por_caminata)



if __name__ == '__main__':

    distancias_de_caminata = [10,100,1000,10000,100000]
    numero_de_intentos = 100

    main(distancias_de_caminata, numero_de_intentos, BorrachoTradicional)
