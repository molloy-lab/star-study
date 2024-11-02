import os
import sys
import shutil


data_path = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data"
start_trees_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/G_bio_result_pruned_deduplicate/'
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/G_bio_result_pruned_deduplicate/laml'

folders = ['3724_NT_All', '3513_NT_T1_Fam']
methods = [f for f in os.listdir(result_dir) if os.path.exists(os.path.join(result_dir, f))]
print(folders)
methods = ['paup_sc']
print(methods)


for folder in folders:
    for method in methods:
        if not os.path.exists(os.path.join(result_dir, method, folder)):
            os.mkdir(os.path.join(result_dir, method, folder))

        if method == 'startle_nni_pub':
            continue

        method_prefix = method
        method_suffix = method

        if method == 'paup_sc':
            method_prefix = 'paup'

        if method in ['star_cdp_rand_sol', 'star_cdp_one_sol', 'star_cdp_sc']:
            method_prefix = 'star_cdp'
        elif method in ['paup_one_sol']:
            method_prefix = 'paup'
        elif method in ['startle_nni', 'python_startle_nni']:
            method_suffix = 'nni_tree'
        elif method in ['paup_sc']:
            method_suffix = 'paup_sc'
        


        cur_start_tree_path = os.path.join(start_trees_dir, method_prefix, folder, method_suffix + '_deduplicate.tre')
        
        prefix = method
        
        if method in ['python_startle_nni', 'startle_nni']:
            prefix = 'nni_tree'
        
        shutil.copy(cur_start_tree_path, os.path.join(result_dir,method, folder, prefix + '_deduplicate.tre'))

    
