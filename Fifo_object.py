# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:34:44 2018

@author: Alu
"""




class FIFO :
    def __init__(self,size):
        self.size = size
        self.list = []
        
    def is_empty(self):
        if self.list==[]:
            return(True)
        return (False)
    
    def add(self,value):
        self.list.append(value)
        if len(self.list) > self.size :
            self.list.pop(0)
        
    def last(self,i):
        return (self.list[len(self.list)-1-i])