#!/bin/bash

exit
MTHDS=( "star_cdp" \
        "laml" \
        "startle_nni" \
        "paup" \
        "cassiopeia_hybrid" )

LAML_MTHDS=( "paup_one_sol" "paup_sc" "star_cdp_one_sol" "star_cdp_rand_sol" "star_cdp_sc" "startle_nni" )

DATAS=( "3513_NT_T1_Fam" \
        "3515_Lkb1_T1_Fam" \
        "3724_NT_All" )

mkdir -p bio-result
cd bio-result

# Pipeline 1
for PIPELINE in "deduplicate-bio-result" "prune-deprune-deduplicate-bio-result"; do
mkdir -p $PIPELINE
cd $PIPELINE
for MTHD in ${MTHDS[@]}; do
    mkdir -p $MTHD
    cd $MTHD
    if [ $MTHD != "laml" ]; then
        for DATA in ${DATAS[@]}; do
            mkdir -p $DATA
        done 
    else
        for DATA in ${DATAS[@]}; do
            mkdir -p $DATA
	    cd $DATA
	    for LAML_MTHD in ${LAML_MTHDS[@]}; do
                mkdir -p $LAML_MTHD
            done
            cd ..
        done
    fi
    cd ..
done    
cd ..
done
