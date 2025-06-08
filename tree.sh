#!/bin/bash

# Load IQ-TREE if necessary (uncomment if using an HPC)
# module load iqtree/2.1.4

# Loop through all .paml files
for aln in *.paml; do
    prefix=$(basename "$aln" .paml)
    echo "Building tree for $aln..."

    iqtree -s "$aln" \
           -m GTR+G \
           -nt AUTO \
           -pre "$prefix" \
           -keep-ident \
           -redo
done

