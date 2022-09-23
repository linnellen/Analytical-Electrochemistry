# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:06:49 2022

@author: lkelley
"""
# Begin by defining a class. A class is a data type that contains attributes 
# (similar to variables) and methods (functions) that can only be accessed by 
# creating an instance of the class (object). 

class SumMult(object):
    # The __init__ (initiate) function is part of all classes and is used to 
    # define user inputs required to initiate an instance of the class. The 
    # variable, self, refers to the specific object made by creating an 
    # instance of the class. 
    def __init__(self,x,y):
        # Assign attributes to the object as self.attribute = value/variable.
        # It is common to start by making the user inputs attributes.
        self.x = x
        self.y = y
        # Attrirbutes can be created that are not user inputs.
        self.sum = x+y
    # Methods are created by writing functions. Make sure to include the self
    # variable so the function can access all object attributes. By doing this
    # it is unnecessary to have function inputs for variables that are function
    # attrirbutes. Function inputs that are not object attributes must be 
    # specified.     
    def multiply(self,factor):
        self.mult = self.x*self.y*factor
        
#%%
# Create an object which is an instance of the class SumMult.
new_object = SumMult(1,4)

#%%
# Add the attribute mult to the object using the multiply function.
SumMult.multiply(new_object,2)

#%%
# Print the attribute, mult, in the console. 
print(new_object.mult)

