import os
import subprocess as sp
import shutil

def main():
    
    data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle_data_in_startle'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/cassiopeia_greedy'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/paup'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/star_cdp'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/startle_nni'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/startle_ilp'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/star_cdp-sc'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/laml'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/startle_nni_python'
    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/star_cdp-rand'
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    
    # paup_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result/paup'

    folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
    # folders = [f for f in folders if f.split("_")[1]=='50-ncas']
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