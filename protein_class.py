import dataframefunction as frames
import pandas as pd
import numpy as np
import os

class Protein:
    # Initializer / Instance attributes
    def __init__(self, name, filePath, energy = 0): #Default directory is current working directory
        self.filePath = filePath #1
        self.name = name #2
        self.df = df #preprocessed pandas dataframe
        self.energy = energy #4

    # Returns the name of the protein and the file path associated with it
    def description(self, filePath, name):
        return "{}: {}".format(self.name, self.filePath)

    def setPath(self, filePath):
        try:
            with os.path.exists(filePath):
                self.filePath = filePath
        except IOError:
            return "Please pass a valid file path, {} does not exist".format(self.filePath)

    def rename(self, name):
        self.name = input("Please enter a name: ")

    def df(self, filePath):
        self.df = frames(filePath)
