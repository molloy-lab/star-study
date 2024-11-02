import os
import sys
import shutil


data_path = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/KPTracer-Data"
start_trees_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/startle_nni'
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/laml'

folders = [f for f in os.listdir(start_trees_dir) if os.path.exists(os.path.join(start_trees_dir, f))]

for folder in folders:
    cur_tree_dir = os.path.join(start_trees_dir, folder, 'nni_tree.newick')
    cur_nj_dir = os.path.join(start_trees_dir, folder, 'nj_usage.log')
    cur_nni_dir = os.path.join(start_trees_dir, folder, 'nni_usage.log')
    shutil.copy(cur_tree_dir, os.path.join(result_dir, folder, 'nni_tree.newick'))
    shutil.copy(cur_nj_dir, os.path.join(result_dir, folder, 'nj_usage.log'))
    shutil.copy(cur_nj_dir, os.path.join(result_dir, folder, 'nni_usage.log'))

