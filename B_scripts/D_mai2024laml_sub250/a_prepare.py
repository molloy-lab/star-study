import os
import subprocess as sp
import shutil

def main():
    
    data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250'
    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/paup'
    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/star_cdp'
    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/startle_nni'
    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/startle_ilp'
    
    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/laml'

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/star_cdp-sc'
    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/paup-sc'

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/star_cdp_hert'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/star_cdp_hert-sc'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/paup_hert'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/cassiopeia_greedy'
    # result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/star_cdp-rand'
    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/startle_nni_python'
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    
    # paup_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result/paup'

    folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
    folders = [f for f in folders if f not in ['model_tree.txt', 'summary_stats.txt', 'true_missing_stats.txt']]

    # folders = [f for f in folders if f.split("_")[1]=='50-ncas']
    print(folders)
    for folder in folders:
        
        # cur_paup_path = os.path.join(paup_dir, folder)
        cur_data_path = os.path.join(data_path, folder)
        cur_res_path = os.path.join(result_dir, folder)

        print(cur_res_path)
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)            

if __name__ == '__main__':

    main()