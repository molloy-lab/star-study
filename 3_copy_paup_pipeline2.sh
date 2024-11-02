#!/bin/bash

export PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/star-study/"

# Pipeline 2 PAUP*
PDD="prune-deprune-deduplicate-bio-result"
OUT="$PROJDIR/bio-result/$PDD/paup"


DATA="3515_Lkb1_T1_Fam"

# Pipeline 2a
IN="$PROJDIR/H_bio_result_Full/paup"
cp $IN/$DATA/one_sol_branch_trees.nwk $OUT/$DATA/
cp $IN/$DATA/sc_branch_trees.nwk $OUT/$DATA/

cp $IN/$DATA/one_sol_sh_branch_trees.nwk $OUT/$DATA/
cp $IN/$DATA/sc_sh_branch_trees.nwk $OUT/$DATA/
cp $IN/$DATA/paup_usage.log $OUT/$DATA/

# Pipeline 2b
IN="$PROJDIR/H_bio_result_Full/paup"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_ckpt.txt $OUT/$DATA/
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/

cp $IN/$DATA/sc_sh_branch_resolve_poly_ckpt.txt $OUT/$DATA/
cp $IN/$DATA/sc_sh_branch_resolve_poly_usage.log $OUT/$DATA/

DATA="3513_NT_T1_Fam"

# Pipeline 2a
IN="$PROJDIR/G_bio_result_pruned_deduplicate/paup"

cp $IN/$DATA/one_sol_branch_trees.nwk   $OUT/$DATA/one_sol_branch_trees.nwk 
cp $IN/$DATA/sc_branch_trees.nwk $OUT/$DATA/sc_branch_trees.nwk

cp $IN/$DATA/one_sol_branch_sh_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk
cp $IN/$DATA/sc_branch_sh_trees.nwk $OUT/$DATA/sc_sh_branch_trees.nwk

cp $PROJDIR/E_bio_result_pruned/paup/$DATA/paup_usage.log $OUT/$DATA/paup_usage.log

# Pipeline 2b
IN="$PROJDIR/H_bio_result_Full/paup"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_trees.nwk  $OUT/$DATA/
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/

cp $IN/$DATA/sc_sh_branch_resolve_poly_trees.nwk $OUT/$DATA/
cp $IN/$DATA/sc_sh_branch_resolve_poly_usage.log $OUT/$DATA/


DATA="3724_NT_All"

# Pipeline 2a
IN="$PROJDIR/G_bio_result_pruned_deduplicate/paup"

cp $IN/$DATA/one_sol_branch_trees.nwk  $OUT/$DATA/one_sol_branch_trees.nwk
cp $IN/$DATA/sc_branch_trees.nwk  $OUT/$DATA/sc_branch_trees.nwk


cp $IN/$DATA/one_sol_branch_sh_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk
cp $IN/$DATA/sc_branch_sh_trees.nwk $OUT/$DATA/sc_sh_branch_trees.nwk

cp $PROJDIR/E_bio_result_pruned/paup/$DATA/paup_usage.log $OUT/$DATA/paup_usage.log

# Pipeline 2b
IN="$PROJDIR/H_bio_result_Full/paup"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_trees.nwk  $OUT/$DATA/
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/

cp $IN/$DATA/sc_sh_branch_resolve_poly_trees.nwk $OUT/$DATA/
cp $IN/$DATA/sc_sh_branch_resolve_poly_usage.log $OUT/$DATA/


##### PIPELINE 2c

DATA="3513_NT_T1_Fam"
IN="G_bio_result_pruned_deduplicate/laml/"

OUT="bio-result/$PDD/laml/$DATA/paup_one_sol"
cp $IN/paup_one_sol/$DATA/laml_output_trees.nwk $OUT/one_sol_branch_trees.nwk 
cp $IN/paup_one_sol/$DATA/laml_output_usage.log $OUT/one_sol_usage.log

OUT="bio-result/$PDD/laml/$DATA/paup_sc"
cp $IN/paup_sc/$DATA/laml_output_trees.nwk $OUT/one_sol_branch_trees.nwk 
cp $IN/paup_sc/$DATA/laml_output_usage.log $OUT/one_sol_usage.log


DATA="3724_NT_All"

IN="G_bio_result_pruned_deduplicate/laml/"

OUT="bio-result/$PDD/laml/$DATA/paup_one_sol"
cp $IN/paup_one_sol/$DATA/laml_output_trees.nwk $OUT/one_sol_branch_trees.nwk 
cp $IN/paup_one_sol/$DATA/laml_output_usage.log $OUT/one_sol_usage.log


OUT="bio-result/$PDD/laml/$DATA/paup_sc"
cp $IN/paup_sc/$DATA/laml_output_ckpt.txt $OUT/one_sol_ckpt.txt
cp $IN/paup_sc/$DATA/24hrs-best_branch_trees.nwk $OUT/one_sol_branch_trees.nwk

DATA="3515_Lkb1_T1_Fam"

IN="H_bio_result_Full/laml/paup_one_sol/$DATA/one_sol_trees.nwk"
OUT="bio-result/$PDD/laml/$DATA/paup_one_sol/one_sol_branch_trees.nwk"
cp $IN $OUT

IN="H_bio_result_Full/laml/paup_one_sol/$DATA/laml_output_usage.log"
OUT="bio-result/$PDD/laml/$DATA/paup_one_sol/one_sol_usage.log"
cp $IN $OUT


IN="H_bio_result_Full/laml/paup_sc/$DATA/one_sol_ckpt.txt"
OUT="bio-result/$PDD/laml/$DATA/paup_sc"
cp $IN $OUT

