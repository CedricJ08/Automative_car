# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 19:22:54 2018

@author: Alu
"""

import numpy as np



class NN_unsup :
    def __init__(self,input_dim,output_dim,hidden_layers_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_layers_dim = hidden_layers_dim
        self.nb_hidden_layers = len(hidden_layers_dim)
        layers_dim = [self.input_dim]+self.hidden_layers_dim+[self.output_dim]
        len_entrlay=len(layers_dim)-1
        self.W = np.array([np.random.rand(layers_dim[len_entrlay-i],layers_dim[len_entrlay-i-1])/(layers_dim[len_entrlay-i-1]*layers_dim[len_entrlay-i]) for i in range (len_entrlay)])
        self.b = np.array([np.random.rand(layers_dim[len_entrlay-i])/(layers_dim[len_entrlay-i]) for i in range (len_entrlay)])
        
    def predict(self,x,W,b):
        layers_dim = [self.input_dim]+self.hidden_layers_dim+[self.output_dim]
        len_entrlay=len(layers_dim)-1
        z= []
        a= [x]
        for i in range (len_entrlay-1):
            z_i=np.dot(W[len_entrlay-1-i],a[i])+b[len_entrlay-1-i]
            a_i=np.tanh(z_i)
            z.append(z_i)
            a.append(a_i)
        z_i=np.dot(W[0],a[len_entrlay-1])+b[0]
        return(1/(1+np.exp(-z_i)))
        
    def generate_rdm_W(self):
        layers_dim = [self.input_dim]+self.hidden_layers_dim+[self.output_dim]
        len_entrlay=len(layers_dim)-1
        return(np.array([np.random.uniform(-1,1,(layers_dim[len_entrlay-i],layers_dim[len_entrlay-i-1]))/(layers_dim[len_entrlay-i-1]*layers_dim[len_entrlay-i]) for i in range (len_entrlay)]))

    def generate_rdm_b(self):
        layers_dim = [self.input_dim]+self.hidden_layers_dim+[self.output_dim]
        len_entrlay=len(layers_dim)-1
        return(np.array([np.random.uniform(-1,1,layers_dim[len_entrlay-i])/(layers_dim[len_entrlay-i]) for i in range (len_entrlay)]))

