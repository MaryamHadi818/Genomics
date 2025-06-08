import glob

def remove_first_line(file_path):
    """Remove the first line from a Clustal file."""
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    # Remove the first line (index 0) from the list of lines
    lines = lines[1:]
    
    # Write the modified lines back to the file
    with open(file_path, "w") as f:
        f.writelines(lines)

# Apply the function to all Clustal files ending with '_protein.clw'
clustal_files = glob.glob("*_protein.clw")  # Matches all files ending with '_protein.clw' in the current directory

for clustal_file in clustal_files:
    remove_first_line(clustal_file)
    print(f"✅ Removed first line from: {clustal_file}")
