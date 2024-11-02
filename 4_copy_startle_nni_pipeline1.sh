#!/bin/bash

export PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/star-study/"

# Pipeline 1 Startle-NNI
OUT="$PROJDIR/bio-result/deduplicate-bio-result/startle_nni"


DATA="3515_Lkb1_T1_Fam"

# Pipeline 1a
IN="$PROJDIR/I_bio_result_Full_deduplicate/startle_nni"
cp $IN/$DATA/one_sol_branch_branch_trees.nwk $OUT/$DATA/one_sol_branch_trees.nwk


cp $IN/$DATA/one_sol_sh_branch_branch_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk

cp $IN/$DATA/nj_usage.log $OUT/$DATA/
cp $IN/$DATA/nni_usage.log $OUT/$DATA/

# Pipeline 1b
IN="$PROJDIR/I_bio_result_Full_deduplicate/startle_nni"
cp $IN/$DATA/one_sol_sh_branch_branch_resolve_poly_trees.nwk $OUT/$DATA/one_sol_sh_branch_resolve_poly_trees.nwk
cp $IN/$DATA/one_sol_sh_branch_branch_resolve_poly_usage.log $OUT/$DATA/one_sol_sh_branch_resolve_poly_usage.log


DATA="3513_NT_T1_Fam"

# Pipeline 1a
IN="$PROJDIR/F_bio_result_deduplicate/startle_nni"
cp $IN/$DATA/laml-branch_trees.nwk  $OUT/$DATA/one_sol_branch_trees.nwk

cp $IN/$DATA/one_sol_sh_branch_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk

cp $IN/$DATA/nj_usage.log $OUT/$DATA/
cp $IN/$DATA/nni_usage.log $OUT/$DATA/

# Pipeline 1b
IN="$PROJDIR/I_bio_result_Full_deduplicate/startle_nni"
cp $IN/$DATA/one_sol_sh_branch_branch_resolve_poly_trees.nwk  $OUT/$DATA/one_sol_sh_branch_resolve_poly_trees.nwk
cp $IN/$DATA/one_sol_sh_branch_branch_resolve_poly_usage.log $OUT/$DATA/one_sol_sh_branch_resolve_poly_usage.log


DATA="3724_NT_All"

# Pipeline 1a
IN="$PROJDIR/F_bio_result_deduplicate/startle_nni"
cp $IN/$DATA/laml-branch_trees.nwk  $OUT/$DATA/one_sol_branch_trees.nwk
cp $IN/$DATA/one_sol_sh_branch_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk

cp $IN/$DATA/nj_usage.log $OUT/$DATA/
cp $IN/$DATA/nni_usage.log $OUT/$DATA/

# Pipeline 1b
IN="$PROJDIR/I_bio_result_Full_deduplicate/startle_nni"
cp $IN/$DATA/one_sol_sh_branch_branch_resolve_poly_trees.nwk  $OUT/$DATA/one_sol_sh_branch_resolve_poly_trees.nwk
cp $IN/$DATA/one_sol_sh_branch_branch_resolve_poly_usage.log $OUT/$DATA/one_sol_sh_branch_resolve_poly_usage.log


##### PIPELINE 1c

DATA="3513_NT_T1_Fam"
IN="F_bio_result_deduplicate/laml/$DATA/"

OUT="bio-result/deduplicate-bio-result/laml/$DATA/startle_nni"
cp $IN/laml_output-1_trees.nwk $OUT/one_sol_branch_trees.nwk 
cp $IN/laml_usage-1.log $OUT/one_sol_usage.log



DATA="3724_NT_All"

IN="F_bio_result_deduplicate/laml/$DATA/"

OUT="bio-result/deduplicate-bio-result/laml/$DATA/startle_nni"
cp $IN/laml_output-1_trees.nwk $OUT/one_sol_branch_trees.nwk 
cp $IN/laml_usage-1.log $OUT/one_sol_usage.log


DATA="3515_Lkb1_T1_Fam"

IN="I_bio_result_Full_deduplicate/laml/startle_nni/$DATA/one_sol_ckpt.txt"
OUT="bio-result/deduplicate-bio-result/laml/$DATA/startle_nni"
cp $IN $OUT


