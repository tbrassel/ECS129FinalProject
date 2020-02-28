#Module for processing and managing the dataframe
import pandas as pd
import os
from functools import reduce

def frames(filePath, name):
    df = (pd.read_csv(filePath+name, skiprows = 2,delim_whitespace=True,header=None, index_col=None)).head(2288)
    df.columns = ['i','X','Y','Z','R','Epsilon','Sigma','Charge','ASP','Atm_name','Res_name','Res']
    df.Res = df['Res'].astype(int)
    realcolumns = ['i','Nexclude','E_list','NA1','NA2','NA3','NA4','NA5','NA6','NA7','NA8','NA9']
    df2 = (pd.read_csv(filePath+name, delim_whitespace=True,skiprows=2,header=None,names = realcolumns)).tail(2288)
    df2['Combined'] = df2[realcolumns[2:]].apply(lambda x: [(int(val)-1) for val in x if not pd.isnull(val)], axis=1)
    df2 = df2.drop(realcolumns[2:12],axis  = 1)
    df3 = pd.merge(df,df2,on = ['i'])
    df3 = df3.drop(['i'],axis = 1)
    return df3

def get_sanitized_input(path_to_dir):
    while True:
        try:
            with os.path.exists(path_to_dir) and os.path.isdir(path_to_dir):
                if not os.listdir(path_to_dir):
                    return f"The directory entered appears to be empty, please add files for analysis."
                    continue
                else:
                    to_process = os.listdir(path_to_dir)
                    print(f"Processing {to_process} files... in folder ""{path_to_dir}.")
                    #for path_to_dir, sub_dirs, names in os.walk(path_to_dir, topdown=True):
        except IOError:
            return f"Please pass a valid directory path, {path_to_dir} does not exist"
            continue

def testwalk(path_to_dir):
    for root, dirs, files in os.walk("/home/tyler/ECS129FinalProjectInput/", topdown=True):
            for name in files:
                print(os.path.join(dirs[0], name))
                
def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    types = list()
    mod_files = list()
    for path, dirs, files in os.walk(rootdir, topdown=True):
        folders = path[start:].split(os.sep)
        for i in range(0, len(files)):
           split = os.path.splitext(files[i])
           mod_files.append(split[0])
           types.append(split[1])
           
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir


