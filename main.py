#Main method, our actual executable file
#call Energy calc class and dataframe class(object):

#Todo: need extra class to define neighbor

from protein_class import Protein

path = ""
model_name1 = ""
model_name2 = ""
protein1 = Protein(path, model_name1)
protein2 = Protein(path, model_name2)

Predicted_model = Engergy(protein1.dataframe, protein2.dataframe)

result = Predicted_model.Energy_diff
