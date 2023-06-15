import os
import cv2

ejemplo_dir = 'D:/Javier/Universidad/7/Mineria De Datos/GNA DBScan'
f = open("rgbExtracted.txt","w")#creacion de archivo
with os.scandir(ejemplo_dir) as ficheros:
    for fichero in ficheros:
        if fichero.name.endswith('.jpg'):
            image = cv2.imread(fichero.name)
            print(fichero.name)
            for i in range(0,image.shape[0]):
                for j in range(0,image.shape[1]):
                    b, g, r = image[i,j]
                    f.write(str(r)+","+str(g)+","+str(b)+'\n')
f.close()