import os
import subprocess as sp
import pandas as pd 
import numpy as np
import sys 
import json

sys.path.append('../')
from utilities import *

def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/startle_nni'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')
    
    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

    # folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]

    data_df = pd.read_csv('../cells_number.csv')
    sorted_df = data_df.sort_values(by='rest_cell_num')
    folders = sorted_df['data'].values
    folders = folders.tolist()
    folders.remove('3724_NT_All')

    
    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)

            
        cmat_path = os.path.join(cur_data_path, folder + '_pruned_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv')
        
        pmap_file = os.path.join(cur_data_path, folder + '_eqclass.json')

        with open(pmap_file, 'r') as pf:
            pmap = json.load(pf)

        pruned_tree_path = os.path.join(cur_res_path,'nni_tree.newick')

        if not os.path.exists(pruned_tree_path):
                print(f"Failed to find starting tree: {pruned_tree_path}")
                continue
        print(pruned_tree_path)

        depruned_tree_path = os.path.join(cur_res_path, 'depruned.tre')
        pruned_tree = from_newick_get_nx_tree(pruned_tree_path)
        depruned_tree = tree_to_newick_eq_classes(pruned_tree, pmap)

        with open(depruned_tree_path, 'w') as rf:
            rf.write(f"{depruned_tree};")


if __name__ == '__main__':

    main()