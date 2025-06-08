from Bio import SeqIO
import os

# Input files
orthogroups_file = "Orthogroups_Metrosideros_OtherSpecies.tsv"
cds_files = {
    "Metrosideros": "Metrosideros polymorpha var. incanaWRKYCDS.fas",
    "Eucalyptus": "Eucalyptus grandis.WRKYCDS.fas",
    "Syzygium": "Syzygium aromaticum.WRKYCDS.fas",
    "Arabidopsis": "Arabidopsis thaliana.WRKYCDS.fas"
}

# Load CDS sequences from FASTA files into a dictionary
cds_dict = {}
for species, fasta_file in cds_files.items():
    cds_dict[species] = {record.id: record for record in SeqIO.parse(fasta_file, "fasta")}

# Create an output directory
output_dir = "WRKY_Orthogroup_CDS"
os.makedirs(output_dir, exist_ok=True)

# Process the orthogroups file and extract sequences
with open(orthogroups_file, "r") as infile:
    header = infile.readline()  # Skip header if present
    for line in infile:
        parts = line.strip().split("\t")
        ortho_id = parts[0]  # Orthogroup ID
        genes = parts[1:]  # List of genes in the group

        fasta_output = os.path.join(output_dir, f"{ortho_id}.fasta")

        # Write CDS sequences for each orthogroup
        with open(fasta_output, "w") as outfile:
            for gene in genes:
                for species, seq_dict in cds_dict.items():
                    if gene in seq_dict:
                        SeqIO.write(seq_dict[gene], outfile, "fasta")

print(f"CDS extraction complete! Files saved in '{output_dir}'")

