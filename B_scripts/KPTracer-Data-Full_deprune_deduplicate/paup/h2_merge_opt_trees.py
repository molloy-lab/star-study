import os
import subprocess as sp
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import treeswift

def clean_newick_string(newick_str):
    # Remove all whitespace characters
    cleaned_newick_str = re.sub(r'\s+', '', newick_str)
    
    # Validate the Newick string (basic validation)
    if cleaned_newick_str.count('(') != cleaned_newick_str.count(')'):
        raise ValueError("Invalid Newick string: unmatched parentheses")
    
    if not cleaned_newick_str.endswith(';'):
        raise ValueError("Invalid Newick string: must end with a semicolon ';'")
    
    return cleaned_newick_str



def combine_newick_files(input_folder, output_file):
    """Combine all Newick strings from files in the input folder into a single output file."""
    combined_newick_strings = []
    trees = []
    for file_name in os.listdir(input_folder):
        if file_name.split('.')[-1] != 'newick':
            continue
        file_path = os.path.join(input_folder, file_name)
        print(file_path)
        if os.path.exists(output_file):
            os.remove(output_file)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                newick_string = file.read().strip()
                tre = treeswift.read_tree(newick_string, 'newick')
                trees.append(tre)
                combined_newick_strings.append(newick_string)
    print(len(combined_newick_strings))
    print(len(trees))
    with open(output_file, 'w') as out_file:
        for newick_string in combined_newick_strings:
            out_file.write(newick_string + '\n')

def main():


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/paup'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

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
    # folders = [f for f in folders if f.split("-")[0]=='nlin_50' and f.split("-")[1]!='ncas_20']

    # score_pattern = r"small parsimony score = ([\d.]+)"


    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)

            
        # opt_trees_dir = os.path.join(cur_res_path, 'optimal_trees')
        opt_trees_dir = os.path.join(cur_res_path, 'pruned_optimal_trees')
            
        # all_opt_trees_file = os.path.join(cur_res_path, 'all_paup_opt_trees.newicks')
        all_opt_trees_file = os.path.join(cur_res_path, 'pruned_all_paup_opt_trees.newicks')
        data_prefix = folder
        print(data_prefix)
        if not os.path.exists(all_opt_trees_file):
            combine_newick_files(opt_trees_dir, all_opt_trees_file)
            
            
               
if __name__ == '__main__':

    main()