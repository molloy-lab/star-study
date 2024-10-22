import os
import subprocess as sp




def write_paup_sbatch(curr_dir : str, exe: str, sbatch_file:str,cmat:str,priors:str):
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
                    # 'module load python3/3.9.15',
                    ' '.join([time, '-v', '-o', 'cassiopeia_greedy_usage.log', 'python3', exe,'-i',cmat, '-m', priors, '-o', 'cassiopeia_greedy.tre', '--method', '1', '&>', 'cassiopeia_greedy.log', '2>&1'])
                    ]

    with open(sbatch_file, 'w') as sf:
        sf.write("\n".join(rows_to_wrtie))



def submit_paup_sbacth(sbatch: str, data_prefix: str, res_dir:str):
    job_name = "--job-name=" + "a.cassiopeia_greedy." + data_prefix
    output =  "--output="+ "a.cassiopeia_greedy." + data_prefix + ".%j.out"
    err = "--error=" + "a.cassiopeia_greedy." + data_prefix + ".%j.err"
    os.chdir(res_dir)
    if not os.path.exists(os.path.join(res_dir, 'all_trees.trees')):
        sp.run(['sbatch', job_name, output, err, sbatch])



def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/cassiopeia-greedy'
    
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle_used_in_startle"
    exe = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/scripts/KPTracer-Data/cassiopeia-greedy/run_cassiopeia.py"
    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)

        
        reps = [rep for rep in os.listdir(cur_data_path) if os.path.isdir(os.path.join(cur_data_path, rep))]
        
        for rep in reps:
            cur_rep_res_path = os.path.join(cur_res_path, rep)
            cur_rep_data_path = os.path.join(cur_data_path, rep)


            # cmat_path = os.path.join(cur_rep_data_path, folder + '_character_matrix.csv')
            cmat_path = os.path.join(cur_rep_data_path,next(\
            (file for file in os.listdir(cur_rep_data_path) if file.endswith('_character_matrix.csv')), None))
            
            priors_path = os.path.join(cur_rep_data_path,next(\
            (file for file in os.listdir(cur_rep_data_path) if file.endswith('_mutation_prior.csv')), None))


            data_prefix = folder + "_seed_" + rep

            sbtach_file = os.path.join(cur_rep_res_path, 'run_cassiopeia_greedy.sbatch')
            
            if not os.path.exists(os.path.join(cur_rep_res_path, "cassiopeia_greedy.tre")):
                write_paup_sbatch(cur_rep_res_path, exe, sbtach_file,cmat_path, priors_path)
                print('Writing sbatch file for ' + cur_rep_res_path)
                submit_paup_sbacth(sbtach_file, data_prefix, cur_rep_res_path)
                print('Submiting job for ' + cur_rep_res_path)
                

if __name__ == '__main__':

    main()
