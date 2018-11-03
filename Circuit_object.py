# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 23:36:25 2018

@author: Alu
"""

import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt




class Circuit :
    def __init__(self,dep=(103,262),fin=(686,244),path='trajet.png'):
        self.path = path
        self.dep = dep
        self.fin = fin
        
        
    def get_circuit(self):
        img=mpimg.imread(self.path)[100:600,200:1000,1]
        for i in range (len(img)):
            for j in range (len(img[0])):
                if img[i][j]!=1:
                    img[i][j]=0
        return(img)
    
    def get_path(self,circuit):
        pos = self.dep
        steps=[pos]
        cir = np.copy(circuit)
        len_cir=len(cir)
        j=0
        while np.sqrt((pos[0]-self.fin[0])**2+(pos[1]-self.fin[1])**2) > 30 :
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
        
    def draw_path(self, path ,circuit ):
        image_with_points=np.copy(circuit)
        for point in path :
            J_im = point[0]
            I_im = len(circuit)-point[1]
            for u in range (I_im-5,I_im+5):
                for v in range (J_im-5,J_im+5):
                    image_with_points[u][v] = 0
        plt.imshow(image_with_points)


