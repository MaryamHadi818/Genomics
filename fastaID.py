from Bio import SeqIO

# List of your four CDS FASTA files
cds_files = [
    "Arabidopsis thaliana.WRKYCDS.fas",
    "Eucalyptus grandis.WRKYCDS.fas",
    "Metrosideros polymorpha var. incanaWRKYCDS.fas",
    "Syzygium aromaticum.WRKYCDS.fas"
]

# Dictionary to store all sequences with full header as ID
all_cds_dict = {}

for fasta_file in cds_files:
    for record in SeqIO.parse(fasta_file, "fasta"):
        # Override the default behavior: use the full description as the ID
        record.id = record.description.strip()
        all_cds_dict[record.id] = record

# For testing, print out the keys to verify full headers are used as IDs
for key in all_cds_dict:
    print(key)

