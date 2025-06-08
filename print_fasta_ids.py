from Bio import SeqIO

fasta_file = "Eucalyptus grandis.WRKYCDS.fas"
for record in SeqIO.parse(fasta_file, "fasta"):
    print(f"ID: '{record.id}' | Description: '{record.description}'")

