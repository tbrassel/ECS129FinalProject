from dataframefunction import frames
import pandas as pd
import numpy as np
import os

class Protein:
    # Initializer / Instance attributes
    def __init__(self, filePath, name, energy = 0): #Default directory is current working directory
        self.filePath = filePath #1
        self.name = name #2
        self.energy = energy #4

    # Returns the name of the protein and the file path associated with it
    # just print the object that been assigned with the class
    def __repr__(self):
        return "%s: %s" % (self.name, self.filePath)

    def setPath(self, filePath):
        try:
            with os.path.exists(filePath):
                self.filePath = filePath
        except IOError:
            return "Please pass a valid file path, {} does not exist".format(self.filePath)

    def rename(self, name):
        self.name = input("Please enter names of models to compare in tuple: ")

    def dataframe(self):
        return frames(self.filePath, self.name)
        
if __name__=='__main__':
    path = '/Users/mac/Desktop/'
    name = 'model1.crd'
    test = Protein(path, name)
    print(test) #__repr__#
    dftest = test.dataframe() #dataframe stored into variable in this form
    print(dftest) #check output
