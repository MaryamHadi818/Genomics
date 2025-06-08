#!/bin/bash

# Create a folder to store codeml results
mkdir -p codemlresults

# Loop through all files with the extension .paml
for file in *.paml; do
    base=$(basename "$file" .paml)

    echo "Processing $base..."

    # --- REMOVE IQ-TREE STEPS HERE ---
    # We skip generating trees because we assume you already have them.
    # For example, if your existing tree file is named "$base.tree", adjust as needed.

    # Loop through selection models and create .ctl files
    for model in "M0" "M1a" "M2a" "M7" "M8"; do
        case $model in
            M0)
                NSsites=0
                model_num=0
                ;;
            M1a)
                NSsites=1
                model_num=0
                ;;
            M2a)
                NSsites=2
                model_num=0
                ;;
            M7)
                NSsites=7
                model_num=0
                ;;
            M8)
                NSsites=8
                model_num=0
                ;;
        esac

        # Create the codeml control (.ctl) file
        cat > "${base}_${model}.ctl" << EOF
      seqfile = $base.paml
      treefile = $base_protein.treefile     * <-- Update if your tree file has a different name!
      outfile = codemlresults/${base}_${model}_codeml.out

      noisy = 9
      verbose = 1
      runmode = 0

      seqtype = 1      * 1 = codon sequences
      CodonFreq = 2    * F3x4 model for codon frequencies
      clock = 0
      model = ${model_num}
      NSsites = ${NSsites}
      icode = 0
      fix_kappa = 0
      kappa = 2
      fix_omega = 0
      omega = 1

      cleandata = 1
      method = 0
EOF

        # Run codeml for each model and move the .ctl file into 'codemlresults'
        codeml "${base}_${model}.ctl"
        mv "${base}_${model}.ctl" codemlresults/

        echo "$base $model done."
    done
done
