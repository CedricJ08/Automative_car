# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 19:04:31 2018

@author: Alu
"""

import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt





def get_circuit():
    img=mpimg.imread('trajet.png')[100:600,200:1000,1]
    for i in range (len(img)):
        for j in range (len(img[0])):
            if img[i][j]!=1:
                img[i][j]=0
    return (img)




def draw( steps,circuit ):
    image_with_points=np.copy(circuit)
    for point in steps :
        J_im = point[0]
        I_im = len(circuit)-point[1]
        for u in range (I_im-5,I_im+5):
            for v in range (J_im-5,J_im+5):
                image_with_points[u][v] = 0
    plt.imshow(image_with_points)



def get_path(depart,arrival,circuit):
    pos = depart
    steps=[pos]
    cir = np.copy(circuit)
    len_cir=len(cir)
    j=0
    while np.sqrt((pos[0]-arrival[0])**2+(pos[1]-arrival[1])**2) > 30 :
        x_j=steps[j][0]
        y_j=steps[j][1]
        Lr=[]
        Lpos=[(x_j,y_j)]
        Ltheta=[]
        pos_visited=[]
        
        for i in range (1000):
            theta = 2*np.pi*(i/1000)
            for r in range(2,2000):
                x=x_j+int(r*np.cos(theta))
                y=y_j+int(r*np.sin(theta))
                pos_visited.append((x,y))             
                if cir[len_cir-y][x] == 0:
                    break
                Lr.append(r)
                Lpos.append((x,y))
                Ltheta.append(theta)
        for visited_point in pos_visited:
            cir[len_cir-visited_point[1]][visited_point[0]] = 0     
                
        indice = np.argmax(Lr)
        theta=Ltheta[indice]
        pos=Lpos[indice]
        steps.append(pos)
        j+=1
    return(steps)



circuit = get_circuit()
path = get_path((103,262),(686,244),circuit)
pos=(400,320)
    
def distance(position,chemin):
    k=0
    K=[]
    L_dist=[]
    for i in range (len(path)-1):
        x_i_1=chemin[i][0]
        x_i_2=chemin[i+1][0]
        y_i_1=chemin[i][1]
        y_i_2=chemin[i+1][1]
        for j in range (1,101):
            alpha = j/100
            x_j= alpha*(x_i_2-x_i_1)+x_i_1
            y_j= alpha*(y_i_2-y_i_1)+y_i_1
            L_dist.append(np.sqrt((position[0]-x_j)**2+(position[1]-y_j)**2))
            K.append(k)
            k+=1
    return(K[np.argmin(L_dist)]/len(K))

