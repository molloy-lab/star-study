import os
import subprocess as sp
import pandas as pd 
import numpy as np



def write_nni_sbatch(startle_exe: str, cmat: str, priors: str, sbatch_file: str, start_tree: str):
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
                    ' '.join([time,'-v','-o','nni_usage.log',startle_exe,'large',cmat,priors, start_tree, '--output', 'nni',\
                    '&>','nni.log','2>&1'])
                    ]

    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))


def submit_nni_sbacth(sbatch: str, data_prefix: str, res_dir:str):
    job_name = "--job-name=" + "c.nni." + data_prefix
    output =  "--output="+ "c.nni." + data_prefix + ".%j.out"
    err = "--error=" + "c.nni." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    if not os.path.exists(os.path.join(res_dir, "nni_tree.newick")):
        sp.run(['sbatch', job_name, output, err, sbatch])
        print('Submiting nni job for ' + res_dir)
        return 1
    return 0


def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/I_bio_result_Full_deduplicate/startle_nni'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')
    
    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

    folders = ['3515_Lkb1_T1_Fam']

    count = 0
    
    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
            
        cmat_path = os.path.join(cur_data_path, folder + '_deduplicated_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv')
        nj_tree_path = os.path.join(cur_res_path, 'nj.newick')

        nni_sbatch = os.path.join(cur_res_path, 'run_nni.sbatch')
        # print(nni_sbatch)
        # print(cmat_path)
        # print(nj_tree_path)
        # exit(0)

        if not os.path.exists(nj_tree_path):
                print(f"Failed to find starting tree: {nj_tree_path}")
                continue

        data_prefix = folder 
        print(data_prefix)

        if not os.path.exists(os.path.join(cur_res_path, "nni_tree.newick")):
            write_nni_sbatch(startle_exe, cmat_path, priors_path, nni_sbatch, nj_tree_path)
            print('Writing sbatch file for ' + cur_res_path)
            count += submit_nni_sbacth(nni_sbatch, data_prefix, cur_res_path)
            print('Submiting nj job for ' + cur_res_path)

    print(f'total folders:{len(folders)}, submit jobs: {count}')        

if __name__ == '__main__':

    main()