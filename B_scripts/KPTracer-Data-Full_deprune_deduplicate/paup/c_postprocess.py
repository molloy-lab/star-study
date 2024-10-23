import treeswift as ts
from typing import List, Tuple, Dict
import json
import os
import io
import sys

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

        all_trees_path = os.path.join(cur_res_path, "all_trees.trees")
        all_paup_res_path = os.path.join(cur_res_path, 'paup_trees.trees')
        nmap_file = os.path.join(cur_res_path, 'taxon_map.csv')
        nmap = read_name_map(nmap_file)

        if os.path.exists(all_trees_path):
                
            if not os.path.exists(all_paup_res_path):
                with open(all_trees_path, 'r') as atf, open(all_paup_res_path, 'w') as nbatf:
                    for line in atf:
                        tre = ts.read_tree_newick(line)
                        tre = relabel_and_remove_outgroup(tre, nmap)
                        nwk = tre.newick().replace('[&R]', '') + '\n'
                        nbatf.write(nwk)
                
                print(f'finised:{all_paup_res_path}')
            else:
                print(f'warnning: miss {all_trees_path}')
            
            
if __name__ == '__main__':

    main()