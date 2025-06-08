import os
import subprocess
import glob

PAL2NAL_PATH = "/mnt/c/Users/Maryam/Downloads/WRKY-orthofinder/fastafiles/pal2nal/pal2nal.v14/pal2nal.pl"

protein_files = glob.glob("OG*_protein.clw")

for protein_file in protein_files:
    base_name = protein_file.replace("_protein.clw", "")
    cds_file = f"{base_name}_CDS.fas"
    
    if os.path.exists(cds_file):
        output_file = f"{base_name}.paml"
        
        cmd = f"perl {PAL2NAL_PATH} {protein_file} {cds_file} -output paml"
        
        with open(output_file, "w") as out_f:
            subprocess.run(cmd, shell=True, check=True, stdout=out_f)
        
        print(f"✅ PHYLIP/PAML file created: {output_file}")
    else:
        print(f"❌ Missing CDS file: {cds_file}")
