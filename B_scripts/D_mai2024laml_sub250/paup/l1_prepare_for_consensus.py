import os
import subprocess as sp
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction




def write_to_nexus(paup_file, opt_trees_file, consensus_tree_file):
    # Note - 
    # irreversible (Camin-Sokal); up means higher numbers are derived
    # you can use weight set of integers...
    # I can probably do round to second decimal and take base 100 weights
    with open(paup_file, 'w') as fp:
        fp.write("#NEXUS\n")
        fp.write("BEGIN PAUP;\n")
        fp.write("set maxtrees=510;\n")
        fp.write("set autoclose=yes warntree=no warnreset=no;\n")
        fp.write(f"gettrees file={opt_trees_file};\n")
        fp.write(f"contree all/strict=yes treefile={consensus_tree_file}")
        fp.write(" format=newick;\n")
        fp.write("END;\n")





def main():


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/paup'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    

    # score_pattern = r"small parsimony score = ([\d.]+)"


    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
            
        opt_trees_dir = os.path.join(cur_res_path, 'optimal_trees')
            
        all_opt_trees_file = os.path.join(cur_res_path, 'all_paup_opt_trees.newicks')
        data_prefix = folder
        print(data_prefix)
        write_to_nexus(os.path.join(cur_res_path, 'paup_consensus.nex'), all_opt_trees_file, os.path.join(cur_res_path, 'strict_consensus.tre'))
            
            
               
if __name__ == '__main__':

    main()