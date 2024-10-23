import os
import sys
import shutil


data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle_data_in_startle'
start_trees_dir = result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/startle_nni'
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/laml'

folders = [f for f in os.listdir(start_trees_dir) if os.path.exists(os.path.join(start_trees_dir, f))]

for folder in folders:

    cur_data_path = os.path.join(data_path, folder)
    cur_res_path = os.path.join(result_dir, folder)

        
    reps = [rep for rep in os.listdir(cur_data_path) if os.path.isdir(os.path.join(cur_data_path, rep))]

    for rep in reps:


        cur_tree_dir = os.path.join(start_trees_dir, folder, rep,'nni_tree.newick')
        cur_nj_dir = os.path.join(start_trees_dir, folder, rep,'nj_usage.log')
        cur_nni_dir = os.path.join(start_trees_dir, folder, rep,'nni_usage.log')
        shutil.copy(cur_tree_dir, os.path.join(result_dir, folder, rep,'nni_tree.newick'))
        shutil.copy(cur_nj_dir, os.path.join(result_dir, folder, rep,'nj_usage.log'))
        shutil.copy(cur_nj_dir, os.path.join(result_dir, folder, rep,'nni_usage.log'))

