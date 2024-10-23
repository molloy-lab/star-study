import treeswift as ts
import pandas as pd
import os

result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/paup'
data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full'

folders = ['3457_Apc_T4_Fam', \
    '3513_NT_T1_Fam', \
    '3508_Apc_T2_Fam', \
    '3519_Lkb1_T1_Fam', \
    '3457_Apc_T1_Fam',\
    '3460_Lkb1_T1_Fam',\
    '3519_Lkb1_All',\
    '3454_Lkb1_All',\
    '3508_Apc_All',\
    '3515_Lkb1_T1_Fam',\
    '3515_Lkb1_All']

for folder in folders:
    cmat_file = os.path.join(data_path, folder, folder + '_deduplicated_character_matrix.csv')
    cmat_df = pd.read_csv(cmat_file, index_col=0, dtype=str)
    
    depruned_trees_path = [os.path.join(result_dir, folder, x) for x in ['one_sol_depruned_trees.newick', 'sc_depruned_trees.newick']]

    deduplicate_trees_path = [os.path.join(result_dir, folder, 'deduplicated_paup_' + x) for x in ['one_sol_trees.nwk', 'sc_trees.nwk']]
    
    
    for i in range(2):
        cur_depruned = depruned_trees_path[i]
        cur_deduplicate = deduplicate_trees_path[i]
        
        depruned_tre = ts.read_tree_newick(cur_depruned)
        deduplicate_tre = depruned_tre.extract_tree_with(set(cmat_df.index))
        deduplicate_tre.write_tree_newick(cur_deduplicate, hide_rooted_prefix=True)