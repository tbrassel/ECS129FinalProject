#Module for processing and managing dataframes and files
import pandas as pd
import os
from functools import reduce

def frames(filePath, name):
    file = open(filePath+name)
    number_of_rows =int(file.readline())
    file.close()
    df = (pd.read_csv(filePath+name, skiprows = 2,delim_whitespace=True,header=None, index_col=None)).head(number_of_rows)
    df2 = (pd.read_csv(filePath+name, delim_whitespace=True,skiprows=2,header=None)).tail(number_of_rows)
    try:
        if len(df.columns) == 13 and len(df2.columns) == 13:
            df.drop(df.columns[-2],axis=1,inplace=True)
            df2.drop(df.columns[-2],axis=1,inplace=True)
        elif len(df.columns) == 12 and len(df2.columns) == 12:
            pass
    except ValueError:
        raise "please keep a constant input shape"
    df.columns = ['i','X','Y','Z','R','Epsilon','Sigma','Charge','ASP','Atm_name','Res_name','Res']
    realcolumns = ['i','Nexclude','E_list','NA1','NA2','NA3','NA4','NA5','NA6','NA7','NA8','NA9']
    df2.columns = realcolumns
    df.Res = df['Res'].astype(int)
    df2['Combined'] = df2[realcolumns[2:]].apply(lambda x: [(int(val)-1) for val in x if not pd.isnull(val)], axis=1)
    df2.drop(realcolumns[2:12],axis  = 1, inplace=True)
    df3 = pd.merge(df,df2,on = ['i'])
    df3.drop(['i'],axis = 1,inplace = True)
    return df3

def final_comparison_df(df1, df2):
    concat_output = pd.DataFrame()
    print(f"I ran")
    for i in range(0, (len(df1))):
       value1 = df1.iloc[i, 1] 
       value2 = df2.iloc[i, 1]
       if(value1<value2):
           concat_output = concat_output.append(df1.iloc[[i]])
       elif(value1>value2):
           concat_output = concat_output.append(df2.iloc[[i]])
    return concat_output

def check_if_crd(file_list):
    if isinstance(file_list, str):
        file_list = [file_list]
    mod_files = list()
    types = list()
    crd_check = list()
    for i in range(0, len(file_list)):
        split = os.path.splitext(file_list[i])
        mod_files.append(split[0])
        types.append(split[1])
        if types[i]==".crd":
            crd_check.append(True)
        else:
            crd_check.append(False)
    return crd_check, mod_files, types 
                





