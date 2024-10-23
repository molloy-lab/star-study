import treeswift as ts
import pandas as pd
import os

result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/G_bio_result_pruned_deduplicate/python_startle_nni'
data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data'

folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]

for folder in folders:
    
    cmat_file = os.path.join(data_path, folder, folder + '_deduplicated_character_matrix.csv')
    
    cmat_df = pd.read_csv(cmat_file, index_col=0, dtype=str)
    
    depruned_one_sol_path = os.path.join(result_dir, folder, 'nni_tree_depruned.tre')
    
    deduplicate_one_sol_path = os.path.join(result_dir, folder, 'nni_tree_deduplicate.tre')
    
    depruned_one_sol_tre = ts.read_tree_newick(depruned_one_sol_path)

    
    deduplicate_one_sol_tre = depruned_one_sol_tre.extract_tree_with(set(cmat_df.index))

    deduplicate_one_sol_tre.write_tree_newick(deduplicate_one_sol_path, hide_rooted_prefix=True)
