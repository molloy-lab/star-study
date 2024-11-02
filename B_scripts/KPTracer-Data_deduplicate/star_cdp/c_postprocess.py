import pandas
import treeswift as ts
import os
import shutil
import sys
import json

sys.path.append('../prepare')

from utilities import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('pruned_tree', type=str, help='pruned_tree')
parser.add_argument('no_outg_tree_path', type=str, help="no_outg_tree_path")
parser.add_argument('replaced_tree_path', type=str, help='replaced_tree_path')
args = parser.parse_args()

pruned_tree = args.pruned_tree
no_outg_tree_path = args.no_outg_tree_path
replaced_tree_path = args.replaced_tree_path

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
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/F_bio_result_deduplicate/star_cdp'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data"
    

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
  

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
            
        pmap_file = os.path.join(cur_data_path, folder + '_deduplicated_eqclass.json')
        #pruned_tree = os.path.join(cur_res_path, 'star_cdp_one_sol.tre')
        # pruned_tree = os.path.join(cur_res_path, 'consensus_star_cdp_strict_consensus.tre')
        # pruned_tree = os.path.join(cur_res_path, 'consensus_star_cdp_majority_consensus.tre')
        # pruned_tree = os.path.join(cur_res_path, 'consensus_star_cdp_greedy_consensus.tre')
        # pruned_tree = os.path.join(cur_res_path, 'star_cdp_migration.tre')
        # pruned_tree = os.path.join(cur_res_path, 'star_cdp-rand-1_one_sol.tre')
        # pruned_tree = os.path.join(cur_res_path, 'star_cdp_sc_strict_consensus.tre')
        pruned_tree = os.path.join(cur_res_path, pruned_tree)
        if not os.path.exists(pruned_tree):
            print(f"Missing {pruned_tree}")
            continue

        with open(pmap_file, 'r') as pf:
            pmap = json.load(pf)

        data_prefix = folder 
        print(data_prefix)
        
        # no_outg_tree_path = os.path.join(cur_res_path, 'removed_outg_star_cdp_one_sol.tre')
        # no_outg_tree_path = os.path.join(cur_res_path, 'removed_outg_consensus_star_cdp_strict_consensus.tre')
        # no_outg_tree_path = os.path.join(cur_res_path, 'removed_outg_consensus_star_cdp_majority_consensus.tre')
        # no_outg_tree_path = os.path.join(cur_res_path, 'removed_outg_star_cdp_migration.tre')
        # no_outg_tree_path = os.path.join(cur_res_path, 'removed_outg_star_cdp_sc_strict_consensus.tre')
        no_outg_tree_path = os.path.join(cur_res_path, no_outg_tree_path)

        if not os.path.exists(no_outg_tree_path):
            remove_outg(pruned_tree, no_outg_tree_path)

        # replaced_tree_path = os.path.join(cur_res_path, 'replaced_star_cdp_one_sol.tre')
        # replaced_tree_path = os.path.join(cur_res_path, 'replaced_consensus_star_cdp_strict_consensus.tre')
        # replaced_tree_path = os.path.join(cur_res_path, 'replaced_consensus_star_cdp_majority_consensus.tre')
        # replaced_tree_path = os.path.join(cur_res_path, 'replaced_star_cdp_migration.tre')
        # replaced_tree_path = os.path.join(cur_res_path, 'replaced_star_cdp_sc_strict_consensus.tre')
        replaced_tree_path = os.path.join(cur_res_path, replaced_tree_path)

        # pruned_tree = from_newick_get_nx_tree(no_outg_tree_path)

        # pruned_tree = ts.read_tree_newick(no_outg_tree_path)
        pruned_tree = from_newick_get_nx_tree(no_outg_tree_path)
        # leaves = []
        # for leaf in pruned_tree.traverse_leaves():
            # leaves.append(leaf.get_label())
            # leaves.append(leaf)
        # leaves = [node for node in pruned_tree.nodes if pruned_tree.out_degree(node) == 0]
        # print("Leaf nodes:", leaves)
        # print("# of leaf:", len(leaves))
        # replaced_tree = tree_to_newick_eq_classes(pruned_tree, pmap)

        # replaced_tree = replaced_pruned_cells(pruned_tree, pmap)
        # replaced_tree.write_tree_newick(replaced_tree_path,hide_rooted_prefix=True)

        replaced_tree_nwk = tree_to_newick_eq_classes(pruned_tree, pmap)
        with open(replaced_tree_path, 'w') as rf:
            rf.write(replaced_tree_nwk)

        # with open(replaced_tree_path, 'w') as rf:
            # rf.write(f"{replaced_tree};")

        ##note: Using treeswfit to read the greedy consensus tree get # of leaves = 1207
        ##note: But use code in Startle paper to read a tree get # of leaves = 1247 which is incorrect

if __name__ == '__main__':

    main()