#!/bin/bash

export PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/star-study/"
# Pipeline 1 Cassiopeia-Hybrid
OUT="$PROJDIR/bio-result/deduplicate-bio-result/cassiopeia_hybrid"

DATA="3513_NT_T1_Fam"

IN="$PROJDIR/F_bio_result_deduplicate/cassiopeia_hybrid"

# Pipeline 1a

DATA="3513_NT_T1_Fam"
cp $IN/$DATA/one_sol_branch_trees.nwk $OUT/$DATA/one_sol_branch_trees.nwk
DATA="3724_NT_All"
cp $IN/$DATA/one_sol_branch_trees.nwk $OUT/$DATA/one_sol_branch_trees.nwk

DATA="3515_Lkb1_T1_Fam"

IN="$PROJDIR/I_bio_result_Full_deduplicate/cassiopeia_hybrid/$DATA"
cp $IN/deduplicate_tree.nwk $OUT/$DATA/one_sol_trees.nwk