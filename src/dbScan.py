import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import radius_neighbors_graph
from matplotlib import pyplot as plt
import time
import pandas as pd
from statistics import pstdev

def vecinosCercanos(x):
    neighbors = NearestNeighbors(n_neighbors=6)
    neighbors_fit = neighbors.fit(x)
    distances, indices = neighbors_fit.kneighbors(x)
    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    plt.plot(distances)
    plt.grid()
    plt.show()

def dbScan(x,epsilon,points):
    inicio = time.time()
    db = DBSCAN(eps=epsilon, min_samples=points).fit(x)
    fin = time.time()
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    print("Epsilon:"+str(epsilon)+", MinPoints: " +str(points))
    print("Numero de clusters: %d" % n_clusters_)
    print("Numero de ruido: %d" % n_noise_)
    inicio2 = time.time()
    labels = list(labels)
    clusters = []
    if n_clusters_==0:
        return 0, 0, 0
    else:
        for i in range(0,n_clusters_):
            cluster = labels.count(i)
            clusters.append(cluster)
    devsta = pstdev(clusters)
    print("Desviacion estandar del cluster: %f" %devsta)
    porcentaje = 1-(n_noise_/675000)
    ins_clas = 675000-n_noise_
    fit = (((ins_clas/n_clusters_)*porcentaje)+ins_clas)-(devsta*2)#Funcion matematica
    print("Metrica mas chida: %f"%fit)
    fin2 = time.time()
    print("Tiempo del fit: %s s" % str(fin-inicio))
    print("Tiempo de la metrica: %s s" % str(fin2-inicio2))
    return n_clusters_, n_noise_, devsta

def grafico3D(x):
    print(x)
    figura = plt.figure()
    grafica = figura.add_subplot(111,projection='3d')
    [xi, yi, zi] = np.transpose(x)
    grafica.scatter(xi,yi,zi,c="blue",marker='o',label="x[i]")
    grafica.set_title('Dataset')
    grafica.set_xlabel('R')
    grafica.set_ylabel('G')
    grafica.set_zlabel('B')
    grafica.legend()
    plt.show()

"""with open("rgbExtracted.txt") as f:
    x = np.genfromtxt('rgbExtracted.txt',delimiter=',',dtype=None)
#grafico3D(x)
#vecinosCercanos(x)
dbScan(x,5,60)"""
