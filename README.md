# ECS129 Final Project: Computing the Energy of a Protein Structure
A simple interactive Python program to calculate and compare protein structure energies.

## Quick Start Guide
Our main executable file ```main.py``` imports the following files: ```ecalc.py```, ```protein_class.py```, ```dataframefunction.py```, and ```dict_output.py```. We used Python 3.7.6 as well as Spyder IDE for development. All outputs are placed in the current working directory.

## Protein selection
Protein are selected using R script. R studio will support the ```Protein.selection.rmd```

## Clean up
Official pdb clean ups and server-predicted pdb clean ups can be find in clean_up folder

## Visualization of protein sturcture
Protein sturctures are visualized and compared using [SwissPdb Viewer](https://spdbv.vital-it.ch/). 

## Reproducing our Results
We requested the conversion of many pdb files to crd. All of these files are contained within the zip archive titled "Platform_Analysis_Input" should one wish to replicate our data analysis.

## Team
- __Tyler Brassel__: Ecalc functions. Pipeline builder.
- __Xinzhe Li__: protein selection, visualization
- __Yinuo Zhang__: pdb clean ups, data frame processing
