import os
import numpy as np
import pandas as pd
import json
import sys

from utilities import *

def main():

    trees_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full'

    folders = [f for f in os.listdir(trees_dir) if os.path.isdir(os.path.join(trees_dir, f))]
    
    count = 0

    for folder in folders:



        target_dir = os.path.join(trees_dir, folder)

        print(folder)
        pruned_matrix = os.path.join(target_dir, folder + '_deduplicated_character_matrix.csv')

        pruned_tree_file = os.path.join(target_dir, folder + '_deduplicated_tree.nwk')
        
        eqclass = os.path.join(target_dir, folder + '_deduplicated_eqclass.json')

        # eq_upto_miss = os.path.join(target_dir, folder + '_eqclass_upto_miss.csv')
        # pruned_upto_miss_character_matrix = os.path.join(target_dir, folder + '_pruned_upto_miss_character_matrix.txt')
        # pruned_upto_miss_tree = os.path.join(target_dir, folder + '_pruned_upto_miss_tree.nwk')
        
        cmat_name = folder + '_character_matrix.csv'
        tree_name = folder + '_tree.nwk'
        tree = os.path.join(target_dir, tree_name)
        cmat = os.path.join(target_dir, cmat_name)
        
        if not os.path.exists(cmat):
            continue
        
        
        cmat = pd.read_csv(cmat,index_col=[0], sep=',', dtype=str)
        
        eq_class, cmat = compute_equivalence_classes_up_to_exact(cmat)
        
        with open(eqclass, 'w') as ef:
            json.dump(eq_class, ef)

        cmat.to_csv(pruned_matrix, sep=',')
        count += 1
        
    print(f"total:{len(folders)}, finished:{count}")
    
    


if __name__ == "__main__":
    main()