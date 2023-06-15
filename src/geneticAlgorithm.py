import numpy as np
from math import trunc
import dbScan
#5 bits para el epsilon 2-7
#10 bits para el numero de puntos 6-1500

def generarPoblacion():
    poblacion = []
    for _ in range(0,40):
        individuo =list(np.random.randint(0,2,15))
        poblacion.append(individuo)
    return poblacion

def funcionFitness(x,individuo,i,f):
    epsilon = int("".join(map(str,individuo[0:5])),2)
    minPoints = int("".join(map(str,individuo[5:])),2)
    epsilon+=1
    minPoints+=1
    epsilon=(epsilon*0.15625)+2
    minPoints=trunc((minPoints*1.458984375)+6)
    print(individuo)
    clusters, ruido, devsta = dbScan.dbScan(x,epsilon,minPoints)
    if clusters == ruido == devsta == 0:
        print(0)
        return 0
    else:
        porcentaje = 1-(ruido/675000)
        ins_clas = 675000-ruido
        fit = (((ins_clas/clusters)*porcentaje)+ins_clas)-(devsta*2)#Funcion matematica
        f.write(str(i)+", "+str(epsilon)+", "+str(minPoints)+", "+str(clusters)+", "+str(ruido)+", "+str(devsta)+", "+str(fit)+"\n")
        return fit

def crossover(parent0, parent1):
    points0 = list(range(1,14))
    points = list(np.random.choice(points0,replace=False,size=4))
    points.sort()
    child0, child1 = [], []
    #Se crea el hijo 1
    child0+=parent0[0:points[0]]
    child0+=parent1[points[0]:points[1]]
    child0+=parent0[points[1]:points[2]]
    child0+=parent1[points[2]:points[3]]
    child0+=parent0[points[3]:]
    #Se crea el hijo 2
    child1+=parent1[0:points[0]]
    child1+=parent0[points[0]:points[1]]
    child1+=parent1[points[1]:points[2]]
    child1+=parent0[points[2]:points[3]]
    child1+=parent1[points[3]:]
    return child0, child1

def mutacion(population):
    index0 = np.random.randint(0,20)
    index1 = np.random.randint(20,40)
    #fHijo = np.random.choice(index1,size=1)
    #fPadre = np.random.choice(index0,size=1)
    #Mutacion primer individuo
    bit = np.random.randint(0,15)
    if population[index0][bit]==0:
        population[index0][bit]=1
    else:
        population[index0][bit]=0
    #Mutacion segundo individuo
    bit = np.random.randint(0,15)
    if population[index1][bit]==0:
        population[index1][bit]=1
    else:
        population[index1][bit]=0
    return population

def algoritmoGenetico(x):
    #Generando poblacion inicial
    population = generarPoblacion()
    ite = 0
    fitness = []
    newPopulation = []
    while(ite<30):
        fitness.clear()
        i = 1
        f = open("Registro/Poblacion_"+str(ite+1)+".txt","w")
        for individuo in population:
            print(i)
            fitness.append(funcionFitness(x,individuo,i,f))
            i+=1
        #Seleccionando los individuos de la siguiente generacion
        newPopulation.clear()
        index = list(range(0,40))
        for _ in range(0,20):
            pairs = np.random.choice(index,replace=False,size=2)
            index.remove(pairs[0])
            index.remove(pairs[1])
            if fitness[pairs[0]]>fitness[pairs[1]]:
                newPopulation.append(population[pairs[0]])
            else:
                newPopulation.append(population[pairs[1]])
        index = list(range(0,20))
        #Realizando el cruce de las parejas
        for _ in range(0,10):
            pairs = np.random.choice(index,replace=False,size=2)
            index.remove(pairs[0])
            index.remove(pairs[1])
            child0, child1 = crossover(population[pairs[0]],population[pairs[1]])
            newPopulation.append(child0)
            newPopulation.append(child1)
        newPopulation=mutacion(newPopulation)
        population=newPopulation.copy()
        ite+=1
        f.close()

with open("rgbExtracted.txt") as f:
    x = np.genfromtxt('rgbExtracted.txt',delimiter=',',dtype=None)
algoritmoGenetico(x)