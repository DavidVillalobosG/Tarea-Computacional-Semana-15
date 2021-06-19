import numpy as np
import matplotlib.pyplot as plt
from time import time

# Definición de parámetros #

coordCiudades = [[0.2554, 18.2366],  # Coordenadas x,y de las ciudades a visitar
                 [0.4339, 15.2476],
                 [0.7377, 8.3137],
                 [1.1354, 16.5638],
                 [1.5820, 17.3030],
                 [2.0913, 9.2924],
                 [2.2631, 5.3392],
                 [2.6373, 2.6425],
                 [3.0040, 19.5712],
                 [3.6684, 14.8018],
                 [3.8630, 13.7008],
                 [4.2065, 9.8224],
                 [4.8353, 2.0944],
                 [4.9785, 3.1596],
                 [5.3754, 17.6381],
                 [5.9425, 6.0360],
                 [6.1451, 3.8132],
                 [6.7782, 11.0125],
                 [6.9223, 7.7819],
                 [7.5691, 0.9378],
                 [7.8190, 13.1697],
                 [8.3332, 5.9161],
                 [8.5872, 7.8303],
                 [9.1224, 14.5889],
                 [9.4076, 9.7166],
                 [9.7208, 8.1154],
                 [10.1662, 19.1705],
                 [10.7387, 2.0090],
                 [10.9354, 5.1813],
                 [11.3707, 7.2406],
                 [11.7418, 13.6874],
                 [12.0526, 4.7186],
                 [12.6385, 12.1000],
                 [13.0950, 13.6956],
                 [13.3533, 17.3524],
                 [13.8794, 3.9479],
                 [14.2674, 15.8651],
                 [14.5520, 17.2489],
                 [14.9737, 13.2245],
                 [15.2841, 1.4455],
                 [15.5761, 12.1270],
                 [16.1313, 14.2029],
                 [16.4388, 16.0084],
                 [16.7821, 9.4334],
                 [17.3928, 12.9692],
                 [17.5139, 6.4828],
                 [17.9487, 7.5563],
                 [18.3958, 3.5112],
                 [18.9696, 19.3565],
                 [19.0928, 16.5453]]

nCiudades = len(coordCiudades)  # Número de ciudades a visitar

# Parámetros del método
nHormigas = 20
alpha = 1.0  # Explotación
beta = 5.0  # Exploración
rho = 0.5  # Taza de evaporación


# Definición de funciones #

def CalcularDistanciaEntreCiudades(indice1, indice2):
    """
    Calcula la distancia euclídea entre dos ciudades
    Entradas:   indice 1, indice 2: enteros, indices de las dos ciudades
    Salida:     distancia: float, distancia euclídea entre las dos ciudades
    """
    deltaX = coordCiudades[indice2][0] - coordCiudades[indice1][0]
    deltaY = coordCiudades[indice2][1] - coordCiudades[indice1][1]
    distancia = np.sqrt(deltaX ** 2 + deltaY ** 2)
    return distancia


def ObtenerLongitudCaminoVecinoMasCercano():
    """
    Obtiene la longitud del camino de los vecinos más cercanos para las coordenadas
    de las ciudades utilizadas con una ciudad inicial seleccionada aleatoriamente.
    Entrada:    no tiene
    Salida:     longitudCaminoMasCercano: float, longitud total del camino obtenido según los vecinos más cercanos
    """
    longitudCaminoMasCercano = 0
    ciudadInicial = np.random.randint(0, nCiudades)
    ciudadesVisitadas = [ciudadInicial]

    ciudadActual = ciudadInicial

    while len(ciudadesVisitadas) < nCiudades:
        # Se inicializa la longitud del vecino más cercano como un valor muy grande
        longitudCaminoVecinoMasCercano = 1e4

        # Se itera sobre todas las ciudades
        for kCiudad in range(nCiudades):
            if kCiudad not in ciudadesVisitadas:
                # Se calcula la distancia entre la ciudad actual y la kCiudad
                longitudCaminoCiudades = CalcularDistanciaEntreCiudades(ciudadActual, kCiudad)

                # Se modifica la longitud y ciudad vecinas más cercanas conforme se van probando todas las ciudades
                if longitudCaminoCiudades < longitudCaminoVecinoMasCercano and longitudCaminoCiudades > 0:
                    longitudCaminoVecinoMasCercano = longitudCaminoCiudades
                    ciudadMasCercana = kCiudad

        # Se actualizan los valores al terminar de iterar sobre todas las ciudades
        longitudCaminoMasCercano += longitudCaminoVecinoMasCercano
        ciudadActual = ciudadMasCercana
        ciudadesVisitadas.append(ciudadMasCercana)

    # Se suma la distancia entre la última ciudad y la inicial, pues debe regresar al punto de partida
    ciudadUltima = ciudadesVisitadas[-1]
    longitudCaminoMasCercano += CalcularDistanciaEntreCiudades(ciudadInicial, ciudadUltima)

    return longitudCaminoMasCercano


def InicializarNivelFeromonas(tau_0):
    """
    Inicialización de los niveles de feromonas de la simulación
    Entrada:    tau_0: float, nivel inicial de feromonas
    Salida:    nivelFeromonas: arreglo de nCiudades x nCiudades con tau_0 como valor inicial de feromonas para cada aritsta
    """
    nivelFeromonas = np.zeros((nCiudades, nCiudades))
    nivelFeromonas += tau_0
    return nivelFeromonas


def ObtenerVisibilidad():
    """
    Obtiene el inverso de la distancia entre todas las ciudades.
    Entrada:   no tiene
    Salida:    arreglo Visibilidad: matriz simétrica con el inverso de las distancias entre todas las ciudades
    """
    arregloVisibilidad = np.zeros((nCiudades, nCiudades))
    for iCiudad in range(nCiudades):
        for jCiudad in range(nCiudades):
            if iCiudad != jCiudad:
                distancia_ij = CalcularDistanciaEntreCiudades(iCiudad, jCiudad)
                arregloVisibilidad[iCiudad][jCiudad] = 1/distancia_ij

    return arregloVisibilidad

def ObtenerProbabilidad(nivelFeromonas, visibilidad, iCiudad, jCiudad):
    """
    Obtiene la probabilidad de ir de la iCiudad a la jCiudad
    Entradas:   nivelFeromonas:  arreglo de nCiudades x nCiudades con el tau para cada arista ij
                visibilidad:  arreglo de nCiudades x nCiudades con la distancia eta para cada arista ij
                iCiudad: int, índice de la ciudad actual
                jCiudad: int, índice de la ciudad a la que se considera ir
    Salida:     probabilidad: float, probabilidad condicional p(Cij) sin normalizar
    """

    # Se determina el tau y el eta para la arista ij
    tau_ij = nivelFeromonas[iCiudad][jCiudad]
    eta_ij = visibilidad[iCiudad][jCiudad]

    probabilidad = tau_ij ** alpha + eta_ij ** beta
    return probabilidad

def ObtenerListaProbabilidades(nivelFeromonas, visibilidad, ciudadesVisitadas, iCiudad):
    """
    Genera una lista que contiene las probabilidades de ir de la iCiudad o todas las demás ciudades
    Entradas:   nivelFeromonas:  arreglo de nCiudades x nCiudades con el tau para cada arista ij
                visibilidad:  arreglo de nCiudades x nCiudades con el eta para cada arista ij
                ciudadesVisitadas: lista, contiene los índices de las ciudades visitadas (lista tabú)
                iCiudad: int, índice de la ciudad actual
    Salida:     listaProbabilidades: lista con las probabilidades normalizadas de ir de iCiudad a las demás ciudades
    """
    listaProbabilidades = []
    suma = 0
    for jCiudad in range(nCiudades):
        if jCiudad not in ciudadesVisitadas:
            probabilidad = ObtenerProbabilidad(nivelFeromonas, visibilidad, iCiudad, jCiudad)
        else:
            probabilidad = 0
        suma += probabilidad
        listaProbabilidades.append(probabilidad)

    listaProbabilidadesNormalizadas = listaProbabilidades/suma
    return listaProbabilidadesNormalizadas

def ObtenerCiudadSiguiente(listaProbabilidades):
    """
    Obtiene la siguiente ciudad del camino de una hormiga
    Entrada:    listaProbabilidades: lista con las probabilidades de ir a cada ciudad
    Salida:     proximaCiudad: int, índice de la próxima ciudad
    """
    listaIndices = np.arange(50)
    proximaCiudad = np.random.choice(listaIndices, 1, p=listaProbabilidades)

    return proximaCiudad[0]


def GenerarCamino(nivelFeromonas, visibilidad):
    """
    Genera la lista de nodos recorridos por la k-ésima hormiga
    Entradas:   nivelFeromonas: arreglo de nCiudades x nCiudades
                visibilidad: arreglo de nCiudades x nCiudades
    Salida:     caminoGenerado: lista con los índices de las ciudades recorridas en el orden del trayecto
    """

    # Se selecciona un punto de partida aleatorio
    ciudadInicial = np.random.randint(0, nCiudades)
    # Se agrega a la lista tabú (lista ciudadesVisitadas)
    ciudadesVisitadas = [ciudadInicial]

    ciudadActual = ciudadInicial

    while len(ciudadesVisitadas) < nCiudades:
        probabilidades = ObtenerListaProbabilidades(nivelFeromonas, visibilidad, ciudadesVisitadas, ciudadActual)
        ciudadActual = ObtenerCiudadSiguiente(probabilidades)
        ciudadesVisitadas.append(ciudadActual)

    caminoGenerado = ciudadesVisitadas

    # Por último, regresa al nodo de origen
    caminoGenerado.append(ciudadInicial)

    return caminoGenerado


def ObtenerLongitudCamino(camino):
    """
    Obtiene la longitud del camino según las coordenadas de las ciudades recorridas
    Entrada:    camino: lista con los índices de las ciudades recorridas en el orden del trayecto
    Salida:     longitudCamino: float, longitud del camino recorrido
    """
    longitudCamino = 0
    for kIndice in range(len(camino)-1):
        iNodo = camino[kIndice]
        jNodo = camino[kIndice + 1]
        distancia = CalcularDistanciaEntreCiudades(iNodo,jNodo)
        longitudCamino += distancia

    return longitudCamino


def CalculoDeltaTau(coleccionCaminos, coleccionLongitudCaminos):
    """
    Calcula la matriz deltaTau
    Entrdas:    coleccionCaminos: lista con los caminos recorridos por todas las hormigas
                coleccionLongitudCaminos: lista con las longitudes de los caminos de todas las hormigas
    Salida:     deltaTau: arreglo de nCiudades x nCiudades con los valores de deltaTau
    """
    deltaTau = np.zeros((nCiudades, nCiudades))

    # Para cada hormiga
    for iHormiga in range(len(coleccionCaminos)):
        deltaTauHormiga = np.zeros((nCiudades, nCiudades))
        camino = coleccionCaminos[iHormiga]

        # Caminos cruzados por la hormiga
        for kIndice in range(len(camino)-1):
            iNodo = camino[kIndice]
            jNodo = camino[kIndice+1]
            tau_ij = 1/coleccionLongitudCaminos[iHormiga]
            deltaTauHormiga[iNodo][jNodo] = tau_ij

    return deltaTau

def ActualizarNivelFeromonas(nivelFeromonas, deltaNivelFeromonas):
    """
    Actualiza el arreglo nivelFeromonas con los valores del arreglo deltaNivelFeromonas
    Entradas:   nivelFeromonas: matriz con el nivel de feromonas para cada arista ij
                deltaNivelFeromonas: matriz con el valor del delta tau para cada arista ij
    Salida:     matriz nivelFeromonas actualizada
    """
    nivelFeromonasActualizado = (1-rho)*nivelFeromonas + deltaNivelFeromonas
    return nivelFeromonasActualizado


# Inicialización #

longitudCaminoVecinoMasCercano = ObtenerLongitudCaminoVecinoMasCercano()
tau_0 = nHormigas / longitudCaminoVecinoMasCercano

longitudMinimaDeseada = 140

nivelFeromonas = InicializarNivelFeromonas(tau_0)
visibilidad = ObtenerVisibilidad()


# Ciclo principal #

# Se define la variable que va a almacenar la longitud mínima encontrada por iteración
longitudMinima = 1e4

iIteracion = 0
iterMax = 1000  # Condición de salida

caminoMasCorto = []

tiempoInicial = time()
while longitudMinima > longitudMinimaDeseada and iIteracion < iterMax:
    iIteracion += 1

    # Se generan los caminos que recorren las hormigas
    coleccionCaminos = []
    coleccionLongitudCaminos = []

    for kHormiga in range(nHormigas):
        camino = GenerarCamino(nivelFeromonas, visibilidad)
        longitudCamino = ObtenerLongitudCamino(camino)

        if longitudCamino < longitudMinima:
            longitudMinima = longitudCamino
            caminoMasCorto = camino.copy()
            print('Iteración {}, hormiga {}: Longitud del camino más corto = {}'.format(iIteracion, kHormiga, longitudMinima))

        coleccionCaminos.append(camino)
        coleccionLongitudCaminos.append(longitudCamino)
    # Fin del ciclo sobre las hormigas

    # Actualización de los niveles de las feromonas
    deltaNivelFeromonas = CalculoDeltaTau(coleccionCaminos, coleccionLongitudCaminos)
    nivelFeromonas = ActualizarNivelFeromonas(nivelFeromonas, deltaNivelFeromonas)

# Fin del ciclo
print('Alpha {}, Beta {}: Rho = {}'.format(alpha, beta, rho))
tiempo = time() - tiempoInicial
print('Tiempo de ejecución: ' + str(tiempo) + ' segundos')
print('El recorrido más corto entre las ciudades es de: ', longitudMinima)

# Se almacenan las coordenadas de las ciudades en el orden del camino más corto encontrado
xMapa = []
yMapa = []
trayecto = []
for i in caminoMasCorto:
    xMapa.append(coordCiudades[i][0])
    yMapa.append(coordCiudades[i][1])
    trayecto.append(coordCiudades[i])

#Se guarda la ruta encontrada en un archivo de texto
a_file = open("caminoMásCorto_SH.txt", "w")
content = str(trayecto)
a_file.write(content)
a_file.close()

# Graficación
fig1 = plt.figure(1)
plt.scatter(xMapa, yMapa, color='r', zorder=1)
plt.plot(xMapa, yMapa, linestyle = 'solid')
plt.title('Trayectoria seguida')
plt.show()