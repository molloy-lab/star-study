import os
import subprocess as sp



def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/cassiopeia_greedy'


    folders = [f for f in os.listdir(result_dir) if os.path.isdir(os.path.join(result_dir, f))]

    failed_jobs = []
    succes_count = 0
    for folder in folders:
        cur_res_path = os.path.join(result_dir, folder)

        cur_rep_res_path = os.path.join(cur_res_path)

        sbatch_path = os.path.join(cur_rep_res_path, 'cassiopeia_greedy.sbatch')
            
        tree_path = os.path.join(cur_rep_res_path, 'cassiopeia_greedy.tre')

        if not os.path.exists(tree_path):
            failed_jobs.append(cur_rep_res_path)
        else:
            succes_count += 1

    print(failed_jobs)
    print(f'# failed = {len(failed_jobs)}')
    print(f'# success = {succes_count}')
                

if __name__ == '__main__':

    main()
