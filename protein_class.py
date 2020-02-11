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
        return f"{self.filePath}: {self.name}"

    def setPath(self, filePath):
        try:
            with os.path.exists(filePath):
                self.filePath = filePath
        except IOError:
            return f"Please pass a valid file path, {self.filePath} does not exist"

    def rename(self, name):
        self.name = input("Please enter names of models to compare in tuple: ")

    def dataframe(self):
        return frames(self.filePath, self.name)
        
