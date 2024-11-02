import treeswift as ts
import pandas as pd
import os
import subprocess as sp
import re
import dendropy
import sys

result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/G_bio_result_pruned_deduplicate/paup'
data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data'

folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]

software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/B_scripts/KPTracer-Data"

comp_exe = os.path.join(software_dir, 'compare_two_rooted_trees_under_star.py')

for folder in folders:

    
    
    cmat_path = os.path.join(data_path, folder, folder + '_deduplicated_character_matrix.csv')
    
    
    # deduplicate_one_sol_path = os.path.join(result_dir, folder, 'paup_one_sol_deduplicate.tre')
    
    deduplicate_one_sol_path = os.path.join(result_dir, folder, 'paup_sc_deduplicate.tre')


    # contract_path = os.path.join(result_dir, folder, 'paup_one_sol_deduplicate_contract_sh.tre')
    contract_path = os.path.join(result_dir, folder, 'paup_sc_deduplicate_contract_sh.tre')

    score_res = sp.run(['python3', comp_exe, '-t1', deduplicate_one_sol_path, '-t2', deduplicate_one_sol_path, '-c1','1', '-c2', '1', '-m', cmat_path, '--extract_tree2', '1', '-t2p', contract_path], capture_output=True, text=True)  

    deduplicate_one_sol_path = os.path.join(result_dir, folder, 'paup_one_sol_deduplicate.tre')
    contract_path = os.path.join(result_dir, folder, 'paup_one_sol_deduplicate_contract_sh.tre')

    score_res = sp.run(['python3', comp_exe, '-t1', deduplicate_one_sol_path, '-t2', deduplicate_one_sol_path, '-c1','1', '-c2', '1', '-m', cmat_path, '--extract_tree2', '1', '-t2p', contract_path], capture_output=True, text=True)  