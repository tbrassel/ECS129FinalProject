# clean ups
code runs with python 3.7

**important package to be installed** [biopython 1.73](https://biopython.org/wiki/Download)<br/>
<br/>
**For official pdb clean up**: <br/>
If there're multiple models for the protein, only keep the first model;<br/>
If there're multiple chains, only keep chain A;<br/>
If there're HETATM ATOMS, ignore.<br/>
Delete hydrogen atoms.<br/> 
<br/>
**For predicted file clean up**: <br/>
Pick out sequences that matches the exact order and amino acids from cleaned_up_official pdbs (only one model and chain A).<br/>
Delete hydrogen atoms.<br/> 

To run cleanup.py, move into this directory, if it's a single file that needs clean up, use command<br/>
```python cleanup.py```<br/>
To run all the file in files.txt (containing both official and predicted pdb names):<br/>
```python cleanup.py files.txt```

Special official pdbs that didn't have the same protein sequence with the sequence we sent for server prediction needs manual input, 
considering the sample size is not large (special adjustment will be listed below). The differ in sequence may due to different isoforms.

**The input files must be in the same directory as the python code**<br/>
 (All inputs are already put in the same directory)<br/>
**The output files are stored in version3.zip**<br/>
**The offical pdbs are stored in official folder**<br/>
**ENSG00000115263 needs some manual adjustment to enable all 3 official pdbs to be run**

## Special adjustments 
**(needs to be run in single file command with manual adjustment)**<br/>
**where to change is annotated in cleanup.py**
 
### ENSG00000092009
used pdb id 3N7O
official:
>3N7O:A|PDBID|CHAIN|SEQUENCE
IIGGTECKPHSRPYMAYLEIVTSNGPSKFCGGFLIRRNFVLTAAHCAGRSITVTLGAHNITEEEDTWQKLEVIKQFRHPK
YNTSTLHHDIMLLKLKEKASLTLAVGTLPFPSQFNFVPPGRMCRVAGWGRTGVLKPGSDTLQEVKLRLMDPQACSHFRDF
DHNLQLCVGNPRKTKSAFKGDSGGPLLCAG```A```AQGIVSYGRSDAKPPAVFTRISHY```Q```PWINQILQAN

>3N7O modified to allow predicted pdbs can have at least same number of residues as official pdbs
IIGGTECKPHSRPYMAYLEIVTSNGPSKFCGGFLIRRNFVLTAAHCAGRSITVTLGAHNITEEEDTWQKLEVIKQFRHPK
YNTSTLHHDIMLLKLKEKASLTLAVGTLPFPSQFNFVPPGRMCRVAGWGRTGVLKPGSDTLQEVKLRLMDPQACSHFRDF
DHNLQLCVGNPRKTKSAFKGDSGGPLLCAG```V```AQGIVSYGRSDAKPPAVFTRISHY```R```PWINQILQAN

### ENSG00000144891:
all 4 published model used a different isoform than ours, so didn't collect data for this protein

### ENSG00000115263:
Manually modify the official pdb input for this protein within the code
by moving the corresponding pdb outside out the official folder<br/>
Actually there're 3 pieces,<br/> 
Piece C have perfect match. Site 146-178 2l63 NMR<br/>
Piece B have perfect match: Site 98-127 1D0R NMR<br/>
Piece A not perfect match: Site 53-81 1BH0 X-RAY<br/>
official:
>1BH0:A|PDBID|CHAIN|SEQUENCE<br/>
HSQGTFTSDYSKYLDS```KK```AQ```E```FVQWLMNT<br/>
>Sequence I used:<br/>
HSQGTFTSDYSKYLDS```RR```AQ```D```FVQWLMNT
