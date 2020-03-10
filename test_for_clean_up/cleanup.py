from Bio.PDB import *
from Bio.PDB.Polypeptide import PPBuilder, three_to_one
from Bio.Seq import Seq
from Bio.Alphabet import generic_protein
import os,sys

class RecordingSelected(Select):
    def accept_residue(self, residue):
        if residue in processing_valid_info:
            return 1
        else:
            return 0
class chainReduce(Select):
    def accept_residue(self, residue):
        if residue.get_parent().id == 'A' and residue.get_resname() != 'HOH' \
        and residue.get_resname() != 'NAG' and residue.get_resname()!='ZD7'\
        and residue.get_resname() != ' CL' and residue.get_resname() != ' ZN'\
        and residue.get_resname() != 'N7O' and residue.get_resname() != 'UNL':
            return 1
        else:
            return 0
class modelReduce(Select):
    def accept_model(self, model):
        if model.id == 0:
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
                #print(len(one_letter_code), len(self.valid[m]))
            if self.check[m] == 1:
                output = output + real_residue_label[i:i+len(self.valid[m])]#list concat

        if all(self.check):
            return output
        else:
            print('no matched up sequences between official structure and server prediction')

class HydrogenSelect(Select):
    def accept_atom(self, atom):
        if 'H' not in atom.get_name() or atom.get_name() == 'OH'or 'NH'in atom.get_name():
            return 1
        else:
            return 0

os.system('mkdir intermediate_files')
p=PDBParser()
ppb=PPBuilder()
io = PDBIO()
'''one model version'''
name = 'ENSG00000092009_Robetta_model01'
protein_id = 'ENSG00000092009'
official_structure = p.get_structure(name,'%s_official.pdb'%protein_id)
residue_valid = []#potential breaks in sequences of the published pdb files
M_notneed = False
count = 0
model_count = 0
for model in official_structure:
    model_count += 1

if model_count >1:
    M_notneed = True

if M_notneed:
    io.set_structure(official_structure)
    io.save('%s_removeothermodel.pdb'% protein_id, modelReduce())
    io.set_structure(p.get_structure(name,'%s_removeothermodel.pdb'%protein_id))
    io.save('%s_removeotherchain.pdb'% protein_id, chainReduce())
    io.set_structure(p.get_structure(name,'%s_removeotherchain.pdb'%protein_id))
    io.save('%s_official_cleanup.pdb'%protein_id, HydrogenSelect())
    new_official_structure = p.get_structure(name,'%s_official_cleanup.pdb'%protein_id)
    for pp in ppb.build_peptides(new_official_structure):
        residue_valid.append(pp.get_sequence())
else:
    io.set_structure(official_structure)
    io.save('%s_removeotherchain.pdb'% protein_id, chainReduce())
    io.set_structure(p.get_structure(name,'%s_removeotherchain.pdb'%protein_id))
    io.save('%s_official_cleanup.pdb'%protein_id, HydrogenSelect())
    new_official_structure = p.get_structure(name,'%s_official_cleanup.pdb'%protein_id)
    for pp in ppb.build_peptides(new_official_structure):
        residue_valid.append(pp.get_sequence())

print(residue_valid)
for i in residue_valid:
    x.write(str(i))
server_structure = p.get_structure('server_model','%s.pdb'%name)
io.set_structure(server_structure)
global processing_valid_info
processing_valid_info = SiteSelect(residue_valid).selecting_valid_residues(server_structure)
if processing_valid_info is not None:
    io.save('valid_%s.pdb' % name,RecordingSelected())
    processing_valid_info = None
else:
    print('no matched up sequences between official structure and server prediction')
#Cleaningup--Get rid of hydrogen atoms
new_structure = p.get_structure('newmodel','valid_%s.pdb' % name)
io.set_structure(new_structure)
io.save('cleaned_up_%s.pdb'%name, HydrogenSelect())
os.system('mv valid_*.pdb intermediate_files')
os.system('mv *_removeotherchain.pdb intermediate_files')
os.system('mv *_removeothermodel.pdb intermediate_files')

'''pipeline version'''
'''
files = open(sys.argv[1])
for file in files:
    name = file[:-1]
    protein_id = name[:15]
    #get the valid residues presented in the 'official' pdbs publicated
    try:
        official_structure = p.get_structure(name,'%s_official.pdb'%protein_id)
        residue_valid = []#potential breaks in sequences of the published pdb files
        M_notneed = False
        count = 0
        model_count = 0
        for model in official_structure:
            model_count += 1

        if model_count >1:
            M_notneed = True

        if M_notneed:
            io.set_structure(official_structure)
            io.save('%s_removeothermodel.pdb'% protein_id, modelReduce())
            io.set_structure(p.get_structure(name,'%s_removeothermodel.pdb'%protein_id))
            io.save('%s_removeotherchain.pdb'% protein_id, chainReduce())
            io.set_structure(p.get_structure(name,'%s_removeotherchain.pdb'%protein_id))
            io.save('%s_official_cleanup.pdb'%protein_id, HydrogenSelect())
            new_official_structure = p.get_structure(name,'%s_official_cleanup.pdb'%protein_id)
            for pp in ppb.build_peptides(new_official_structure):
                residue_valid.append(pp.get_sequence())
        else:
            io.set_structure(official_structure)
            io.save('%s_removeotherchain.pdb'% protein_id, chainReduce())
            io.set_structure(p.get_structure(name,'%s_removeotherchain.pdb'%protein_id))
            io.save('%s_official_cleanup.pdb'%protein_id, HydrogenSelect())
            new_official_structure = p.get_structure(name,'%s_official_cleanup.pdb'%protein_id)
            for pp in ppb.build_peptides(new_official_structure):
                residue_valid.append(pp.get_sequence())


        #print(residue_valid)


        server_structure = p.get_structure('server_model','%s.pdb'%name)
        io.set_structure(server_structure)
        global processing_valid_info
        processing_valid_info = SiteSelect(residue_valid).selecting_valid_residues(server_structure)
        if processing_valid_info is not None:
            io.save('valid_%s.pdb' % name,RecordingSelected())
            processing_valid_info = None
        else:
            print('no matched up sequences between official structure and server prediction')

        #Cleaningup--Get rid of hydrogen atoms
        new_structure = p.get_structure('newmodel','valid_%s.pdb' % name)
        io.set_structure(new_structure)
        io.save('cleaned_up_%s.pdb'%name, HydrogenSelect())
    except FileNotFoundError:
        print('no matched official_structure for %s'%name)
        continue
os.system('mv valid_*.pdb intermediate_files')
os.system('mv *_removeotherchain.pdb intermediate_files')
os.system('mv *_removeothermodel.pdb intermediate_files')
'''
