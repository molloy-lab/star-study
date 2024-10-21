import os
import sys
import shutil
import re
import subprocess as sp



def write_laml_sbatch(cmat: str, priors: str, sbatch_file: str, start_tree: str, prefix:str):
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
                    'module load Python3/3.9.15',
                    ' '.join([time,'-v','-o','laml_usage.log','run_laml','-c',cmat, '-p', priors,'-t',start_tree, '-o', prefix ,'--nInitials','1',' --topology_search','&>','laml.log','2>&1'])
                    ]

    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))


def submit_laml_sbacth(sbatch: str, data_prefix: str, res_dir:str):
    job_name = "--job-name=" + "c.laml." + data_prefix
    output =  "--output="+ "c.laml." + data_prefix + ".%j.out"
    err = "--error=" + "c.laml." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    if not os.path.exists(os.path.join(res_dir,'star_cdp_one_sol.tre')):
        sp.run(['sbatch', job_name, output, err, sbatch])




data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250'
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/laml'

pattern = re.compile(r's(\d+)d(\d+)p(\d+)_sub250_r(\d+)')

folders = [f for f in os.listdir(result_dir) if os.path.exists(os.path.join(result_dir, f))]

for folder in folders:

    match = pattern.match(folder)

    if match:
        silencing,dropout,prior,rep = match.groups()
        print(folder)
        print(silencing, dropout, prior, rep)
        
        cur_data_path = os.path.join(data_path, folder)
        cur_res_path = os.path.join(result_dir, folder)
    
        cmat_path = os.path.join(cur_data_path, "character_matrix.csv")
            
        priors_path = os.path.join(cur_data_path, f'prior_k30_r{prior}.csv')

        start_tree_path = os.path.join(cur_res_path, 'nni_tree.newick')
        laml_sbatch = os.path.join(cur_res_path, 'run_laml.sbatch')
        data_prefix = folder
        print(data_prefix)
        print(os.path.join(cur_res_path, 'laml'))

        if not os.path.exists(os.path.join(cur_res_path, "laml_output-1_trees.nwk")):
            write_laml_sbatch(cmat_path, priors_path, laml_sbatch, start_tree_path, os.path.join(cur_res_path, 'laml_output-1'))
            print('Writing sbatch file for ' + cur_res_path)
            submit_laml_sbacth(laml_sbatch, data_prefix, cur_res_path)
            print('Submiting  job for ' + cur_res_path)
