import os
import subprocess

# Create folders if they don't exist
os.makedirs("alignments", exist_ok=True)
os.makedirs("trees", exist_ok=True)

# Open the log file for recording errors
error_log = open("errors.log", "a")

def run_muscle(input_file, output_file):
    subprocess.run([
        "muscle", "-in", input_file, "-out", output_file, "-clw", "-clwstrict"
    ], check=True)
    print(f"✅ Alignment completed: {output_file}")

def run_iqtree(alignment_file, output_prefix):
    subprocess.run([
        "iqtree2", "-s", alignment_file, "-m", "LG+G", "-bb", "1000", "-nt", "AUTO",
        "-pre", output_prefix
    ], check=True)
    print(f"🌳 IQ-TREE analysis completed: {output_prefix}")

# Process all .fas files in the current directory
for file in os.listdir():
    if file.endswith(".fas"):
        try:
            base_name = file.replace(".fas", "")
            clw_file = os.path.join("alignments", f"{base_name}.clw")
            tree_prefix = os.path.join("trees", base_name)
            tree_file = f"{tree_prefix}.treefile"

            # Skip if alignment exists
            if os.path.exists(clw_file):
                print(f"⚠️ Alignment exists, skipping MUSCLE: {clw_file}")
            else:
                print(f"\n🔄 Running MUSCLE on {file}...")
                run_muscle(file, clw_file)

            # Skip if tree exists
            if os.path.exists(tree_file):
                print(f"⚠️ Tree exists, skipping IQ-TREE: {tree_file}")
            else:
                print(f"🔄 Running IQ-TREE on {clw_file}...")
                run_iqtree(clw_file, tree_prefix)

        except subprocess.CalledProcessError as e:
            error_message = f"❌ Error processing {file}: {e}\n"
            print(error_message)
            error_log.write(error_message)
        except Exception as e:
            error_message = f"⚠️ Unexpected error with {file}: {e}\n"
            print(error_message)
            error_log.write(error_message)

error_log.close()
print("\n🚀 All done! Check 'errors.log' for any issues.")
