import pandas as pd
import os
import sys
import treeswift as ts

data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250'



def check_SH_mutation_less(parent_state, children_state):
    n = len(parent_state)
    if n != len(children_state):
        raise Exception("Two state vector with different len")
    else:
        for i in range(n):
            if children_state[i] != '?' and children_state[i] != parent_state[i]:
                return False
    return True



def contract_tree_SH(treefile:str, seq_file:str, output_tree:str):
    tre = ts.read_tree_newick(treefile)
    seq = pd.read_csv(seq_file)
    seq = seq.set_index('cell').T.to_dict('list')
    
    rlen = tre.root.get_edge_length()

    for node in tre.traverse_postorder():
        if not node.is_root():
            parent = node.get_parent()
            
            parent_state = seq[parent.label]
            parent_state = ['?' if x in ['s', 'd'] else x for x in parent_state]
            node_state = seq[node.label]
            node_state = ['?' if x in ['s', 'd'] else x for x in node_state]


            if not check_SH_mutation_less(parent_state, node_state):
                
                node.set_edge_length(sum(1 for a, b in zip(seq[parent.label], seq[node.label]) if a != b))
            
            else:
                node.set_edge_length(0)
        else:
            if rlen == 0:
                node.set_edge_length(0.5)
        if node.is_leaf():
            if node.get_edge_length() == 0:
                node.set_edge_length(1)

    for node in tre.traverse_postorder():
        if node.get_edge_length() == 0:
            node.contract()

    for node in tre.traverse_leaves():
        if node.get_edge_length() == 0.5:
            node.set_edge_length(0.0)

    if rlen == 0:
        tree.root.set_edge_length(0.0)

    tre.write_tree_newick(output_tree)


def contract_tree(treefile:str, seq_file:str, output_tree:str):
    tre = ts.read_tree_newick(treefile)
    seq = pd.read_csv(seq_file)
    seq = seq.set_index('cell').T.to_dict('list')
    
    
    rlen = tre.root.get_edge_length()

    for node in tre.traverse_postorder():
        if not node.is_root():
            parent = node.get_parent()
            
            if seq[parent.label]  != seq[node.label]:
                
                node.set_edge_length(sum(1 for a, b in zip(seq[parent.label], seq[node.label]) if a != b))
            
            else:
                node.set_edge_length(0)
        else:
            if rlen == 0:
                node.set_edge_length(0.5)
        if node.is_leaf():
            if node.get_edge_length() == 0:
                node.set_edge_length(1)

    for node in tre.traverse_postorder():
        if node.get_edge_length() == 0:
            node.contract()

    for node in tre.traverse_leaves():
        if node.get_edge_length() == 0.5:
            node.set_edge_length(0.0)

    if rlen == 0:
        tree.root.set_edge_length(0.0)

    tre.write_tree_newick(output_tree)
        
        
        





folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
folders = [f for f in folders if f not in ['model_tree.txt', 'summary_stats.txt', 'true_missing_stats.txt']]

for folder in folders:
    cur_path = os.path.join(data_path, folder)
    cur_tree_file = os.path.join(cur_path, 'true_tree.tre')
    cur_seq_file = os.path.join(cur_path, 'all_sequences.txt')
    # cur_output_tree = os.path.join(cur_path, 'SH_contract_true_tree.tre')
    cur_output_tree = os.path.join(cur_path, 'Exact_contract_true_tree.tre')
    contract_tree(cur_tree_file, cur_seq_file,cur_output_tree)
    # contract_tree_SH(cur_tree_file, cur_seq_file,cur_output_tree)
    print(cur_path)
