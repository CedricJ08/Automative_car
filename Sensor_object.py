# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 13:19:22 2018

@author: Alu
"""

import numpy as np

def list_vec_to_check(rangge,orientation,direction , pos_x, pos_y):
    l=[]
    rayon =0.99
    r=0
    while r < rangge :
        r+=rayon
        ex=pos_x + r*np.cos(orientation + direction)
        ey=pos_y + r*np.sin(orientation + direction)
        Ex=float(int(ex))
        Ey=float(int(ey))
        if np.sqrt(((ex-Ex)**2)+((ey-Ey)**2)) < rayon :
            l.append ((Ex,Ey))
    return(l)

class Sensor :         
    def __init__(self,direction):
        self.direction=direction
        self.range = 100
        self.value = 0

    def up_date_value(self,x,y,orientation,circuit):
        L=list_vec_to_check(self.range,orientation*(np.pi/4),self.direction*(np.pi/8) , x, y)
        len_cir=len(circuit)
        len_cir0=len(circuit[0])
        for couple in L:
            X=couple[0]
            Y=couple[1]
            i = min(len_cir-1,max(0,int(len_cir-Y)))
            j = min(len_cir0-1,max(0,int(X)))
            if circuit[i][j]==0:
                self.value = np.sqrt((X-x)**2+(Y-y)**2)
                break
            self.value = self.range
