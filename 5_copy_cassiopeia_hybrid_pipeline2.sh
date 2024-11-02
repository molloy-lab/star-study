#!/bin/bash

export PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/star-study/"
# Pipeline 2 Cassiopeia-Hybrid
PDD="prune-deprune-deduplicate-bio-result"
OUT="$PROJDIR/bio-result/$PDD/cassiopeia_hybrid"

DATA="3513_NT_T1_Fam"

IN="$PROJDIR/G_bio_result_pruned_deduplicate/cassiopeia_hybrid"

# Pipeline 2a

DATA="3513_NT_T1_Fam"
cp $IN/$DATA/one_sol_branch_trees.nwk $OUT/$DATA/one_sol_branch_trees.nwk
DATA="3724_NT_All"
cp $IN/$DATA/one_sol_branch_trees.nwk $OUT/$DATA/one_sol_branch_trees.nwk


DATA="3515_Lkb1_T1_Fam"

IN="$PROJDIR/H_bio_result_Full/cassiopeia_hybrid/$DATA"
cp $IN/deduplicate_tree.nwk $OUT/$DATA/one_sol_trees.nwk
