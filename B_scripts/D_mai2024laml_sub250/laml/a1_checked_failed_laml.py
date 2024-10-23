import os
import subprocess as sp



def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/laml'


    folders = [f for f in os.listdir(result_dir) if os.path.isdir(os.path.join(result_dir, f))]

    failed_jobs = []
    succes_count = 0
    for folder in folders:
        cur_res_path = os.path.join(result_dir, folder)

        
      
        sbatch_path = os.path.join(cur_res_path, 'run_laml.sbatch')
            
        tree_path = os.path.join(cur_res_path, 'laml_output-1_trees.nwk')

        if not os.path.exists(tree_path):
            failed_jobs.append(cur_res_path)
        else:
            succes_count += 1

    print(failed_jobs)
    print(f'# failed = {len(failed_jobs)}')
    print(f'# success = {succes_count}')
                

if __name__ == '__main__':

    main()
