import treeswift as ts
import pandas as pd
import os

result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/G_bio_result_pruned_deduplicate/star_cdp'
data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data'

folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]

for folder in folders:
    cmat_file = os.path.join(data_path, folder, folder + '_deduplicated_character_matrix.csv')
    cmat_df = pd.read_csv(cmat_file, index_col=0, dtype=str)
    depruned_one_sol_path = os.path.join(result_dir, folder, 'star_cdp_one_sol_depruned.tre')
    depruned_rand_sol_path = os.path.join(result_dir, folder, 'star_cdp_rand_depruned.tre')
    depruned_sc_path = os.path.join(result_dir, folder, 'star_cdp_sc_depruned.tre')

    deduplicate_one_sol_path = os.path.join(result_dir, folder, 'star_cdp_one_sol_deduplicate.tre')
    deduplicate_rand_sol_path = os.path.join(result_dir, folder, 'star_cdp_rand_sol_deduplicate.tre')
    deduplicate_sc_path = os.path.join(result_dir, folder, 'star_cdp_sc_deduplicate.tre')

    depruned_one_sol_tre = ts.read_tree_newick(depruned_one_sol_path)

    depruned_rand_sol_tre = ts.read_tree_newick(depruned_rand_sol_path)

    depruned_sc_tre = ts.read_tree_newick(depruned_sc_path)

    deduplicate_one_sol_tre = depruned_one_sol_tre.extract_tree_with(set(cmat_df.index))

    deduplicate_rand_sol_tre = depruned_rand_sol_tre.extract_tree_with(set(cmat_df.index))

    deduplicate_sc_tre = depruned_sc_tre.extract_tree_with(set(cmat_df.index))


    deduplicate_one_sol_tre.write_tree_newick(deduplicate_one_sol_path, hide_rooted_prefix=True)

    deduplicate_rand_sol_tre.write_tree_newick(deduplicate_rand_sol_path, hide_rooted_prefix=True)

    deduplicate_sc_tre.write_tree_newick(deduplicate_sc_path, hide_rooted_prefix=True)