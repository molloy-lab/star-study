import os
import pandas as pd
import treeswift as ts




def get_highest_probability(value):
    if '/' in value:  
        pairs = value.split('/') 
        state, prob = max((pair.split(':') for pair in pairs), key=lambda x: float(x[1]))
        return state 
    return value  



def contract_tree(seq_file:str, output_tree:str):
    
    
    
    newick_str = ""
    
    with open(seq_file, 'r') as rf:
        newick_str = rf.readline()
    
    tre = ts.read_tree_newick(newick_str)

    seq = pd.read_csv(seq_file, skiprows=1, header=None)

    seq = seq.set_index(0).T.to_dict('list')
    
    for cell,sites in seq.items():
        processed_sites = [get_highest_probability(str(site)) for site in sites]
        # print(processed_sites)
        seq[cell] = processed_sites

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



    
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/laml'


folders = [f for f in os.listdir(result_dir) if os.path.isdir(os.path.join(result_dir, f))]



for folder in folders:
        cur_res_path = os.path.join(result_dir, folder)
        
        reps = [rep for rep in os.listdir(cur_res_path) if os.path.isdir(os.path.join(cur_res_path, rep))]
        
        for rep in reps:
            cur_rep_res_path = os.path.join(cur_res_path, rep)

            print(cur_rep_res_path)
            cur_tree_file = os.path.join(cur_rep_res_path,'laml_output_trees.nwk')
            cur_seq_file = os.path.join(cur_rep_res_path, 'laml_output_annotations.txt')
            cur_output_file = os.path.join(cur_rep_res_path, 'contract_laml_tree.nwk')
            contract_tree(cur_seq_file, cur_output_file)