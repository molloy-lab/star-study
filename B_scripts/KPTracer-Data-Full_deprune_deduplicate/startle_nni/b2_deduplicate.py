import os
import subprocess as sp
import pandas as pd 
import numpy as np
import sys 
import json
import treeswift as ts


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

            
        cmat_file = os.path.join(cur_data_path, folder + '_deduplicated_character_matrix.csv')
    
        cmat_df = pd.read_csv(cmat_file, index_col=0, dtype=str)
        

        depruned_tree_path = os.path.join(cur_res_path, 'depruned.tre')
        
        deduplicate_tree_path = os.path.join(cur_res_path, 'deduplicate.tre')
        depruned_tree = ts.read_tree_newick(depruned_tree_path)
        deduplicate_tree = depruned_tree.extract_tree_with(set(cmat_df.index))
        deduplicate_tree.write_tree_newick(deduplicate_tree_path, hide_rooted_prefix=True)


if __name__ == '__main__':

    main()