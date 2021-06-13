import numpy as np
import matplotlib.pyplot as plt
import statistics as sts

mapa = [[0.2554, 18.2366],
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

CantidadCiudades = 50 #Número de ciudades a visitar
TamañoPoblacion = 30 #Número de cromosomas en una generación
Generaciones = 10000 #Número de generaciones a ejecutar



def CrearCromosoma(CantidadCiudades):
    '''
    Crea una lista que contiene los índices sin repetir que representa el orden de las ciudades a visitar.
    '''
    listaTabu = []
    cromosoma = []
    for i in range (0,CantidadCiudades):
        control = True
        while control == True:
            ciudad = np.random.randint(0,CantidadCiudades)
            if ciudad not in listaTabu:
                cromosoma.append(ciudad)
                control = False
        listaTabu.append(ciudad)
    return cromosoma

def VecinoMasCercano(CantidadCiudades,mapa):
    '''
    Version alternativa a la función CrearCromosoma. En lugar de ser totalmente aleatorio el cromosoma se crea considerando
    la distancia entre las ciudades vecinas.
    '''
    CiudadInicial = np.random.randint(0,CantidadCiudades)
    CiudadActual = CiudadInicial
    CiudadesVisitadas = [CiudadInicial]

    for i in range (CantidadCiudades-1):
        LongitudVecinoMasCercano = 1e4
        for j in range (CantidadCiudades):
            longitudCamino = ((mapa[j][0]-mapa[CiudadActual][0])**2+(mapa[j][1]-mapa[CiudadActual][1])**2)**(1/2)
            if longitudCamino < LongitudVecinoMasCercano and longitudCamino > 0 and j not in CiudadesVisitadas:
                LongitudVecinoMasCercano = longitudCamino
                CiudadMasCercana = j
        CiudadActual =CiudadMasCercana
        CiudadesVisitadas.append(CiudadMasCercana)
    return CiudadesVisitadas

def CrearPoblacion(CantidadCiudades,TamañoPoblacion):
    '''
    Genera la primera generación de cromosomas.
    '''
    Poblacion = []
    for j in range (0,TamañoPoblacion):
        individuo = CrearCromosoma(CantidadCiudades)
        Poblacion.append(individuo)
    return Poblacion

def InicializaciónModificada(CantidadCiudades,TamañoPoblacion,mapa):
    '''
    Version alternativa de CrearPoblacion(). Esta versión utiliza el camino más cercano entre vecinos y los somete a
    mutaciones aleatorias.
    '''
    Poblacion = []
    #Se crea la poblacion basada en los vecinos más cercanos.
    for j in range(0, TamañoPoblacion):
        individuo = VecinoMasCercano(CantidadCiudades,mapa)
        Poblacion.append(individuo)
    CromosomasPorMutar = np.random.randint(3,11)
    #Se someten a mutacion aleatoria.
    for k in range(CromosomasPorMutar):
        IndividuoPorMutar = np.random.randint(1,len(Poblacion))
        indiceA = np.random.randint(0, CantidadCiudades)
        indiceB = np.random.randint(0, CantidadCiudades)
        Poblacion[IndividuoPorMutar][indiceA], Poblacion[IndividuoPorMutar][indiceB] = Poblacion[IndividuoPorMutar][indiceB],Poblacion[IndividuoPorMutar][indiceA]
    return Poblacion

def EvaluarFuncion (Cromosoma,mapa):
    '''
    Encuentra la distancia que recorre el vendedor ambulante si sigue el ordel del cromosoma dado.
    '''
    longitud = 0
    for k in range (0,len(Cromosoma)-1):
        distancia = ((mapa[Cromosoma[k+1]][0]-mapa[Cromosoma[k]][0])**2+(mapa[Cromosoma[k+1]][1]-mapa[Cromosoma[k]][1])**2)**(1/2)
        longitud = longitud+distancia
    longitud = longitud + ((mapa[0][0]-mapa[-1][0])**2+(mapa[0][1]-mapa[-1][1])**2)**(1/2)
    return 1/longitud

def Mutador(indiceMejorResultado,Poblacion):
    '''
    Crea una nueva poblacion, excluyendo al mejor de la generación actual. El resto de elementos serán expuestos a una
    probabilidad de mutación. El mejor de la generación actual se mantiene intacto y se agrega en un paso posterior.
    '''
    PoblacionNueva = []
    probabilidadMutacion = 0.25
    PoblacionPorMutar = Poblacion.copy()
    PoblacionPorMutar.pop(indiceMejorResultado)
    for cromosoma in range (0,len(PoblacionPorMutar)):
        probabilidadAleatoria = np.random.random()
        if probabilidadAleatoria < probabilidadMutacion:
            indiceA = np.random.randint(0,CantidadCiudades)
            indiceB = np.random.randint(0,CantidadCiudades)
            Poblacion[cromosoma][indiceA],Poblacion[cromosoma][indiceB] = Poblacion[cromosoma][indiceB],Poblacion[cromosoma][indiceA]
            PoblacionNueva.append(PoblacionPorMutar[cromosoma].copy())
        else:
            PoblacionNueva.append(PoblacionPorMutar[cromosoma].copy())
    return PoblacionNueva

#Se crea la primera generación, se puede escoger entre utilizar CrearPoblacion(CantidadCiudades,TamañoPoblacion) para
#una poblacion totalmente aleatoria o puede usarse InicializaciónModificada(CantidadCiudades,TamañoPoblacion,mapa) para
#considerar los vecinos más cercanos.
PoblacionActual = CrearPoblacion(CantidadCiudades,TamañoPoblacion)

#Estas listas almacenarán los resultados obtenidos para luego ser graficados
listaMejoresResultados = []
listaResultadosPromedios = []


#Ciclo principal
for iGen in range (0,Generaciones):
    mejorIndividuo = 0
    resultados = []
    resultadoPromedio = 0

    #Evalua cada cromosoma en la funcion por optimizar
    for jCromosoma in range (0,len(PoblacionActual)):
        CromosomaEvaluar = PoblacionActual[jCromosoma]
        CromosomaResultado = EvaluarFuncion(CromosomaEvaluar,mapa)
        resultados.append(CromosomaResultado)
    mejorResultado = max(resultados)
    resultadoPromedio = sts.mean(resultados)
    mejorIndividuo = PoblacionActual[resultados.index(mejorResultado)]

    #Nueva poblacion y mutaciones
    PoblacionMutada = Mutador(resultados.index(mejorResultado),PoblacionActual.copy())
    PoblacionMutada.append(mejorIndividuo)
    PoblacionActual = PoblacionMutada

    #Se registra el resultado promedio y el mejor resultado de cada generación
    listaMejoresResultados.append(mejorResultado)
    listaResultadosPromedios.append((resultadoPromedio))

#Se crea una lista que contiene las generaciones, su único proposito es para graficar
listaGeneraciones = np.linspace(1,Generaciones,Generaciones)

#Se imprime el resultado de la simulación.
print('El recorrido más corto entre las ciudades es de: ', 1/mejorResultado)

#Se obtiene la ruta de ciudades a seguir a partir de los índices obtenidos en el ciclo principal y se le agrega la ciudad inicial
#para cerrar la trayectoria.
PuntoDePartida = mejorIndividuo[0]
mejorIndividuo.append(PuntoDePartida)
TrayectoriaFinal = mejorIndividuo
CaminoMasCorto = []
for j in range(0,len(TrayectoriaFinal)):
    indice = TrayectoriaFinal[j]
    CaminoMasCorto.append(mapa[indice])
CaminoMasCorto = np.array(CaminoMasCorto)

#Se guarda esta ruta en un archivo de texto
a_file = open("caminoMásCorto_AGE.txt", "w")
content = str(CaminoMasCorto)
a_file.write(content)
a_file.close()

#Se separa la matriz de posición de las ciudades en una lista por coordenada
xMapa = []
for x in range(0,len(TrayectoriaFinal)):
    xMapa.append(CaminoMasCorto[x][0])
yMapa = []
for y in range(0,len(TrayectoriaFinal)):
    yMapa.append(CaminoMasCorto[y][1])

#Se grafican los resultados
fig1 = plt.figure(1)
plt.plot(listaGeneraciones,listaMejoresResultados, label = 'Mejor Resultado')
plt.plot(listaGeneraciones,listaResultadosPromedios, label = 'Resultado promedio')
plt.xlabel('Generaciones')
plt.ylabel('1/(Distancia recorrida)')
plt.legend(loc='upper right')
plt.title('Función de ajuste vs Generación')

fig2 = plt.figure(2)
plt.scatter(xMapa,yMapa,color='r',zorder=1)
plt.plot(xMapa,yMapa,linestyle = 'solid')
plt.title('Trayectoria seguida')
plt.show()











