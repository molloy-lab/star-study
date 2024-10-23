import treeswift as ts
import pandas as pd
import os
import subprocess as sp
import re
import dendropy
import sys

result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/I_bio_result_Full_deduplicate/laml'
data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full'

folders = ['3515_Lkb1_T1_Fam']

software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/B_scripts/KPTracer-Data"

comp_exe = os.path.join(software_dir, 'compare_two_rooted_trees_under_star.py')


methods = ['paup_one_sol', 'paup_sc', 'star_cdp_one_sol', 'star_cdp_rand_sol', 'star_cdp_sc', 'startle_nni']

count = 0
for folder in folders:

    for method in methods:

    
    
        cmat_path = os.path.join(data_path, folder, folder + '_deduplicated_character_matrix.csv')

        deduplicate_one_sol_path = os.path.join(result_dir, method, folder, 'one_sol_trees.nwk')

        if not os.path.exists(deduplicate_one_sol_path):
            deduplicate_one_sol_path = os.path.join(result_dir, method, folder, 'one_sol_24hrs_best_trees.nwk')
            
        if os.path.exists(deduplicate_one_sol_path):
            count += 1
            contract_path = os.path.join(result_dir, method, folder, 'one_sol_sh_trees.nwk')
            print(deduplicate_one_sol_path)
            score_res = sp.run(['python3', comp_exe, '-t1', deduplicate_one_sol_path, '-t2', deduplicate_one_sol_path, '-c1','1', '-c2', '1', '-m', cmat_path, '--extract_tree2', '1', '-t2p', contract_path], capture_output=True, text=True)  

print(f'tot: {len(folders)*len(methods)}, finished: {count}')