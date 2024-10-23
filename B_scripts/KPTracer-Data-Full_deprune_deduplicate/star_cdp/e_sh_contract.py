import treeswift as ts
import pandas as pd
import os
import subprocess as sp
import re
import dendropy
import sys

result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/star_cdp'
data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full'

folders = ['3457_Apc_T4_Fam', \
    '3513_NT_T1_Fam', \
    '3508_Apc_T2_Fam', \
    '3519_Lkb1_T1_Fam', \
    '3457_Apc_T1_Fam',\
    '3460_Lkb1_T1_Fam',\
    '3515_Lkb1_T1_Fam']

software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/B_scripts/KPTracer-Data"

comp_exe = os.path.join(software_dir, 'compare_two_rooted_trees_under_star.py')

for folder in folders:

    
    
    cmat_path = os.path.join(data_path, folder, folder + '_deduplicated_character_matrix.csv')
    
    deduplicate_trees_path = [os.path.join(result_dir, folder, 'deduplicated_star_cdp_' + x + '_trees.nwk') for x in ['one_sol', 'rand_sol', 'sc']]

    contract_trees_path = [os.path.join(result_dir, folder, 'deduplicated_star_cdp_' + x + '_trees.nwk') for x in ['one_sol_sh', 'rand_sol_sh', 'sc_sh']]

    for i in range(3):

        deduplicate_one_sol_path = deduplicate_trees_path[i]
        contract_path = contract_trees_path[i]
        print(deduplicate_one_sol_path)

        score_res = sp.run(['python3', comp_exe, '-t1', deduplicate_one_sol_path, '-t2', deduplicate_one_sol_path, '-c1','1', '-c2', '1', '-m', cmat_path, '--extract_tree2', '1', '-t2p', contract_path], capture_output=True, text=True)  