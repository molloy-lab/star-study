import os
import subprocess as sp
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction




def write_to_nexus(paup_file, opt_trees_file, consensus_tree_file):
    # Note - 
    # irreversible (Camin-Sokal); up means higher numbers are derived
    # you can use weight set of integers...
    # I can probably do round to second decimal and take base 100 weights
    with open(paup_file, 'w') as fp:
        fp.write("#NEXUS\n")
        fp.write("BEGIN PAUP;\n")
        fp.write("set maxtrees=510;\n")
        fp.write("set autoclose=yes warntree=no warnreset=no;\n")
        fp.write(f"gettrees file={opt_trees_file};\n")
        fp.write(f"contree all/strict=yes treefile={consensus_tree_file}")
        fp.write(" format=newick;\n")
        fp.write("END;\n")





def main():


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/paup'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

    folders = ['3457_Apc_T4_Fam', \
    '3513_NT_T1_Fam', \
    '3508_Apc_T2_Fam', \
    '3519_Lkb1_T1_Fam', \
    '3457_Apc_T1_Fam',\
    '3460_Lkb1_T1_Fam',\
    '3519_Lkb1_All',\
    '3454_Lkb1_All',\
    '3508_Apc_All',\
    '3515_Lkb1_T1_Fam',\
    '3515_Lkb1_All']


    # score_pattern = r"small parsimony score = ([\d.]+)"


    for folder in folders:

        cur_res_path = os.path.join(result_dir, folder)
    
        # opt_trees_dir = os.path.join(cur_res_path, 'optimal_trees')
        opt_trees_dir = os.path.join(cur_res_path, 'pruned_optimal_trees')
            
        # all_opt_trees_file = os.path.join(cur_res_path, 'all_paup_opt_trees.newicks')
        all_opt_trees_file = os.path.join(cur_res_path, 'pruned_all_paup_opt_trees.newicks')
        data_prefix = folder 
        print(data_prefix)
        # write_to_nexus(os.path.join(cur_res_path, 'paup_consensus.nex'), all_opt_trees_file, os.path.join(cur_res_path, 'strict_consensus.tre'))
        write_to_nexus(os.path.join(cur_res_path, 'pruned_paup_consensus.nex'), all_opt_trees_file, os.path.join(cur_res_path, 'pruned_strict_consensus.tre'))
            
               
if __name__ == '__main__':

    main()