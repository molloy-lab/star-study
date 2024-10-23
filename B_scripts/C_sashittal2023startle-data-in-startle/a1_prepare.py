import os
import subprocess as sp
import shutil

def main():
    
    data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle_data_in_startle'
    

    result_dirs = [os.path.join('/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/', x) for x in ['cassiopeia_greedy', 'paup', 'star_cdp', 'startle_nni', 'startle_ilp', 'laml', 'startle_nni_python']]
    
    for result_dir in result_dirs:

        if not os.path.exists(result_dir):
            os.mkdir(result_dir)
    
    

        folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
    
        print(folders)
        for folder in folders:
            print(folder)
        
            # cur_paup_path = os.path.join(paup_dir, folder)
            cur_data_path = os.path.join(data_path, folder)
            cur_res_path = os.path.join(result_dir, folder)

            print(cur_res_path)
            if not os.path.exists(cur_res_path):
                os.mkdir(cur_res_path)
        
            reps = [rep for rep in os.listdir(cur_data_path) if os.path.isdir(os.path.join(cur_data_path, rep))]
            print(reps)

            for rep in reps:
                cur_res_rep_path = os.path.join(cur_res_path, rep)
                if not os.path.exists(cur_res_rep_path):
                    os.mkdir(cur_res_rep_path)
        

                
            

if __name__ == '__main__':

    main()