# Our interactive executable file. Runs a protein energy analysis based on user input.
from protein_class import Protein
from dict_output import make_dictionary
from dataframefunction import check_if_crd, final_comparison_df
import ecalc as e
import os
from timeit import default_timer as timer
import numpy as np
import json
import csv

if __name__=='__main__':      
    print(f"Hello and welcome to our protein energy calculation tool! Please enter \"quit\" or \"q\" to exit at any prompt.")
    q = bool()
    while (True):
        # This check ensures that when the analysis is finished, and the user does not wish to run another, that the program quits.
        if (q==True):
            break
        else:
            user_choice = str()
            while (True):
                user_choice = input(f"Do you wish to run a standalone analysis or replicate the method used in our report? Enter \"1\" for standalone analysis, \"2\" to replicate: ")
                if (user_choice == "1" or 
                    user_choice == "2"):
                    break
                elif (user_choice.casefold() == "quit" or 
                      user_choice.casefold() == "q"):
                    q = True
                    break
                else:
                    continue
            # This allows the user to completetely quit at the first prompt, without asking if they want to run another analysis.
            if (q==True):
                break
            else:
                if int(user_choice) == 1:
                    done = bool
                    # This while condition causes the  program to break out of both loops at once, sending it to the "run again" prompt at the very end.
                    while (done !=True):
                        user_choice = input(f"Please enter a Unix path to a file or directory for analysis: ")
                        # This section is present after all input prompts, allowing the user to 
                        if (user_choice == "quit" or 
                            user_choice == "q"):
                            break
                        else:
                            path = user_choice
                            # Check that the path exists. If not, return an error and repeat the input prompt.
                            if(os.path.exists(path)):
                                # Check if the path is a directory and not a file.
                                if(os.path.isdir(path) and not(os.path.isfile(path))):
                                    # Check that the directory is not empty.
                                    if(len(os.listdir(path))>=1):
                                        while (True):
                                            # Assess the depth of the directory tree. Can handle 1 level of subfolders, but cannot handle nested subfolders.
                                            user_choice = input(f"Does the directory specified contain subfolders for each protein, which further contain file for analysis (y/n)? ")
                                            if (user_choice.casefold() == "quit" or 
                                                user_choice.casefold() == "q"):
                                                break
                                            else:
                                                if (user_choice.casefold() == "y" or 
                                                    user_choice.casefold() =="yes"):
                                                    start = timer()
                                                    final_output, final_df = make_dictionary(path, subfolders = True)
                                                    end = timer()
                                                    # Output the time it took to run the analysis.
                                                    time_elapsed = (end-start)
                                                    # Save the dictionary output to a json file in the working directory.
                                                    with open('final_dict_output', 'w') as fp:
                                                        json.dump(final_output, fp, indent = 4)
                                                    # Save the final dataframe output to a csv, also in the working directory. 
                                                    final_df.to_csv("final_df_output", header=True, index=True, index_label = False)
                                                    # Output the time it took to run the analysis.
                                                    print(f"Analysis complete, calculated in {time_elapsed} seconds.")
                                                    done = True
                                                    break
                                                elif (user_choice.casefold() == "n" or 
                                                      user_choice.casefold() == "no"):
                                                    start = timer()
                                                    final_output, final_df = make_dictionary(path, subfolders = False)
                                                    end = timer()
                                                    time_elapsed = (end-start)
                                                    with open('final_dict_output', 'w') as fp:
                                                        json.dump(final_output, fp, indent = 4)
                                                    # Save the final dataframe output to a csv.
                                                    final_df.to_csv("final_df_output", header=True, index=True, index_label = False) 
                                                    # Output the time it took to run the analysis.
                                                    print(f"Analysis complete, calculated in {time_elapsed} seconds.")
                                                    done = True
                                                    break
                                                else:
                                                    # If the user enters an unknown input, repeat the input prompt.
                                                    continue 
                                    else:
                                        print(f"[ERROR] The provided directory appears to be empty, please add files for analysis.")
                                        continue
                                elif(os.path.isfile(path)):
                                    check, mod_files, types = check_if_crd(path)
                                    split = os.path.split(path)
                                    sub_path = split[0]
                                    name = split[1]
                                    # Check to see if the query file is a .crd file. 
                                    if check[0] == True:
                                        protein = Protein(filePath=sub_path+os.sep, name=name)
                                        start = timer()
                                        protein_energy, vdw_energies, solvation_energies = e.energy(protein)
                                        end = timer()
                                        time_elapsed = (end-start)
                                        # Saves all 3 values to a names fie. Used for histogram creation and analysis
                                        with open(f"{name}_energy_output", 'w', newline='') as file:
                                            writer = csv.writer(file)
                                            writer.writerow([protein_energy])
                                            
                                        # Save np arrays using numpy
                                        np.savetxt(f"{name}_vdw_energies", vdw_energies)
                                        np.savetxt(f"{name}_solvation_energies", solvation_energies)
                                        print(f"Protein {name} has an internal energy of {protein_energy} kcal/mol")
                                        print(f"Analysis completed in {time_elapsed} seconds.")
                                        break
                                    else:
                                        print(f"[ERROR] The file path entered does not seem to be a .crd file. If this is a mistake, add \".crd\" to the end of the file for analysis.")
                                        continue
                            else:
                                print(f"[ERROR] The following path does not exist: {path}")
                                continue
                elif int(user_choice) == 2:
                    # Repeat the same error catching procedure as shown above, this time for two file paths instead of just one. 
                    path1 = str()
                    path2 = str()
                    while (True):
                        user_choice = input(f"Please enter the path to the parent directory containing all Robetta subdirectories and files: ")
                        if (user_choice == "q" or 
                            user_choice == "quit"):
                            q = True
                            break
                        else:
                            if (os.path.exists(user_choice)):
                                if(os.path.isdir(user_choice) and not(os.path.isfile(user_choice))):
                                    if(len(os.listdir(user_choice))>=1):
                                        path1=user_choice
                                        break
                                    else:
                                        print(f"[ERROR] The provided directory appears to be empty.")
                                        continue
                                elif(os.path.isfile(path1)):
                                    print(f"[ERROR] To replicate our analysis, please enter a path to a directory, not a file.")
                                    continue
                            else:
                                print(f"[ERROR] The following path does not exist: {user_choice}")
                                continue
                    if(q==True):
                        break
                    else:
                        while (True):
                            user_choice = input(f"Please enter the path to the parent directory containing all trRosetta subdirectories and files: ")
                            if (user_choice == "q" or 
                                user_choice == "quit"):
                                q = True
                                break
                            else:
                                if (os.path.exists(user_choice)):
                                    if(os.path.isdir(user_choice) and not(os.path.isfile(user_choice))):
                                        if(len(os.listdir(user_choice))>=1):
                                            path2 = user_choice
                                            break
                                        else:
                                            print(f"[ERROR] The provided directory appears to be empty, please add files for analysis.")
                                            continue
                                    elif(os.path.isfile(user_choice)):
                                        print(f"[ERROR] To replicate our analysis, please enter a path to a directory, not a file.")
                                        continue
                                else:
                                    print(f"[ERROR] The following path does not exist: {user_choice}")
                                    continue
                        if (q==True):
                            break
                        else:
                            # Run two seperate analyses for each platform and summarize each. 
                            start = timer()    
                            robetta_summary = make_dictionary(path1, subfolders = True)
                            trRosetta_summary = make_dictionary(path2, subfolders = True)
                            end = timer()
                            time_elapsed = (end-start)
                            print(f"Analysis completed in {time_elapsed} seconds. Saving summary files...")
                            
                            # Save all files to properly named csv files in the current working directory. 
                            robetta_summary_df = robetta_summary[1]
                            robetta_summary_df.to_csv("Robetta_Summary.csv", header=True, index=True, index_label = False) 
    
                            trRosetta_summary_df= trRosetta_summary[1]
                            trRosetta_summary_df.to_csv("trRosetta_Summary.csv", header=True, index=True, index_label = False) 
    
                            concat_output = final_comparison_df(df1 = robetta_summary_df, df2 = trRosetta_summary_df)
                            concat_output.to_csv("Final_Summary.csv", header=True, index=True, index_label = False)
                            # Tells the user when it is finished. 
                            print(f"Saved \"Robetta_Summary.csv\"\, \"trRosetta_Summary.csv\"\, and \"Final_Summary.csv\" to current working directory.")
        # This prompt allows the user to run another analysis or redo a step due to a typographical error. Quiting here will exit the program. 
        while (True):
            user_choice = input(f"Would you like to run another analysis? (y/n/quit) ")
            if (user_choice.casefold() == "n" or 
                user_choice.casefold() == "no" or 
                user_choice.casefold() == "q" or 
                user_choice.casefold() == "quit"):
                q = True
                break
            elif (user_choice.casefold() == "y" or 
                  user_choice.casefold() == "yes"):
                q = False
                break
            else:
                continue