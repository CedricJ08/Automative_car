# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 11:50:46 2018

@author: Alu
"""
import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt

from Circuit_object import Circuit
from Non_supervised_NN import  NN_unsup
from Car_object import Car





C=Circuit()
circuit = C.get_circuit()
path = C.get_path(circuit)
NN=NN_unsup(5,2,[3])
lr=10
Distances=[]
Positions=[]
for i in range (50):
    Position=[]
    Ldistance=[]
    L_W=[]
    L_b=[]
    cars = [Car(C.dep,2) for i in range (30)]
    j=0
    for car in cars :
        Position.append([])
        Gr_W= lr*NN.generate_rdm_W()
        GR_b= lr*NN.generate_rdm_b()
        W=NN.W+Gr_W
        b=NN.b+GR_b
        k=0
        while car.is_walled(circuit)==0 and k < 900:
            Position[j].append((car.x,car.y))
            k+=1
            x=np.array(car.get_sensors_value(circuit))
            pred=NN.predict(x,W,b)
            if float(abs(pred[0]-pred[1])) > 0:
                if float( pred[0]-pred[1] ) > 0 :
                    car.turn_right()
                if float( pred[0]-pred[1] ) < 0 :
                    car.turn_left()
            car.move_forward(2,circuit)
        j+=1
        Ldistance.append(car.distance(path))
        L_W.append(W)
        L_b.append(b)
        
    indice = np.argmax(Ldistance)
    distance=Ldistance[indice]
    Distances.append(distance)
    NN.W=L_W[indice]
    NN.b=L_b[indice]
    Positions.append(Position[indice])
    print ('progress: '+str(i*2)+' %')

def get_best():
    best_pos=[Positions[0]]
    dis = Distances[0]
    best_dist=[dis]
    for i in range (1,len(Positions)):
        if Distances[i]>dis:
            dis = Distances[i]
            best_pos.append(Positions[i])
            best_dist.append(Distances[i])
        


def draww(pos,circuit,i):
    image_with_points=np.copy(circuit)
    for point in pos[i] :
        J_im = point[0]
        I_im = len(circuit)-point[1]
        for u in range (I_im-2,I_im+2):
            for v in range (J_im-2,J_im+2):
                image_with_points[u][v] = 0
    plt.imshow(image_with_points)




def try_other_path(debart=(195,310),end=(680,150),path_circuit='trajet_test.png',NN_test=NN):
    car_test = Car(debart,0)
    C_test=Circuit(dep=debart,fin=end,path=path_circuit)
    circuit_test = C_test.get_circuit()
    k=0
    while car_test.is_walled(circuit)==0 and k < 500:
        k+=1
        x=np.array(car_test.get_sensors_value(circuit_test))
        pred=NN_test.predict(x,NN_test.W,NN_test.b)
        if float(abs(pred[0]-pred[1])) > 0:
            if float( pred[0]-pred[1] ) > 0 :
                car_test.turn_right()
            if float( pred[0]-pred[1] ) < 0 :
                car_test.turn_left()
        car_test.move_forward(2,circuit)
    car_test.draw(circuit_test)


