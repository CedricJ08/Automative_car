# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 13:17:04 2018

@author: Alu
"""

import numpy as np
from Sensor_object import Sensor
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.ndimage

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

def triangle():
    im_car1 = np.zeros((5,20))
    for i in range (5):
        for j in range (20):
            if 4*i > j:
                im_car1[i][j]=1
    im_car2 = np.flip(im_car1,axis=0)
    im_car=np.concatenate((im_car1,im_car2),axis=0)
    return(im_car)

def clean(arr):
    for i in range(len(arr)):
        for j in range (len(arr[0])):
            if arr[i][j] < 0.5:
                arr[i][j]=0
            else :
                arr[i][j]=1
    return(arr)
          
              
class Car :
    def __init__(self,pos_ini,o_ini):
        self.x = pos_ini[0]
        self.y = pos_ini[1]
        self.orientation = o_ini
        
        self.sensor_1=Sensor(-2)
        self.sensor_2=Sensor(-1)
        self.sensor_3=Sensor(0)
        self.sensor_4=Sensor(1)
        self.sensor_5=Sensor(2)
    
    
    def move_forward(self, distance,circuit):
#        self.x+=int(distance*np.cos(self.orientation*(np.pi/4)))
#        self.y+=int(distance*np.sin(self.orientation*(np.pi/4)))
        x_target=self.x+int(distance*np.cos(self.orientation*(np.pi/4)))
        y_target=self.y+int(distance*np.sin(self.orientation*(np.pi/4)))
        k=0
        for i in range (1,101):
            k+=1
            alpha = i/100
            x_i= int(alpha*(x_target-self.x)+self.x)
            y_i= int(alpha*(y_target-self.y)+self.y)
            if int(circuit[len(circuit)-y_i][x_i]) == 0 :
                self.x= int(((i-1)/100)*(x_target-self.x)+self.x)
                self.y= int(((i-1)/100)*(y_target-self.y)+self.y)
                break
        if k == 100 :
            self.x=x_target
            self.y=y_target
            
    def turn_left(self):
        if self.orientation == 7 :
            self.orientation =0
        else :
            self.orientation =self.orientation +1
    def turn_right(self):
        if self.orientation == 0 :
            self.orientation = 7
        else :
            self.orientation = self.orientation -1
    
        
    def get_sensors_value(self,circuit):
        self.sensor_1.up_date_value(self.x,self.y,self.orientation,circuit)
        self.sensor_2.up_date_value(self.x,self.y,self.orientation,circuit)
        self.sensor_3.up_date_value(self.x,self.y,self.orientation,circuit)
        self.sensor_4.up_date_value(self.x,self.y,self.orientation,circuit)
        self.sensor_5.up_date_value(self.x,self.y,self.orientation,circuit)
        return ([self.sensor_1.value,self.sensor_2.value,self.sensor_3.value,self.sensor_4.value,self.sensor_5.value])
        

    def is_walled(self,circuit):
        I=len(circuit)-self.y
        J=self.x
        if sum(sum(circuit[I-2:I+2,J-2:J+2])) != 16 :
            L=self.get_sensors_value(circuit)
            a= L[0]+L[1]
            b= L[2]+L[3]
            if a < b :
                return ('l')
            else :    
                return('g')
        return(0)

    def update_range(self,new_range):
        self.sensor_1.range=new_range
        self.sensor_2.range=new_range
        self.sensor_3.range=new_range
        self.sensor_4.range=new_range
        self.sensor_5.range=new_range

    def draw(self,circuit):
        x=self.x
        y=self.y
        orientation = self.orientation
        angle =int((((orientation)*np.pi)/4)*(180/np.pi))
        image_with_car=np.copy(circuit)
        im_car = triangle()
        im_car=scipy.ndimage.rotate(im_car,angle)
        im_car=clean(im_car)
        len_cir =len(circuit)
        len_cir0=len(circuit[0])
        I=len_cir-y
        J=x
        a=int(len(im_car[0])/2)
        b=int(len(im_car)/2)
        len_imJ = len(image_with_car[0])
        len_imI =len(image_with_car)
        for i in range (max(0,I-b),min(I+b,len_imI-1)):
            for j in range (max(0,J-a),min(J+a,len_imJ-1)):
                if im_car[i-I+b][j-J+a]!=0:
                    image_with_car[i][j]=0.4
        rang=self.sensor_1.range
        L_1=list_vec_to_check(rang,orientation*(np.pi/4),-2*(np.pi/8) , x, y)
        L_2=list_vec_to_check(rang,orientation*(np.pi/4),-1*(np.pi/8) , x, y)
        L_3=list_vec_to_check(rang,orientation*(np.pi/4),0*(np.pi/8) , x, y)
        L_4=list_vec_to_check(rang,orientation*(np.pi/4),1*(np.pi/8) , x, y)
        L_5=list_vec_to_check(rang,orientation*(np.pi/4),2*(np.pi/8) , x, y)
        L=[L_1,L_2,L_3,L_4,L_5]
        for l in L :
            for couple in l :
                X=couple[0]
                Y=couple[1]
                i = min(len_cir-1,max(0,int(len_cir-Y)))
                j = min(len_cir0-1,max(0,int(X)))
                if circuit[i][j] == 0:
                    break
                else :
                    image_with_car[i][j] = 0
        plt.imshow(image_with_car)


    def distance(self,chemin):
        k=0
        K=[]
        L_dist=[]
        for i in range (len(chemin)-1):
            x_i_1=chemin[i][0]
            x_i_2=chemin[i+1][0]
            y_i_1=chemin[i][1]
            y_i_2=chemin[i+1][1]
            for j in range (1,101):
                alpha = j/100
                x_j= alpha*(x_i_2-x_i_1)+x_i_1
                y_j= alpha*(y_i_2-y_i_1)+y_i_1
                L_dist.append(np.sqrt((self.x-x_j)**2+(self.y-y_j)**2))
                K.append(k)
                k+=1
        return(K[np.argmin(L_dist)]/len(K))
