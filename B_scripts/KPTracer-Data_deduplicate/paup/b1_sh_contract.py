import treeswift as ts
import pandas as pd
import os
import subprocess as sp
import re
import dendropy
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('deduplicate_one_sol_path', type=str, help="deduplicate_one_sol_path")
parser.add_argument('contract_path', type=str, help="contract_path")

args = parser.parse_args()
deduplicate_one_sol_path = args.deduplicate_one_sol_path
contract_path = args.contract_path

result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/F_bio_result_deduplicate/paup'
data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data'

folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]

software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/B_scripts/KPTracer-Data"

comp_exe = os.path.join(software_dir, 'compare_two_rooted_trees_under_star.py')

for folder in folders:

    
    
    cmat_path = os.path.join(data_path, folder, folder + '_deduplicated_character_matrix.csv')
    
    
    # deduplicate_one_sol_path = os.path.join(result_dir, folder, 'removed_outg_star_cdp_rand_one_sol.tre')
    # contract_path = os.path.join(result_dir, folder, 'star_cdp_rand_sol_sh.tre')

    # deduplicate_one_sol_path = os.path.join(result_dir, folder, 'sc_branch_trees.nwk')
    # contract_path = os.path.join(result_dir, folder, 'sc_sh.tre')

    deduplicate_one_sol_path = os.path.join(result_dir, folder, deduplicate_one_sol_path)
    contract_path = os.path.join(result_dir, folder, contract_path)


    score_res = sp.run(['python3', comp_exe, '-t1', deduplicate_one_sol_path, '-t2', deduplicate_one_sol_path, '-c1','1', '-c2', '1', '-m', cmat_path, '--extract_tree2', '1', '-t2p', contract_path], capture_output=True, text=True)  