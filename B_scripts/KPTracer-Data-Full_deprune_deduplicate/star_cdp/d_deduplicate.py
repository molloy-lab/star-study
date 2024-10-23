import treeswift as ts
import pandas as pd
import os

result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/star_cdp'
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

    depruned_trees_path = [os.path.join(result_dir, folder, 'depruned_star_cdp_' + x) for x in ['one_sol.tre', 'random_sol_trees.tre', 'strict_consensus.tre']]

    deduplicate_trees_path = [os.path.join(result_dir, folder, 'deduplicated_star_cdp_' + x) for x in ['one_sol_trees.nwk', 'rand_sol_trees.nwk', 'sc_trees.nwk']]
    
    
    for i in range(3):
        cur_depruned = depruned_trees_path[i]
        cur_deduplicate = deduplicate_trees_path[i]
        
        depruned_tre = ts.read_tree_newick(cur_depruned)
        deduplicate_tre = depruned_tre.extract_tree_with(set(cmat_df.index))
        deduplicate_tre.write_tree_newick(cur_deduplicate, hide_rooted_prefix=True)
