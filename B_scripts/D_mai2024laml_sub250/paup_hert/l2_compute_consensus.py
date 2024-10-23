import os
import subprocess as sp
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction



def write_paup_sbatch(curr_dir : str, paup_exe: str, paup_nex_file:str, sbatch_file:str):
    # sbatch_file_name = 'run_nni.sbatch'
    # sbatch_file = os.path.join(curr_dir, sbatch_file_name)
    time="/usr/bin/time"
    rows_to_wrtie = ['#!/bin/bash', 
                     '#SBATCH --time=24:00:00', 
                     '#SBATCH --cpus-per-task=1', 
                     '#SBATCH --ntasks=1',
                    '#SBATCH --mem=48G',
                    '#SBATCH --qos=highmem',
                    '#SBATCH --partition=cbcb',
                    '#SBATCH --account=cbcb',
                    '#SBATCH --constraint=EPYC-7313',
                    '#SBATCH --exclusive',
                    'module load Python3/3.8.15',
                    ' '.join([time, '-v', '-o', 'paup_consensus_usage.log', paup_exe, paup_nex_file, '&>', 'consensus_paup.log', '2>&1'])
                    ]

    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))



def submit_paup_sbacth(sbatch: str, data_prefix: str, res_dir:str):
    job_name = "--job-name=" + "l.consensus_paup." + data_prefix
    output =  "--output="+ "l.consensus_paup." + data_prefix + ".%j.out"
    err = "--error=" + "l.consensus_paup." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    if not os.path.exists(os.path.join(res_dir, 'strict_consensus.tre')):
        sp.run(['sbatch', job_name, output, err, sbatch])





def main():


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/paup'

    data_dir =  "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"
    
    paup_exe = os.path.join(software_dir, 'paup4a168_centos64')
    

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    

    # score_pattern = r"small parsimony score = ([\d.]+)"


    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
    
            
          

            
        opt_trees_dir = os.path.join(cur_res_path, 'optimal_trees')
            
        all_opt_trees_file = os.path.join(opt_trees_dir, 'all_paup_opt_trees.newicks')
        data_prefix = folder
        print(data_prefix)

        paup_nex_file = os.path.join(cur_res_path, 'paup_consensus.nex')
        paup_sbatch = os.path.join(cur_res_path, 'run_consensus_paup.sbatch')

        if not os.path.exists(os.path.join(cur_res_path, 'strict_consensus.tre')):
            write_paup_sbatch(cur_res_path, paup_exe, paup_nex_file, paup_sbatch)
            print('Writing sbatch file for ' + cur_res_path)
            submit_paup_sbacth(paup_sbatch, data_prefix, cur_res_path)
            
            
               
if __name__ == '__main__':

    main()