#Main method, our actual executable file 
from dataframefunction import frames, check_if_crd, final_comparison_df
from protein_class import Protein
from dict_output import make_dictionary
import ecalc as e
import pandas as pd
import numpy as np
from functools import reduce
import os
import re
import matplotlib.pyplot as plt

if __name__=='__main__':
    path1 = "/home/tyler/ECS129FinalProjectInput/ECS129_Robetta_crd/"
    path2 = "/home/tyler/ECS129FinalProjectInput/ECS129_trRosetta_crd/"
  
    #Testing functions:
    #protein1 = Protein(filePath=path, name = "model01.crd")
    #print(protein1) #__repr__#
    #dftest = protein1.dataframe() #dataframe stored into variable in this form
    #print(dftest) #check outputdef get_sanitized_input(path_to_dir):

    #output_df.to_csv('Robetta_summary.csv', header=True, index=True, index_label = False) 
    #robetta = pd.read_csv('Robetta_summary.csv')
    #trRosetta = pd.read_csv('trRosetta_summary.csv')

    
    #Specify whether or not you are passing a folder with 1 layer of subfolders for multiple proteins
    #Or just a folder with no subfolders for analysis of 1 protein.
    def process_input(path, subfolders = True, summary = True):
        try:
            assert(os.path.exists(path))
        except AssertionError as error:
                print(error)
                print(f"The following path does not exist: {path}")
        else:
            if(os.path.isdir(path) and not(os.path.isfile(path))):
                try:
                    assert(len(os.listdir(path))>=1)
                except AssertionError as error:
                    return(error)
                    print(f"The provided directory appears to be empty, please add files for analysis")
                else:
                    print(f"The path exists and is a non-empty directory")
                    final_output = make_dictionary(path, subfolders, summary)
                    return final_output
            elif(os.path.isfile(path)):
                check, mod_files, types = check_if_crd(path)
                split = os.path.split(path)
                sub_path = split[0]
                name = split[1]
                #print(f"The path {path} exists and is a file.")
                try:
                    assert(check[0] == True)
                except AssertionError as error:
                    print(error)
                    print(f"The specified file {name} is not a .crd file.")
                else:
                    protein = Protein(filePath=sub_path+os.sep, name=name)
                    protein_energy = e.energy(protein)
                    final_output = protein_energy
                    #print(f"Protein {name} has energy {protein_energy}")
                    return final_output
    
    robetta_summary = process_input(path1)
    trRosetta_summary = process_input(path2)
    
    robetta_summary_df = robetta_summary[1]
    robetta_summary_df.to_csv('Robetta_Summary.csv', header=True, index=True, index_label = False) 
    
    trRosetta_summary_df= trRosetta_summary[1]
    trRosetta_summary_df.to_csv('trRosetta_Summary.csv', header=True, index=True, index_label = False) 
    
    concat_output = final_comparison_df(df1 = robetta_summary_df, df2 = trRosetta_summary_df)
    concat_output.to_csv('Final_Summary.csv', header=True, index=True, index_label = False) 