#!/bin/bash

export PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/star-study/"

# Pipeline 2 Star-CDP
OUT="$PROJDIR/bio-result/prune-deprune-deduplicate-bio-result/star_cdp"
PDD="prune-deprune-deduplicate-bio-result"
DATA="3515_Lkb1_T1_Fam"

# Pipeline 2a
IN="$PROJDIR/H_bio_result_Full/star_cdp"

cp $IN/$DATA/one_sol_branch_trees.nwk $OUT/$DATA/one_sol_branch_trees.nwk
cp $IN/$DATA/rand_sol_branch_trees.nwk $OUT/$DATA/rand_sol_branch_trees.nwk
cp $IN/$DATA/sc_branch_trees.nwk $OUT/$DATA/sc_branch_trees.nwk

cp $IN/$DATA/one_sol_sh_branch_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk
cp $IN/$DATA/rand_sol_branch_trees.nwk $OUT/$DATA/rand_sol_branch_trees.nwk
cp $IN/$DATA/sc_sh_branch_trees.nwk $OUT/$DATA/sc_sh_branch_trees.nwk
cp $IN/$DATA/star_cdp_usage.log $OUT/$DATA/

# Pipeline 2b
IN="$PROJDIR/H_bio_result_Full/star_cdp"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_ckpt.txt $OUT/$DATA/

cp $IN/$DATA/rand_sol_sh_branch_resolve_poly_ckpt.txt $OUT/$DATA/

cp $IN/$DATA/sc_sh_branch_resolve_poly_ckpt.txt $OUT/$DATA/

DATA="3513_NT_T1_Fam"

# Pipeline 2a
IN="$PROJDIR/G_bio_result_pruned_deduplicate/star_cdp"

cp $IN/$DATA/one_sol_branch_trees.nwk $OUT/$DATA/
cp $IN/$DATA/rand_sol_branch_trees.nwk $OUT/$DATA
cp $IN/$DATA/sc_branch_trees.nwk $OUT/$DATA/

cp $IN/$DATA/one_sol_branch_sh_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk
cp $IN/$DATA/rand_sol_branch_sh_trees.nwk $OUT/$DATA/rand_sol_sh_branch_trees.nwk
cp $IN/$DATA/sc_branch_sh_trees.nwk $OUT/$DATA/sc_sh_branch_trees.nwk

cp $PROJDIR/E_bio_result_pruned/star_cdp/$DATA/consensus_star_cdp_usage.log $OUT/$DATA/star_cdp_usage.log

# Pipeline 2b
IN="$PROJDIR/H_bio_result_Full/star_cdp"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_trees.nwk $OUT/$DATA/
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/


cp $IN/$DATA/rand_sol_sh_branch_resolve_poly_trees.nwk $OUT/$DATA/
cp $IN/$DATA/rand_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/

cp $IN/$DATA/sc_sh_branch_resolve_poly_trees.nwk $OUT/$DATA/
cp $IN/$DATA/sc_sh_branch_resolve_poly_usage.log $OUT/$DATA/


DATA="3724_NT_All"

# Pipeline 2a
IN="$PROJDIR/G_bio_result_pruned_deduplicate/star_cdp"

cp $IN/$DATA/one_sol_branch_trees.nwk $OUT/$DATA/
cp $IN/$DATA/rand_sol_branch_trees.nwk $OUT/$DATA
cp $IN/$DATA/sc_branch_trees.nwk $OUT/$DATA/

cp $IN/$DATA/one_sol_branch_sh_trees.nwk $OUT/$DATA/one_sol_sh_branch_trees.nwk
cp $IN/$DATA/rand_sol_branch_sh_trees.nwk $OUT/$DATA/rand_sol_sh_branch_trees.nwk
cp $IN/$DATA/sc_branch_sh_trees.nwk $OUT/$DATA/sc_sh_branch_trees.nwk

cp $PROJDIR/E_bio_result_pruned/star_cdp/$DATA/consensus_star_cdp_usage.log $OUT/$DATA/star_cdp_usage.log

# Pipeline 2b
IN="$PROJDIR/H_bio_result_Full/star_cdp"
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_trees.nwk $OUT/$DATA/
cp $IN/$DATA/one_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/

cp $IN/$DATA/rand_sol_sh_branch_resolve_poly_trees.nwk $OUT/$DATA/
cp $IN/$DATA/rand_sol_sh_branch_resolve_poly_usage.log $OUT/$DATA/

cp $IN/$DATA/sc_sh_branch_resolve_poly_trees.nwk $OUT/$DATA/
cp $IN/$DATA/sc_sh_branch_resolve_poly_usage.log $OUT/$DATA/



##### PIPELINE 2c

DATA="3513_NT_T1_Fam"
IN="G_bio_result_pruned_deduplicate/laml/star_cdp_one_sol/$DATA"
OUT="bio-result/$PDD/laml/$DATA/star_cdp_one_sol"

cp $IN/laml_output_trees.nwk $OUT/one_sol_branch_trees.nwk
cp $IN/laml_output_usage.log $OUT/one_sol_usage.log

IN="G_bio_result_pruned_deduplicate/laml/star_cdp_rand_sol/$DATA"
OUT="bio-result/$PDD/laml/$DATA/star_cdp_rand_sol"

cp $IN/laml_output_trees.nwk $OUT/one_sol_branch_trees.nwk
cp $IN/laml_output_usage.log $OUT/one_sol_usage.log

IN="G_bio_result_pruned_deduplicate/laml/star_cdp_sc/$DATA"
OUT="bio-result/$PDD/laml/$DATA/star_cdp_sc"

cp $IN/laml_output_trees.nwk $OUT/one_sol_branch_trees.nwk 
cp $IN/laml_output_usage.log $OUT/one_sol_usage.log

#####################

DATA="3724_NT_All"
IN="G_bio_result_pruned_deduplicate/laml/star_cdp_one_sol/$DATA"
OUT="bio-result/$PDD/laml/$DATA/star_cdp_one_sol"

cp $IN/laml_output_trees.nwk $OUT/one_sol_branch_trees.nwk
cp $IN/laml_output_usage.log $OUT/one_sol_usage.log

IN="G_bio_result_pruned_deduplicate/laml/star_cdp_rand_sol/$DATA"
OUT="bio-result/$PDD/laml/$DATA/star_cdp_rand_sol"

cp $IN/laml_output-24hrs_trees.nwk $OUT/one_sol_branch_trees.nwk 
cp $IN/laml_output-24hrs_usage.log $OUT/one_sol_usage.log

IN="G_bio_result_pruned_deduplicate/laml/star_cdp_sc/$DATA"
OUT="bio-result/$PDD/laml/$DATA/star_cdp_sc"

cp $IN/laml_output-24hrs_ckpt.txt $OUT/one_sol_ckpt.txt
cp $IN/24hrs-best_branch_trees.nwk $OUT/one_sol_branch_trees.nwk

#################

DATA="3515_Lkb1_T1_Fam"
IN="H_bio_result_Full/laml/star_cdp_one_sol/$DATA"
OUT="bio-result/$PDD/laml/$DATA/star_cdp_one_sol"

cp $IN/one_sol_ckpt.txt $OUT/one_sol_ckpt.txt

IN="H_bio_result_Full/laml/star_cdp_rand_sol/$DATA"
OUT="bio-result/$PDD/laml/$DATA/star_cdp_rand_sol"

cp $IN/one_sol_ckpt.txt $OUT/one_sol_ckpt.txt

IN="H_bio_result_Full/laml/star_cdp_sc/$DATA"
OUT="bio-result/$PDD/laml/$DATA/star_cdp_sc"

cp $IN/one_sol_ckpt.txt $OUT/one_sol_ckpt.txt




