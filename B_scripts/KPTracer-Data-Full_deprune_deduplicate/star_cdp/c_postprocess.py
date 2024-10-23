import pandas
import treeswift as ts
import os
import shutil
import sys
import json

sys.path.append('../')

from utilities import *
#assume only one outgroup 0 
def remove_outg(tree_path: str, output:str):
    # with open(tree_path, 'r') as infile, open(output, 'w') as outfile:
    #     for line in infile:
    #          newick_trimmed = line.strip()[:-1]
    #          newick_trimmed = newick_trimmed[3:-1]
    #          outfile.write(newick_trimmed + ';\n')
    tree = ts.read_tree_newick(tree_path)
    outgroup = {'0'}
    no_outg_tree = tree.extract_tree_without(outgroup)
    no_outg_tree.write_tree_newick(output,hide_rooted_prefix=True)




def replaced_pruned_cells(tree, eqclass):
    for leaf in tree.traverse_leaves():
        if leaf.get_label() in eqclass:
            new_leaves = eqclass[leaf.get_label()]
            parent = leaf.get_parent()
            for new_leaf_label in new_leaves:
                new_leaf = ts.Node(label=new_leaf_label)
                parent.add_child(new_leaf)
            parent.remove_child(leaf)
    return tree



def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/star_cdp'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full"
    

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
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
            
        pmap_file = os.path.join(cur_data_path, folder + '_eqclass.json')

        #pruned_tree = os.path.join(cur_res_path, 'star_cdp_one_sol.tre')
        pruned_trees = ['star_cdp_one_sol.tre', 'star_cdp_strict_consensus.tre', 'star_cdp_random_sol_trees.tre']

        for pruned_tree in pruned_trees:
            cur_pruned_tree_path = os.path.join(cur_res_path, pruned_tree)
            if not os.path.exists(cur_pruned_tree_path):
                print(f"Missing {cur_pruned_tree_path}")
                continue

            with open(pmap_file, 'r') as pf:
                pmap = json.load(pf)

            data_prefix = folder 
            print(data_prefix)
            
            no_outg_tree_path = os.path.join(cur_res_path, 'removed_outg_' + pruned_tree)

            if not os.path.exists(no_outg_tree_path):
                remove_outg(cur_pruned_tree_path, no_outg_tree_path)

            replaced_tree_path = os.path.join(cur_res_path, 'depruned_' + pruned_tree)

            tre = from_newick_get_nx_tree(no_outg_tree_path)
        
            replaced_tree_nwk = tree_to_newick_eq_classes(tre, pmap)
            with open(replaced_tree_path, 'w') as rf:
                rf.write(replaced_tree_nwk)

        ##note: Using treeswfit to read the greedy consensus tree get # of leaves = 1207
        ##note: But use code in Startle paper to read a tree get # of leaves = 1247 which is incorrect

if __name__ == '__main__':

    main()