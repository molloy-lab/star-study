import treeswift as ts
from typing import List, Tuple, Dict
import json
import os
import io
import sys


sys.path.append('../')
from utilities import *

def read_name_map(input:str, right2left=True) -> Dict[str,str]:
    nmap = {}

    with open(input, 'r') as fin:
        content = fin.read()
    lines = content.splitlines()

    for line in lines:
        [left, right] = line.split(',')
        if right2left:
            nmap[right] = left

        else:
            nmap[left] = right

    return nmap


def relabel_and_remove_outgroup(tre:ts.Tree, nmap:Dict[str, str]) -> ts.Tree:
    for leaf in tre.traverse_leaves():
        lab = leaf.label
        try:
            leaf.label = nmap[leaf.label]
        except KeyError:
            pass
   
    return tre.extract_tree_without(['ROOT0', 'ROOT1'])

def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/paup'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    paup_exe = os.path.join(software_dir, 'paup4a168_centos64')

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
        
        data_prefix = folder
        print(data_prefix)

        # all_paup_res_path = os.path.join(cur_res_path, 'one_sol_pruned_trees.newick')
        # replaced_back_all_tree_file = os.path.join(cur_res_path, 'one_sol_depruned_trees.newick')

        all_paup_res_path = os.path.join(cur_res_path, 'pruned_strict_consensus.tre')
        replaced_back_all_tree_file = os.path.join(cur_res_path, 'sc_depruned_trees.newick')
        eqclass_file = os.path.join(cur_data_path, folder + '_eqclass.json')
        
        with open(eqclass_file, 'r') as eqf:
            eqclass = json.load(eqf)

        if os.path.exists(all_paup_res_path):
                
            if not os.path.exists(replaced_back_all_tree_file):
                with open(all_paup_res_path, 'r') as aprp, open(replaced_back_all_tree_file, 'w') as rbatf:
                    for line in aprp:
                        pruned_tre = from_newick_get_nx_tree(io.StringIO(line))
                        replaced_tre = tree_to_newick_eq_classes(pruned_tre, eqclass)
                        rbatf.write(f"{replaced_tre};\n")
                
                print(f'finised:{replaced_back_all_tree_file}')
        else:
            print(f'warnning: miss {all_paup_res_path}')
            
            
if __name__ == '__main__':

    main()