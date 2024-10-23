import os
import subprocess as sp



def main():
    

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/startle_ilp'


    folders = [f for f in os.listdir(result_dir) if os.path.isdir(os.path.join(result_dir, f))]

    ran_jobs = []
    error_files = []
    for folder in folders:
        cur_res_path = os.path.join(result_dir, folder)

        print(cur_res_path)

        sbatch_path = os.path.join(cur_res_path, 'run_ilp.sbatch')
            
        tree_folder = os.path.join(cur_res_path, 'output')

        if not os.path.exists(tree_folder):
            print('no: ' + tree_folder)
            continue
        
        if os.listdir(tree_folder):
            ran_jobs.append(cur_res_path)
            for fil in os.listdir(cur_res_path):
                if (fil.endswith('.err')):
                    error_files.append(os.path.join(cur_res_path, fil))



    print(ran_jobs)
    print(len(ran_jobs))
    print(error_files)
    print(len(error_files))
    for error_file in error_files:
        with open(error_file, 'r') as ef:
            content = ef.read()
            print(content)

                

if __name__ == '__main__':

    main()
