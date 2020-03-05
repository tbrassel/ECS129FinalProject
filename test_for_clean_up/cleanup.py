from Bio.PDB import *
from Bio.PDB.Polypeptide import PPBuilder, three_to_one
from Bio.Seq import Seq
from Bio.Alphabet import generic_protein
import os

'''get the valid residues presented in the 'official' pdbs publicated'''
name = 'igf1_igzy'
p=PDBParser()
official_structure = p.get_structure(name,'1gzy.pdb')
ppb=PPBuilder()
residue_valid = []#potential breaks in sequences of the published pdb files
for pp in ppb.build_peptides(official_structure):
    residue_valid.append(pp.get_sequence())

'''clean up pdb files generated from server
    Only select the a.a. that present in the published pdbs from server output
'''
os.system('mkdir intermediate_files')
server_structure = p.get_structure('server_model','model1.pdb')

class RecordingSelected(Select):
    def accept_residue(self, residue):
        if residue in processing_valid_info:
            return 1
        else:
            return 0

class SiteSelect:
    def __init__(self, valid):
        self.valid = valid
        self.different_domains = len(self.valid)
        self.check = []
        for n in range(self.different_domains):
            self.check.append(0)

    def selecting_valid_residues(self,structure, verbose = False):
        residues_to_be_checked = []
        real_residue_label = []
        output = []
        for residue_ in structure.get_residues():
            real_residue_label.append(residue_)
            residues_to_be_checked.append(residue_.get_resname())
        count = 0
        if verbose: print(self.valid)
        for m in range(self.different_domains):
            for i in range(0, len(residues_to_be_checked)-len(self.valid[m])+1):
                count += 1
                sequence_to_check = residues_to_be_checked[i:i+len(self.valid[m])]
                one_letter_code = ''.join(three_to_one(x) for x in sequence_to_check)
                if one_letter_code == self.valid[m]:
                    self.check[m] = 1
                    if verbose: print(one_letter_code, self.valid[m])
                    break
                else:
                    pass
                #print(sequence_to_check)
            if self.check[m] == 1:
                output = output + real_residue_label[i:i+len(self.valid[m])]#list concat

        if all(self.check):
            return output
        else:
            print('no matched up sequences between official structure and server prediction')

io = PDBIO()
io.set_structure(server_structure)
global processing_valid_info
processing_valid_info = SiteSelect(residue_valid).selecting_valid_residues(server_structure)
if processing_valid_info is not None:
    io.save('valid_%s.pdb' % name,RecordingSelected())
else:
    print('no matched up sequences between official structure and server prediction')

'''Cleaningup--Get rid of hydrogen atoms'''
class HydrogenSelect(Select):
    def accept_atom(self, atom):
        if 'H' not in atom.get_name() or atom.get_name() == 'OH'or 'NH'in atom.get_name():
            return 1
        else:
            return 0

new_structure = p.get_structure('newmodel','valid_%s.pdb' % name)
io.set_structure(new_structure)
io.save('cleaned_up_%s.pdb'%name, HydrogenSelect())
os.system('mv valid_*.pdb intermediate_files')
