import os
import sys
import shutil
import re
import subprocess as sp



def write_laml_sbatch(cmat: str, priors: str, sbatch_file: str, start_tree: str, prefix:str):
    time="/usr/bin/time"
    rows_to_wrtie = ['#!/bin/bash', 
                     '#SBATCH --time=24:00:00', 
                     '#SBATCH --cpus-per-task=16', 
                     '#SBATCH --ntasks=1',
                    '#SBATCH --mem=48G',
                    '#SBATCH --qos=highmem',
                    '#SBATCH --partition=cbcb',
                    '#SBATCH --account=cbcb',
                    '#SBATCH --constraint=EPYC-7313',
                    '#SBATCH --exclusive',
                    'module load Python3/3.9.15',
                    ' '.join([time,'-v','-o','laml_output_usage.log','run_laml','-c',cmat, '-p', priors,'-t',start_tree, '-o', prefix ,'-v','--nInitials','1','--topology_search','--maxIters','2500','--parallel','--timescale','6','&>','laml_output.log','2>&1'])
                    ]

    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))


def submit_laml_sbacth(sbatch: str, data_prefix: str, res_dir:str):
    job_name = "--job-name=" + "d." + data_prefix
    output =  "--output="+ "d." + data_prefix + ".%j.out"
    err = "--error=" + "d." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    if not os.path.exists(os.path.join(res_dir,'one_sol_trees.nwk')):
        sp.run(['sbatch', job_name, output, err, sbatch])
        print('Submiting  job for ' + cur_res_path)
        return 1
    return 0




data_path = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full"

all_result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full'

result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/laml'

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

methods = ['paup_one_sol', 'paup_sc', 'star_cdp_one_sol', 'star_cdp_rand_sol', 'star_cdp_sc', 'startle_nni']
count = 0
for method in methods:
    for folder in folders:
      
        cur_res_path = os.path.join(result_dir,method, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)

        cur_data_path = os.path.join(data_path, folder)

        start_tree_prefix = 'startle_nni'

        if method.startswith('paup'):
            start_tree_prefix ='paup'

        elif method.startswith('star_cdp'):
            start_tree_prefix ='star_cdp'

        start_tree_path = os.path.join(all_result_dir,start_tree_prefix, folder, 'deduplicate.tre')


        if method != 'startle_nni':
            prefix = 'deduplicated_' + method + '_trees.nwk'
            start_tree_path =  os.path.join(all_result_dir,start_tree_prefix, folder, prefix)

        cmat_path = os.path.join(cur_data_path, folder + '_deduplicated_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv') 

        laml_sbatch = os.path.join(cur_res_path, 'run_laml.sbatch')

        data_prefix = method + '/' + method + '/' + folder

        if os.path.exists(start_tree_path):
            write_laml_sbatch(cmat_path, priors_path, laml_sbatch, start_tree_path, os.path.join(cur_res_path, 'one_sol'))
            print('Writing sbatch file for ' + cur_res_path)
            count += submit_laml_sbacth(laml_sbatch, data_prefix, cur_res_path)
            
print(f'tot: {len(methods)*len(folders)}, submit: {count}')
    
