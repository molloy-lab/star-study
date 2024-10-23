import os
import subprocess as sp




def write_nni_sbatch(startle_exe: str, cmat: str, priors: str, sbatch_file: str, start_tree: str):
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
                    ' '.join([time,'-v','-o',\
                    'nni_usage.log',\
                    'python3',\
                    startle_exe,\
                    '-m',priors, \
                    '--iterations','\
                    250',\
                    '--mode',\
                    'infer',\
                    '--threads',\
                    '16',\
                    '--output', \
                    'nni_tree.newick',\
                    start_tree,cmat,\
                    '&>','nni.log','2>&1'])
                    ]

    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))


def submit_nni_sbacth(sbatch: str, data_prefix: str, res_dir:str):
    job_name = "--job-name=" + "s100.nni." + data_prefix
    output =  "--output="+ "s100.nni." + data_prefix + ".%j.out"
    err = "--error=" + "s100.nni." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    if not os.path.exists(os.path.join(res_dir, "nni_tree.newick")):
        sp.run(['sbatch', job_name, output, err, sbatch])

def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/startle_nni_python'
    cplusplus_result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/startle_nni'
    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/software/Python-Startle"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_nni_dir = os.path.join(startle_dir, 'src', 'nni')

    startle_exe = os.path.join(startle_nni_dir, 'startle.py')

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    folders = [f for f in folders if f.startswith('s100')]
    print(folders)
    print(len(folders))
    #exit(0)
    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        cur_cplusplus_result_dir = os.path.join(cplusplus_result_dir, folder)
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        
            
       
        cmat_path = os.path.join(cur_data_path, "startle_format_cmat.csv")
            
        priors_path = os.path.join(cur_data_path, 'startle_format_priors.csv')

            
        nj_tree_path = os.path.join(cur_cplusplus_result_dir, 'nj.newick')
        nni_sbatch = os.path.join(cur_res_path, 'run_nni.sbatch')
        data_prefix = folder
        print(data_prefix)
        if not os.path.exists(nj_tree_path):
            print(f"Failed to find starting tree: {nj_tree_path}")

        if not os.path.exists(os.path.join(cur_res_path, "nni_tree.newick")):
            write_nni_sbatch(startle_exe, cmat_path, priors_path, nni_sbatch, nj_tree_path)
            print('Writing sbatch file for ' + cur_res_path)
            submit_nni_sbacth(nni_sbatch, data_prefix, cur_res_path)
            print('Submiting nj job for ' + cur_res_path)
                
            

if __name__ == '__main__':

    main()