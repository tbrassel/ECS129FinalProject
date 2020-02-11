#Main method, our actual executable file 
from dataframefunction import frames
from protein_class import Protein
import ecalc as e
import pandas as pd
import numpy as np
import os

if __name__=='__main__':
    path = "/home/tyler/ECS129FinalProjectInput/"
    name = "model1.crd"
    protein1 = Protein(filePath=path, name=name)
    print(protein1) #__repr__#
    dftest = protein1.dataframe() #dataframe stored into variable in this form
    print(dftest) #check output
    protein1_energy = e.energy(dftest) 
    print(f"{name} has an energy value of {protein1_energy}")
    
