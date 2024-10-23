import treeswift as ts
import pandas as pd
import os
import subprocess as sp
import re
import dendropy
import sys

result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/paup'
data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full'

folders = ['3513_NT_T1_Fam', \
    '3515_Lkb1_T1_Fam',\
    '3724_NT_All']

software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/B_scripts/KPTracer-Data"

comp_exe = os.path.join(software_dir, 'compare_two_rooted_trees_under_star.py')

for folder in folders:

    
    
    cmat_path = os.path.join(data_path, folder, folder + '_character_matrix.csv')
    
    deduplicate_trees_path = [os.path.join(result_dir, folder, 'deduplicated_paup_' + x + '_trees.nwk') for x in ['one_sol', 'sc']]
    deduplicate_trees_path.append(os.path.join(result_dir, folder, 'one_sol_depruned_trees.newick'))
    deduplicate_trees_path.append(os.path.join(result_dir, folder, 'sc_depruned_trees.newick'))
    print(os.path.join(result_dir, folder, 'sc_depruned_trees.newick'))

    contract_trees_path = [os.path.join(result_dir, folder, 'deduplicated_paup_' + x + '_trees.nwk') for x in ['one_sol_sh', 'sc_sh']]
    contract_trees_path.append(os.path.join(result_dir, folder, 'one_sol_sh_full_trees.nwk'))
    contract_trees_path.append(os.path.join(result_dir, folder, 'sc_sh_full_trees.nwk'))
    for i in range(4):

        deduplicate_one_sol_path = deduplicate_trees_path[i]
        contract_path = contract_trees_path[i]
        print(deduplicate_one_sol_path)

        score_res = sp.run(['python3', comp_exe, '-t1', deduplicate_one_sol_path, '-t2', deduplicate_one_sol_path, '-c1','1', '-c2', '1', '-m', cmat_path, '--extract_tree2', '1', '-t2p', contract_path], capture_output=True, text=True)  