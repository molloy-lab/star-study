import os

import re

import pandas as pd
from collections import defaultdict


def contract_edges(node):
    # If node has no children, return it as is
    if node not in tree:
        return str(node)

    children = []
    for child in tree[node]:
        # Check if the edge has mutations
        if (node, child) in edges_with_mutations:
            # If it has mutations, keep the child as a separate branch
            children.append(contract_edges(child))
        else:
            # If no mutations, merge the child with its descendants
            grandchildren = contract_edges(child)
            
            children.extend(grandchildren.split(','))

    if len(children) == 1:
        return children[0]  # Contracted node

    # Format the Newick string for the current node
    return f"({','.join(children)}){node}"


trees_directory = 'sashittal2023startle_used_in_startle'

models_dir = [f for f in os.listdir(trees_directory) if os.path.isdir(os.path.join(trees_directory, f))]


for model_dir in models_dir:
    cur_model = os.path.join(trees_directory, model_dir)
    reps = [rep for rep in os.listdir(cur_model) if os.path.isdir(os.path.join(cur_model, rep))]
    for rep in reps:
        cur_rep_dir = os.path.join(cur_model, rep)
        edge_list_file = os.path.join(cur_rep_dir, next(\
            (file for file in os.listdir(cur_rep_dir) if file.endswith('_edgelist.csv')), None))

        edge_labels_file = os.path.join(cur_rep_dir, next(\
            (file for file in os.listdir(cur_rep_dir) if file.endswith('_edge_labels.csv')), None))
        
        edge_list_df = pd.read_csv(edge_list_file) 
        edge_labels_df = pd.read_csv(edge_labels_file)

        edges_with_mutations = set(zip(edge_labels_df['src'], edge_labels_df['dst']))
        all_edges = set(zip(edge_list_df['src'], edge_list_df['dst']))


        tree = defaultdict(list)

        for _, row in edge_list_df.iterrows():
            src, dst = row['src'], row['dst']
            tree[src].append(dst)

        newick_string = contract_edges(0) + ';'

        result_tree_file = os.path.join(cur_rep_dir,'contracted_true_tree.newick')

        with open(result_tree_file, 'w') as file:
            file.write(newick_string)