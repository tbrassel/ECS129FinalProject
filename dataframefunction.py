#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
#save the output of this function into variable in master protocol

# In[16]:


path = '/Users/mac/Desktop/'


# In[ ]:


def frames(file_name):
    df = (pd.read_csv(path+file_name,skiprows = 2,delim_whitespace=True,header=None)).head(2288)
    df.columns = ['i','X','Y','Z','R','Epsilon','Sigma','Charge','ASP','Atm_name','Res_name','Res']
    df.Res = df['Res'].astype(int)
    realcolumns = ['i','Nexclude','E_list','NA1','NA2','NA3','NA4','NA5','NA6','NA7','NA8','NA9']
    df2 = (pd.read_csv(path+file_name, delim_whitespace=True,skiprows=2,header=None,names = realcolumns)).tail(2288)
    df2['Combined'] = df2[realcolumns[2:]].apply(lambda x: [(int(val)-1) for val in x if not pd.isnull(val)], axis=1)
    df2 = df2.drop(realcolumns[2:12],axis  = 1)
    df3 = pd.merge(df,df2,on = ['i'])
    df3 = df3.drop(['i'],axis = 1)
    return df3

if __name__ == '__main__':
	name = ['model1.crd','model2.crd']
	for i in range(len(name)):
    		df = frames(name[i])
    		pd.DataFrame.to_csv(df, path+name[i],index=False)


# In[ ]:




