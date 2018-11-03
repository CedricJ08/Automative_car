# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 23:37:33 2018

@author: Alu
"""


import numpy as np

from Circuit_object import Circuit
from Non_supervised_NN import  NN_unsup
from Car_object import Car






def main (epochs,nb_cars,lr) :
    C=Circuit()
    circuit = C.get_circuit()
    path = C.get_path(circuit)
    nbepo=epochs
    nb_cars=nb_cars
    NN=NN_unsup(5,2,[4])
    epo=0
    lr_max=lr
#    lr_min=0.01
    layers_dim = [NN.input_dim]+NN.hidden_layers_dim+[NN.output_dim]
    len_entrlay=len(layers_dim)-1
    
    
    while epo < nbepo :
        epo = epo+ 1
        print(epo)
        Cars=[Car(C.dep,2) for i in range (nb_cars)]
        distances = []
        Ws=[]
        bs=[]
    #    lr=lr_max*np.exp(-((1/nbepo)*np.log(lr_max/lr_min))*epo)
        lr=lr_max
        k=0
        for car in Cars :
            k+=1
            print(k)
            dist=0
            Gr_W= lr*np.array([np.random.uniform(-1,1,(layers_dim[len_entrlay-i],layers_dim[len_entrlay-i-1]))/(layers_dim[len_entrlay-i-1]*layers_dim[len_entrlay-i]) for i in range (len_entrlay)])
            GR_b= lr*np.array([np.random.uniform(-1,1,layers_dim[len_entrlay-i])/(layers_dim[len_entrlay-i]) for i in range (len_entrlay)])
            W=NN.W+Gr_W
            b=NN.b+GR_b
            Ws.append(W)
            bs.append(b)
            while car.is_walled(circuit)==0 :
                pred=NN.predict(np.array(car.get_sensors_value(circuit)),W,b)
                if float( pred[0]-pred[1] ) > 0.5 :
                    car.turn_right()
                if float( pred[0]-pred[1] ) < -0.5 :
                    car.turn_left()
                car.move_forward(2)
            dist=car.distance(path)
            distances.append( dist )
        print(distances[np.argmax(distances)])
        NN.W=Ws[np.argmax(distances)]
        NN.b=bs[np.argmax(distances)]










        