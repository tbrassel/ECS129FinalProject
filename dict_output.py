from protein_class import Protein
import pandas as pd
import ecalc as e
from functools import reduce
import os
import re

def make_dictionary(rootdir, subfolders: bool, summary: bool):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir1 = {}
    #The following line makes the input flexible as to whether or not the user
    #passes a "/" at the end of their path name, using os.sep for Windows and Linux
    rootdir = rootdir.rstrip(os.sep)
    print(f"This is rootdir: {rootdir}")
    start = rootdir.rfind(os.sep) + 1
    print(f"This is start: {start}")
    types = list() #.crd
    energies = list()
    indexes = list()
    values = list()
    mod_files = list() #stores the filenames
    for path, dirs, files in os.walk(rootdir, topdown=True):
        folders = path[start:].split(os.sep)
        print(f"These are the folders: {folders}")
        for i in range(0, len(files)):
           split = os.path.splitext(files[i])
           mod_files.append(split[0])
           types.append(split[1])
           
        files.sort(key=lambda f: int(re.sub('\D', '', f))) #Returns the names in ascending numerical order
        #If we have walked the first parent folder and are looping through the subfolders, calculate energies
        if((len(folders)>1 and subfolders)): 
            sub_path = os.path.join(rootdir, folders[1]+os.sep)
            print(f"This is the sub_path: {sub_path}")
            #Do stuff...
            for j in range(0, len(files)):
                protein = Protein(filePath = sub_path, name = files[j])
                energies.append(e.energy(protein))
            
            # Dictionary comprehension to initialize dictionary with a list of values
            tuples = tuple(zip(files, energies))
            print("Unordered tuples: {tuples}")
            tuples = sorted(tuples, key=lambda x: x[1])
            indexes.append(folders[1])
            values.append(tuples[0])
            print(f"Ordered tuples: {tuples}")
            subdir = {key:value for key, value in tuples}
            print(f"These are the files: {files}")
            print(f"This is the subdir: {subdir}")
            parent = reduce(dict.get, folders[:-1], dir1)
            print(f"This is the parent before: {parent}")
            parent[folders[-1]] = subdir
            print(f"This is the parent after: {parent}")
            print(f"This is types: {types}")
            print(f"These are the modfiles: {mod_files}")
        elif(subfolders == False): #Else if no subfolders
            #Instead of getting a subpath, we just use the passed in file path
            #sub_path = os.path.join(rootdir, folders[1]+os.sep) ---> Returns an error if run here
            #print(f"This is the sub_path: {sub_path}") ---> This as well
            #Do stuff...
            for j in range(0, len(files)):
                protein = Protein(filePath = path+os.sep, name = files[j])
                energies.append(e.energy(protein))
            
            # Dictionary comprehension to initialize dictionary with a list of values
            subdir = {key:value for key, value in zip(files, energies)}
            print(f"These are the files: {files}")
            print(f"This is the subdir: {subdir}")
            parent = reduce(dict.get, folders[:-1], dir1)
            print(f"This is the parent before: {parent}")
            parent[folders[-1]] = subdir
            print(f"This is the parent after: {parent}")
            print(f"These are the types: {types}")
            print(f"These are the modfiles: {mod_files}")
        else: #Do this first if there are subfolders
            subdir = dict.fromkeys(files)
            print(f"These are the files: {files}")
            print(f"This is the subdir: {subdir}")
            parent = reduce(dict.get, folders[:-1], dir1)
            print(f"This is the parent before: {parent}")
            parent[folders[-1]] = subdir
            print(f"This is the parent after: {parent}")
            print(f"This is types: {types}")
            print(f"These are the modfiles: {mod_files}")
    if(summary==True):
        df = pd.DataFrame(data=values, index=indexes, columns = ["Model", "Energy (kcal/mol)"])
        
    return dir1, df

#def summary()