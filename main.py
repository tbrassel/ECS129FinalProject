#Main method, our actual executable file 
from dataframefunction import frames, get_directory_structure
from protein_class import Protein
import ecalc as e
import pandas as pd
import numpy as np
import os
import re

if __name__=='__main__':
   path = "/home/tyler/ECS129FinalProjectInput/Protein2/"
    namelist = list()
    with os.scandir(path) as entries:
        for entry in entries:
            #Use list unpacking to create the list of filenames in the subdirectory
            namelist = [*namelist, entry.name]
    #Sort the filenames in ascending order
    namelist.sort(key=lambda f: int(re.sub('\D', '', f)))
    
    for i in range(0, len(namelist)):
       name = namelist[i]
       protein = Protein(filePath=path, name=name)
       protein_energy = e.energy(protein) 
       print(f"{name} has an energy value of {protein_energy}")

    # Testing functions:
   #protein1 = Protein(filePath=path, name = "model01.crd")
   #print(protein1) #__repr__#
   #dftest = protein1.dataframe() #dataframe stored into variable in this form
   #print(dftest) #check output
    # dir = get_directory_structure(path)
    
