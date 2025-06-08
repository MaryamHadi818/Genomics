#!/usr/bin/env python3

import os

# 1) Input orthogroups file
ORTHOGROUPS_FILE = "Orthogroups_Metrosideros_OtherSpecies.tsv"

# 2) Your species CDS FASTA files (for seqkit extraction)
#    Provide the exact filenames of your FASTA files here.
SPECIES_FASTAS = [
    "Arabidopsis thaliana.WRKYCDS.fas",
    "Eucalyptus grandis.WRKYCDS.fas",
    "Metrosideros polymorpha var. incanaWRKYCDS.fas",
    "Syzygium aromaticum.WRKYCDS.fas"
]

# 3) Output directory for:
#    - A small text file listing gene IDs for each orthogroup
#    - A shell script to extract those genes from each FASTA
OUTPUT_DIR = "per_orthogroup_scripts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def safe_filename(name):
    """Turn an orthogroup ID into a safe filename (optional)."""
    return name.replace(":", "_").replace("/", "_")

with open(ORTHOGROUPS_FILE, "r") as infile:
    header = infile.readline().strip()  # If there's a header line, we skip it here
    for line in infile:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        parts = line.split("\t")
        og_id = parts[0]  # e.g. "OG0000000"
        og_id_safe = safe_filename(og_id)

        # Collect gene IDs from the remaining columns
        all_genes = []
        for col in parts[1:]:
            # Each column can have multiple IDs separated by commas
            genes_in_col = [g.strip() for g in col.split(",") if g.strip()]
            all_genes.extend(genes_in_col)

        # 1) Create a text file listing the gene IDs for this orthogroup
        gene_list_file = os.path.join(OUTPUT_DIR, f"{og_id_safe}_genes.txt")
        with open(gene_list_file, "w") as gf:
            for g in all_genes:
                gf.write(g + "\n")

        # 2) Create a shell script that extracts these IDs from each FASTA
        script_file = os.path.join(OUTPUT_DIR, f"extract_{og_id_safe}.sh")
        with open(script_file, "w") as sf:
            sf.write("#!/bin/bash\n\n")
            sf.write(f"echo 'Extracting CDS for {og_id}...'\n\n")
            # You can choose to either (A) create one combined file or (B) separate per species
            # (A) Single combined FASTA file:
            combined_out = f"{og_id_safe}_CDS.fas"
            sf.write(f"> {combined_out}\n")  # empty/overwrite combined file

            for fasta in SPECIES_FASTAS:
                # Append matches to the combined file
                sf.write(
                    f"seqkit grep -f {gene_list_file} \"{fasta}\" >> {combined_out}\n"
                )

            sf.write("\n")
            sf.write(f"echo 'Done extracting {og_id}.'\n")

        # Make the script executable (optional, if on Unix-like system)
        os.chmod(script_file, 0o755)

print("All orthogroups have been split! Check the per_orthogroup_scripts/ directory.")

