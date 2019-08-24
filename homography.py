from PIL import Image
from pylab import *
import math
import numpy as np


def prox(A):
	if 2*A < 2*int(A) + 1:
		return int(A)
	return int(A+1)


#Bordas de onde a imagem deve entrar
Q1 = array([315,285, 1])
Q2 = array([318, 517, 1])
Q3 = array([568,496, 1])
Q4 = array([568,333, 1])
##########################

figure = array(Image.open("imagem.jpeg"))
destination = array(Image.open("background.jpg"))

y,x = destination.shape[:2]
m,n = figure.shape[:2] 

P1 = array([0,0,1])
P2 = array([0,m,1])
P3 = array([n,m,1])
P4 = array([n,0,1])

P = array([P1,P2,P3,P4])
Q = array([Q1,Q2,Q3,Q4])



matriz_final = list()
aux = list()

for i in range(0,12):
	aux = list()
	for k in range(0,12):
		aux.append(0)
	matriz_final.append(aux)

matriz_final[ 0 ][ 0 ] = P[ 0 ][ 0 ]
for k in range (0, 12): #cada linha da matriz final
	for i in range (0,3): #cada coluna da matriz P
		matriz_final[ k ][ (k%3)*3 + i] = P[ int(math.floor(k/3)) ][ i ]

	if k > 2:
		matriz_final[k][ 8 + int(math.floor(k/3)) ] = - Q[ int(math.floor(k/3)) ][ (k)%3]

# for i in range(0,12):
# 	print(matriz_final[i])

A = np.asarray(matriz_final)
b = np.array([Q1[0],Q1[1],1,0,0,0,0,0,0,0,0,0])
R = np.linalg.solve(A,b)
aux = []
for i in range(3):
	aux.append([R[3*i],R[3*i+1],R[3*i+2]])

H = np.asarray(aux)
print(H)
H_1 = np.linalg.inv(H)

for i in range(x):
    for j in range(y):
        aux = array([i, j, 1])
        aux = aux.transpose()
        ponto = dot(H_1,aux)
        ponto = ponto.transpose()
        a = prox(ponto[0]/ponto[2])
        b = prox(ponto[1]/ponto[2])
        if a in range(n) and b in range(m):
            destination[j][i] = figure[b][a]

plot(x,y,"r*")
imshow(destination)
show()
