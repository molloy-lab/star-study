import os
import subprocess as sp




def write_star_cdp_sbatch(exe: str, cmat: str, priors: str, sbatch_file: str, search_space: str):
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
                    ' '.join([time,'-v','-o','consensus_star_cdp_usage.log',exe,'-i',cmat, '-m', priors, '-x OUTG','-t',search_space, '-HERT','-consensus','--output', 'star_cdp', '-o','consensus_star_cdp','-XOUTG',\
                    '&>','consensus_star_cdp.log','2>&1'])
                    ]

    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))


def submit_star_cdp_sbacth(sbatch: str, data_prefix: str, res_dir:str):
    job_name = "--job-name=" + "c.consensus_star_cdp." + data_prefix
    output =  "--output="+ "c.consensus_star_cdp." + data_prefix + ".%j.out"
    err = "--error=" + "c.consensus_star_cdp." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    if not os.path.exists(os.path.join(res_dir,'consensus_star_cdp_one_sol.tre')) or True:
        sp.run(['sbatch', job_name, output, err, sbatch])

def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/star_cdp_hert'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/software"

    star_cdp_exe = os.path.join(software_dir, 'star-cdp')

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)


    
            
       
        cmat_path = os.path.join(cur_data_path, "startle_format_cmat.csv")
            
        priors_path = os.path.join(cur_data_path, 'startle_format_priors.csv')
            
        search_space = os.path.join(cur_res_path, 'search_space.trees')
        star_cdp_sbatch = os.path.join(cur_res_path, 'run_star_cdp_consensus.sbatch')
        data_prefix = folder
        print(data_prefix)

            #need to change remind! star_cdp_one_sol.tre
        if not os.path.exists(os.path.join(cur_res_path, "consensus_star_cdp_one_sol.tre")):
            write_star_cdp_sbatch(star_cdp_exe, cmat_path, priors_path, star_cdp_sbatch, search_space)
            print('Writing sbatch file for ' + cur_res_path)
            submit_star_cdp_sbacth(star_cdp_sbatch, data_prefix, cur_res_path)
            print('Submiting  job for ' + cur_res_path)
                
            

if __name__ == '__main__':

    main()