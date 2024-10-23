import os
import subprocess as sp



def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/startle_nni_python'


    folders = [f for f in os.listdir(result_dir) if os.path.isdir(os.path.join(result_dir, f))]

    failed_jobs = []
    succes_count = 0
    for folder in folders:
        cur_res_path = os.path.join(result_dir, folder)

        
        reps = [rep for rep in os.listdir(cur_res_path) if os.path.isdir(os.path.join(cur_res_path, rep))]
        
        for rep in reps:
            cur_rep_res_path = os.path.join(cur_res_path, rep)


            sbatch_path = os.path.join(cur_rep_res_path, 'run_nni.sbatch')
            
            tree_path = os.path.join(cur_rep_res_path, 'nni_tree.newick')

            if not os.path.exists(tree_path):
                failed_jobs.append(cur_rep_res_path)
            else:
                succes_count += 1

    print(failed_jobs)
    print(f'# failed = {len(failed_jobs)}')
    print(f'# success = {succes_count}')
                

if __name__ == '__main__':

    main()
