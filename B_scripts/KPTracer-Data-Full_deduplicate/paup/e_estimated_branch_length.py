import os
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
                    'module load Python3/3.8.15',
                    ' '.join([time,'-v','-o',prefix+'_usage.log','run_laml','-c',cmat, '-p', priors,'-t',start_tree, '-o', prefix ,'-v','--nInitials','1','--timescale','6','--resolve_search','--parallel','&>',prefix+'.log','2>&1'])
                    ]

    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))


def submit_laml_sbacth(sbatch: str, data_prefix: str, res_dir:str):
    job_name = "--job-name=" + "e.branch." + data_prefix
    output =  "--output="+ "e.branch." + data_prefix + ".%j.out"
    err = "--error=" + "e.branch." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    # if os.path.exists(os.path.join(res_dir,'removed_outg_star_cdp_sc_strict_consensus.tre')):
        # sp.run(['sbatch', job_name, output, err, sbatch])
    sp.run(['sbatch', job_name, output, err, sbatch])

def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/I_bio_result_Full_deduplicate/paup'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/software"


    # folders = [
    # '3513_NT_T1_Fam',
    # '3515_Lkb1_T1_Fam',
    # '3724_NT_All']

    # folders = ['3724_NT_All'] done
    # folders = ['3515_Lkb1_T1_Fam'] done
    folders = ['3513_NT_T1_Fam']
  
    for folder in folders:
        
        
        sh_contract_folders = os.path.join(result_dir,folder)

        if not os.path.exists(sh_contract_folders):
            continue 
                
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
            
        cmat_path = os.path.join(cur_data_path, folder + '_deduplicated_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv')
        print(priors_path)
            
        one_sol_path = os.path.join(result_dir,folder, 'deduplicated_paup_one_sol_trees.nwk')
            
        one_sh_path = os.path.join(result_dir, folder, 'deduplicated_paup_one_sol_sh_trees.nwk')


        sc_path = os.path.join(result_dir, folder, 'deduplicated_paup_sc_trees.nwk')
            
        sc_sh_path = os.path.join(result_dir,folder, 'deduplicated_paup_sc_sh_trees.nwk')


        trees = [one_sol_path, one_sh_path,sc_path, sc_sh_path]

        
        for sh_tree in trees:
            method_name = sh_tree[sh_tree.find('paup_') + 5:-10]
            print(method_name)
            output_prefix = method_name + '_branch_resolve_poly'
            print(output_prefix)

            laml_sbatch = os.path.join(sh_contract_folders, 'run_laml-branch.sbatch')
            data_prefix = sh_tree + "/"
            print(data_prefix)
            write_laml_sbatch(cmat_path, priors_path, laml_sbatch, os.path.join(sh_contract_folders, sh_tree), os.path.join(sh_contract_folders,output_prefix))
            print('Writing sbatch file for ' + sh_contract_folders)
            submit_laml_sbacth(laml_sbatch, data_prefix, sh_contract_folders)
            print('Submiting  job for ' + sh_contract_folders)
                
            

if __name__ == '__main__':

    main()