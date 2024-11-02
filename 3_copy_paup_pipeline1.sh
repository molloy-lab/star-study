#!/bin/bash

export PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/star-study/"

# Pipeline 1 PAUP*
OUT="$PROJDIR/bio-result/deduplicate-bio-result/paup"


DATA="3515_Lkb1_T1_Fam"

# Pipeline 1a
IN="$PROJDIR/I_bio_result_Full_deduplicate/paup"
cp $IN/$DATA/one_sol_branch_trees.nwk $OUT/$DATA/
cp $IN/$DATA/sc_branch_trees.nwk $OUT/$DATA/

cp $IN/$DATA/one_sol_sh_branch_trees.nwk $OUT/$DATA/
cp $IN/$DATA/sc_sh_branch_trees.nwk $OUT/$DATA/
cp $IN/$DATA/paup_usage.log $OUT/$DATA/

# Pipeline 1b
IN="$PROJDIR/I_bio_result_Full_deduplicate/paup"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_ckpt.txt $OUT/$DATA/
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/

cp $IN/$DATA/sc_sh_branch_resolve_poly_ckpt.txt $OUT/$DATA/
cp $IN/$DATA/sc_sh_branch_resolve_poly_usage.log $OUT/$DATA/

DATA="3513_NT_T1_Fam"

# Pipeline 1a
IN="$PROJDIR/F_bio_result_deduplicate/paup"

cp $IN/$DATA/one_sol_branch_trees.nwk   $OUT/$DATA/one_sol_branch_trees.nwk 
cp $IN/$DATA/sc_branch_trees.nwk $OUT/$DATA/sc_branch_trees.nwk

cp $IN/$DATA/one_sol_sh_branch_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk
cp $IN/$DATA/sc_sh.tre $OUT/$DATA/sc_sh_trees.nwk

cp $IN/$DATA/paup_usage.log $OUT/$DATA/paup_usage.log

# Pipeline 1b
IN="$PROJDIR/I_bio_result_Full_deduplicate/paup"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_trees.nwk  $OUT/$DATA/
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/

cp $IN/$DATA/sc_sh_branch_resolve_poly_trees.nwk $OUT/$DATA/
cp $IN/$DATA/sc_sh_branch_resolve_poly_usage.log $OUT/$DATA/


DATA="3724_NT_All"

# Pipeline 1a
IN="$PROJDIR/F_bio_result_deduplicate/paup"

cp $IN/$DATA/one_sol_branch_trees.nwk  $OUT/$DATA/one_sol_branch_trees.nwk
cp $IN/$DATA/sc_branch_trees.nwk  $OUT/$DATA/sc_branch_trees.nwk


cp $IN/$DATA/one_sol_sh_branch_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk
cp $IN/$DATA/sc_sh.tre $OUT/$DATA/sc_sh.tre

cp $IN/$DATA/paup_usage.log $OUT/$DATA/paup_usage.log

# Pipeline 1b
IN="$PROJDIR/I_bio_result_Full_deduplicate/paup"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_trees.nwk  $OUT/$DATA/
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/

cp $IN/$DATA/sc_sh_branch_resolve_poly_trees.nwk $OUT/$DATA/
cp $IN/$DATA/sc_sh_branch_resolve_poly_usage.log $OUT/$DATA/


##### PIPELINE 1c

DATA="3513_NT_T1_Fam"
IN="F_bio_result_deduplicate/laml/$DATA/"

OUT="bio-result/deduplicate-bio-result/laml/$DATA/paup_one_sol"
cp $IN/laml_output-paup-one_sol_trees.nwk $OUT/one_sol_branch_trees.nwk 
cp $IN/laml-paup-one_sol_usage.log $OUT/one_sol_usage.log

OUT="bio-result/deduplicate-bio-result/laml/$DATA/paup_sc"
cp $IN/laml_output-paup-sc_trees.nwk $OUT/one_sol_branch_trees.nwk 
cp $IN/laml-paup-sc_usage.log $OUT/one_sol_usage.log


DATA="3724_NT_All"

IN="F_bio_result_deduplicate/laml/$DATA/"

OUT="bio-result/deduplicate-bio-result/laml/$DATA/paup_one_sol"
cp $IN/laml_output-paup-one_sol_trees.nwk $OUT/one_sol_branch_trees.nwk 
cp $IN/laml-paup-one_sol_usage.log $OUT/one_sol_usage.log


OUT="bio-result/deduplicate-bio-result/laml/$DATA/paup_sc"
cp $IN/laml_output-paup-sc_ckpt.txt $OUT/one_sol_ckpt.txt
cp $IN/paup_sc_24hrs_branch_trees.nwk $OUT/one_sol_branch_trees.nwk

DATA="3515_Lkb1_T1_Fam"

IN="I_bio_result_Full_deduplicate/laml/paup_one_sol/$DATA/one_sol_ckpt.txt"
OUT="bio-result/deduplicate-bio-result/laml/$DATA/paup_one_sol"
cp $IN $OUT


IN="I_bio_result_Full_deduplicate/laml/paup_sc/$DATA/one_sol_ckpt.txt"
OUT="bio-result/deduplicate-bio-result/laml/$DATA/paup_sc"
cp $IN $OUT

