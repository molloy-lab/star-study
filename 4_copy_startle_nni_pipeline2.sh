#!/bin/bash

export PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/star-study/"

# Pipeline 2 startle_nni*
PDD="prune-deprune-deduplicate-bio-result"
OUT="$PROJDIR/bio-result/$PDD/startle_nni"


DATA="3515_Lkb1_T1_Fam"

# Pipeline 2a
IN="$PROJDIR/H_bio_result_Full/startle_nni"
cp $IN/$DATA/one_sol_branch_branch_trees.nwk $OUT/$DATA/one_sol_branch_trees.nwk


cp $IN/$DATA/one_sol_sh_branch_branch_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk
cp $IN/$DATA/nj_usage.log $OUT/$DATA/
cp $IN/$DATA/nni_usage.log $OUT/$DATA/

# Pipeline 2b
IN="$PROJDIR/H_bio_result_Full/startle_nni"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_ckpt.txt $OUT/$DATA/
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/

DATA="3513_NT_T1_Fam"

# Pipeline 2a
IN="$PROJDIR/G_bio_result_pruned_deduplicate/startle_nni"

cp $IN/$DATA/one_sol_branch_trees.nwk   $OUT/$DATA/one_sol_branch_trees.nwk 

cp $IN/$DATA/one_sol_branch_sh_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk

cp $PROJDIR/E_bio_result_pruned/startle_nni/$DATA/nj_usage.log $OUT/$DATA/nj_usage.log
cp $PROJDIR/E_bio_result_pruned/startle_nni/$DATA/nni_usage.log $OUT/$DATA/nni_usage.log


# Pipeline 2b
IN="$PROJDIR/H_bio_result_Full/startle_nni"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_trees.nwk  $OUT/$DATA/
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/


DATA="3724_NT_All"

# Pipeline 2a
IN="$PROJDIR/G_bio_result_pruned_deduplicate/startle_nni"

cp $IN/$DATA/one_sol_branch_trees.nwk  $OUT/$DATA/one_sol_branch_trees.nwk


cp $IN/$DATA/one_sol_branch_sh_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk

cp $PROJDIR/E_bio_result_pruned/startle_nni/$DATA/nj_usage.log $OUT/$DATA/nj_usage.log
cp $PROJDIR/E_bio_result_pruned/startle_nni/$DATA/nni_usage.log $OUT/$DATA/nni_usage.log

# Pipeline 2b
IN="$PROJDIR/H_bio_result_Full/startle_nni"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_trees.nwk  $OUT/$DATA/
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/


##### PIPELINE 2c

DATA="3513_NT_T1_Fam"
IN="G_bio_result_pruned_deduplicate/laml/startle_nni"

OUT="bio-result/$PDD/laml/$DATA/startle_nni"
cp $IN/$DATA/laml_output_trees.nwk $OUT/one_sol_branch_trees.nwk 
cp $IN/$DATA/laml_output_usage.log $OUT/one_sol_usage.log


DATA="3724_NT_All"

IN="G_bio_result_pruned_deduplicate/laml/startle_nni"

OUT="bio-result/$PDD/laml/$DATA/startle_nni"
cp $IN/$DATA/laml_output_ckpt.txt $OUT/one_sol_ckpt.txt


DATA="3515_Lkb1_T1_Fam"

IN="H_bio_result_Full/laml/startle_nni/$DATA"
OUT="bio-result/$PDD/laml/$DATA/startle_nni/"
cp $IN/one_sol_trees.nwk $OUT/one_sol_branch_trees.nwk
cp $IN/laml_output_usage.log $OUT/one_sol_usage.log


