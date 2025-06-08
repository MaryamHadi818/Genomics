import os

# Codeml parameters template
ctl_template = """
      seqfile = {seqfile}
     treefile = {treefile}
      outfile = {outfile}

        noisy = 9
      verbose = 1
      runmode = 0

      seqtype = 1
    CodonFreq = 2

        clock = 0
       aaDist = 0
   model = 0
   NSsites = 0

    icode = 0
    fix_kappa = 0
        kappa = 2
    fix_omega = 0
        omega = 1

    cleandata = 1
"""

# Get list of all .paml files in the current directory
paml_files = [f for f in os.listdir() if f.endswith('.paml')]

for paml_file in paml_files:
    base_name = paml_file.replace('.paml', '')
    
    seqfile = f"{base_name}.paml"
    treefile = f"{base_name}_protein.treefile"
    outfile = f"{base_name}_codeml.out"
    ctl_filename = f"{base_name}.ctl"

    # Fill in the template
    ctl_content = ctl_template.format(
        seqfile=seqfile,
        treefile=treefile,
        outfile=outfile
    )

    # Write the ctl file
    with open(ctl_filename, 'w') as ctl_file:
        ctl_file.write(ctl_content)

    print(f"Generated {ctl_filename}")

