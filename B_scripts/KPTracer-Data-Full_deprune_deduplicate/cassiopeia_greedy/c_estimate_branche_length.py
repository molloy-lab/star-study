import os
import subprocess as sp


def write_laml_sbatch(cmat: str, priors: str, sbatch_file: str, start_tree: str, prefix:str):
    time="/usr/bin/time"
    rows_to_wrtie = ['#!/bin/bash', 
                     '#SBATCH --time=24:00:00', 
                     '#SBATCH --cpus-per-task=1', 
                     '#SBATCH --ntasks=16',
                    '#SBATCH --mem=48G',
                    '#SBATCH --qos=highmem',
                    '#SBATCH --partition=cbcb',
                    '#SBATCH --account=cbcb',
                    '#SBATCH --constraint=EPYC-7313',
                    '#SBATCH --exclusive',
                    'module load Python3/3.8.15',
                    # ' '.join([time,'-v','-o','one_sol_branch_usage.log','run_laml','-c',cmat, '-p', priors,'-t',start_tree, '-o', prefix ,'-v','--nInitials','1','--timescale','6','&>','one_sol_branch.log','2>&1'])
                    ' '.join([time,'-v','-o','one_sol_branch_sh_usage.log','run_laml','-c',cmat, '-p', priors,'-t',start_tree, '-o', prefix ,'-v','--nInitials','1','--timescale','6','--resolve_search','--parallel','&>','one_sol_branch_sh.log','2>&1'])
                    ]

    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))


def submit_laml_sbacth(sbatch: str, data_prefix: str, res_dir:str):
    job_name = "--job-name=" + "e.laml-cdp-branch." + data_prefix
    output =  "--output="+ "e.laml-cdp-branch." + data_prefix + ".%j.out"
    err = "--error=" + "e.laml-cdp-branch." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    # if os.path.exists(os.path.join(res_dir,'star_cdp_one_sol_deduplicate.tre')):
    if os.path.exists(os.path.join(res_dir,'cassiopeia_greedy_deduplicate_contract_sh.tre')):
        sp.run(['sbatch', job_name, output, err, sbatch])

def main():
    
    anatomical_site_map = {
    '3513_NT_T1_Fam':'3513_NT_T1',
    '3724_NT_All':'3724_NT_T1'}

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/G_bio_result_pruned_deduplicate/cassiopeia_greedy'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/software"


    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        
            
        cmat_path = os.path.join(cur_data_path, folder + '_deduplicated_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv')
        print(priors_path)
            

        # laml_sbatch = os.path.join(cur_res_path, 'run_one_sol_branch.sbatch')
        laml_sbatch = os.path.join(cur_res_path, 'run_one_sol_branch_sh.sbatch')

        data_prefix = folder + "/"
        print(data_prefix)

            #need to change remind! star_cdp_one_sol.tre
        if os.path.exists(os.path.join(cur_res_path, "cassiopeia_greedy_deduplicate_contract_sh.tre")):
            # write_laml_sbatch(cmat_path, priors_path, laml_sbatch, os.path.join(cur_res_path, "cassiopeia_greedy_deduplicate_contract_sh.tre"), os.path.join(cur_res_path,'one_sol_sh_branch_resolve_poly'))
            write_laml_sbatch(cmat_path, priors_path, laml_sbatch, os.path.join(cur_res_path, "cassiopeia_greedy_deduplicate.tre"), os.path.join(cur_res_path,'one_sol_branch_resolve_poly'))
          
            print('Writing sbatch file for ' + cur_res_path)
            submit_laml_sbacth(laml_sbatch, data_prefix, cur_res_path)
            print('Submiting  job for ' + cur_res_path)
                
             

if __name__ == '__main__':

    main()