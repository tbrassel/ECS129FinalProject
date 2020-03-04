#Main method, our actual executable file 
from dataframefunction import frames
from protein_class import Protein
from dict_output import make_dictionary
import ecalc as e
import pandas as pd
import numpy as np
from functools import reduce
import os
import re

if __name__=='__main__':
   path = "/home/tyler/ECS129FinalProjectInput/"
   #namelist = list()
   #with os.scandir(path) as entries:
       #for entry in entries:
           #Use list unpacking to create the list of filenames in the subdirectory
           #namelist = [*namelist, entry.name]
   #Sort the filenames in ascending order
   #namelist.sort(key=lambda f: int(re.sub('\D', '', f)))
    
   #for i in range(0, len(namelist)):
      #name = namelist[i]
      #protein = Protein(filePath=path, name=name)
      #protein_energy = e.energy(protein) 
      #print(f"{name} has an energy value of {protein_energy}")

   #Testing functions:
   #protein1 = Protein(filePath=path, name = "model01.crd")
   #print(protein1) #__repr__#
   #dftest = protein1.dataframe() #dataframe stored into variable in this form
   #print(dftest) #check outputdef get_sanitized_input(path_to_dir):
#Does not work yet:
def get_sanitized_input(path, subfolders=False, summary=True):
    try:
        if os.path.exists(path) and os.path.isdir(path):
            if not(os.listdir(path)):
                print(f"The directory entered appears to be empty, please add files for analysis.")
            else:
                to_process = len(os.listdir(path))
                if(subfolders == False):
                    print(f"Processing {to_process} files in the following directory: {path}")
                else:
                    print(f"Found {to_process} folders in the following directory: {path}")
            final_output = make_dictionary(path, subfolders, summary)
            return final_output
    except IOError:
        raise (f"Please pass a valid directory path, {path} does not exist")

output_dict, output_df = get_sanitized_input(path, subfolders=True, summary=True)
output_df.to_csv('summary.csv', header=False, index=True) 

#Specify whether or not you are passing a folder with 1 layer of subfolders for multiple proteins
#Or just a folder with no subfolders for analysis of 1 protein.
#final_output = make_dictionary(path, subfolders=False)

