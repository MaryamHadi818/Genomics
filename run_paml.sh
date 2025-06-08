#!/bin/bash

# Load required modules (uncomment if needed)
# module load iqtree
# module load paml

for file in *.paml; do
    base=$(basename "$file" .paml)

    echo "Processing $base..."

    # Step 1: Generate an unrooted tree from alignment (replace .phy if needed)
    iqtree -s "$base.paml" -nt AUTO -m GTR+G -pre "$base"

    # Step 2: Create control (.ctl) file for codeml
    cat > "$base.ctl" << EOF
      seqfile = $base.paml
      treefile = $base.treefile
      outfile = ${base}_codeml.out

      noisy = 9
      verbose = 1
      runmode = 0

      seqtype = 1
      CodonFreq = 2
      clock = 0
      model = 0
      NSsites = 0
      icode = 0
      fix_kappa = 0
      kappa = 2
      fix_omega = 0
      omega = 1

      cleandata = 1
EOF

    # Step 3: Run codeml
    codeml "$base.ctl"

    echo "$base done."
done

