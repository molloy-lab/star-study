import os
import subprocess as sp
import pandas as pd 
import numpy as np

def write_nj_sbatch(curr_dir: str, nj_exe: str, cmat: str, sbatch_file: str):

    nj_tree_file = os.path.join(curr_dir, "nj.newick")
    time="/usr/bin/time"

    rows_to_wrtie = ['#!/bin/bash', 
                     '#SBATCH --time=6:00:00', 
                     '#SBATCH --cpus-per-task=1', 
                     '#SBATCH --ntasks=1',
                    '#SBATCH --mem=48G',
                    '#SBATCH --qos=highmem',
                    '#SBATCH --partition=cbcb',
                    '#SBATCH --account=cbcb',
                    '#SBATCH --constraint=EPYC-7313',
                    '#SBATCH --exclusive',
                    'module load Python3/3.8.15',
                    
                    time+ ' -v -o nj_usage.log' + ' python3 ' + nj_exe + ' ' + cmat + ' ' + '--output' + ' '+ nj_tree_file +\
                    " &> " + " nj.log " + " 2>&1 "
                    ]
    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))

def submit_nj_sbatch(data_prefix: str, nj_sbatch: str, res_dir: str):
    job_name = "--job-name=" + "a.nj." + data_prefix
    output =  "--output="+ "a.nj." + data_prefix + ".%j.out"
    err = "--error=" + "a._nj." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    if not os.path.exists(os.path.join(res_dir, 'nj.newick')):
        sp.run(['sbatch', job_name, output, err, nj_sbatch])
        print('Submiting nj job for ' + res_dir)
        return 1
    return 0
def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/startle_nni'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_nj_dir = os.path.join(startle_dir, 'scripts')

    startle_nj_exe = os.path.join(startle_nj_dir, 'nj.py')

    old_folders = [f for f in os.listdir(result_dir) if os.path.isdir(os.path.join(result_dir, f))]

    data_df = pd.read_csv('../cells_number.csv')
    sorted_df = data_df.sort_values(by='rest_cell_num')
    folders = sorted_df['data'].values
    folders = folders.tolist()
    # print(len(folders))

    # for f in old_folders:
    #     if f not in folders:
    #         print(f)
    folders.remove('3724_NT_All')
    print(len(folders))
    exit(0)
    count = 0
    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
            
        cmat_path = os.path.join(cur_data_path, folder + '_pruned_character_matrix.csv')
        
        nj_tree_path = os.path.join(cur_res_path, 'nj.newick')
        nj_sbatch = os.path.join(cur_res_path, 'run_nj.sbatch')
        
        data_prefix = folder 
        print(data_prefix)
        print(cmat_path)
        print(nj_tree_path)
        print(nj_sbatch)

        if not os.path.exists(nj_tree_path):
            write_nj_sbatch(cur_res_path, startle_nj_exe, cmat_path, nj_sbatch)
            print('Writing sbatch file for ' + cur_res_path)
            count += submit_nj_sbatch(data_prefix, nj_sbatch,cur_res_path)
    print(f'total folders:{len(folders)}, submit jobs: {count}')
            

if __name__ == '__main__':

    main()