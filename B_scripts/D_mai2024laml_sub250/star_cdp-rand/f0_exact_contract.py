import os
import subprocess as sp
import re
import dendropy
import sys
import treeswift
import pandas




def infer_states_under_star_at_internal_helper(states_below):
    # Assume ambiguous state = -1
    #        unedited state = 0
    #        edited states = 1, 2, ...

    states_below_list = sorted(list(states_below))

    nbelow = len(states_below_list)
    if nbelow == 1:
        state = states_below_list[0]
    elif nbelow == 2:
        if -1 in states_below:
            state = states_below_list[1]
        else:
            state = 0
    else:
        state = 0

    return state


def infer_states_under_star_at_leaf(node, cmat):
    
    # states_at_leaf = cmat.loc[cmat["cell"] == node.label].values[0][1:]
    states_at_leaf = cmat.loc[int(node.label)].values.tolist()
    
    node.states = []
    node.states_below = []
    for state in states_at_leaf:
        state_set = set([state])
        node.states_below.append(state_set)
        node.states += list(state_set)


def infer_states_under_star_at_internal(node, children):
    nchar = len(children[0].states_below)
    node.states = []
    node.states_below = []

    for i in range(nchar):
        # Get states below
        states_below = children[0].states_below[i]
        for child in children[1:]:
            states_below = states_below.union(child.states_below[i])
        node.states_below.append(states_below)

        # Infer ancestral states
        state = infer_states_under_star_at_internal_helper(states_below)
        node.states += [state]

    for child in children:
        del child.states_below


def get_mutations_on_edge(head, tail):
    nchar = len(head.states)
    muts = []
    for i in range(nchar):
        hs = head.states[i]
        ts = tail.states[i]
        if hs == ts:
            pass
        else:
            if hs != 0 and ts != -1:
                print('hs: ', hs)
                print('ts: ', ts)
                sys.exit("Error in star labeling!")
            muts.append((i, ts))
    return muts


def get_mutations_above_root(root):
    nchar = len(root.states)
    muts = [] 
    for i in range(nchar):
        rs = root.states[i]
        if rs == 0:
            pass
        else:
            muts.append((i, rs))
    return muts


def infer_muts_under_star_model(tree, cmat):
    for node in tree.traverse_postorder():
        if node.is_leaf():
            infer_states_under_star_at_leaf(node, cmat)
        else:
            # Check if node is binary
            children = node.child_nodes()

            infer_states_under_star_at_internal(node, children)

            # Annotate child edges with mutations
            for child in children:
                child.muts = get_mutations_on_edge(node, child)
                child.set_edge_length(len(child.muts))

    # Lastly process the root!
    root = tree.root
    root.muts = get_mutations_above_root(root)
    root.set_edge_length(len(root.muts))

    return tree




def contract_zero_length_branches(tree):
    # Set incoming edges incident to root and leaves
    # to be greater than 0 so they are not contracted
    rlen = tree.root.get_edge_length()
    if rlen == 0:
        tree.root.set_edge_length(0.5)

    for node in tree.traverse_leaves():
        if node.get_edge_length() == 0:
            node.set_edge_length(0.5)

    # Contract zero length edges
    for node in tree.traverse_postorder():
        if node.get_edge_length() == 0:
            node.contract()

    # Re-set edge lengths associated with root and leaves
    for node in tree.traverse_leaves():
        if node.get_edge_length() == 0.5:
            node.set_edge_length(0.0)

    if rlen == 0:
        tree.root.set_edge_length(0.0)



def EX_contract_tree(treefile:str, cmatf:str,output_tree:str):
    tre = treeswift.read_tree_newick(treefile)
    cmat = pandas.read_csv(cmatf, index_col=0)

    infer_muts_under_star_model(tre, cmat)
    contract_zero_length_branches(tre)

    tre.write_tree_newick(output_tree)





def main():
    sys.setrecursionlimit(4000)

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/star_cdp'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/scripts/sashittal2023startle-sim"

    comp_exe = os.path.join(software_dir, 'compare_two_rooted_trees_under_star.py')


    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]


    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        

        cmat_path = os.path.join(cur_data_path, "startle_format_cmat.csv")
            
        cur_tree_path = os.path.join(cur_res_path, 'consensus_star_cdp_strict_consensus.tre')
        cur_outf_tree_path = os.path.join(cur_res_path, 'exact_contract_star_cdp_strict_consensus.tre')
        EX_contract_tree(cur_tree_path, cmat_path, cur_outf_tree_path)
        print('finished: ', cur_outf_tree_path)
        


if __name__ == '__main__':

    main()