import os
import subprocess as sp
import shutil


def copy_file(tar:str, res: str):
    if not os.path.exists(res) or True:
        shutil.copy(tar, res)
        print(f"copy {tar} into {res}")



data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/paup'
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/paup-sc'

folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
for folder in folders:
    cur_data_path = os.path.join(data_path, folder)
   
    cur_res_path = os.path.join(result_dir, folder)

    # tar_tree= os.path.join(cur_data_path, 'strict_consensus.tre')
    # res_tree = os.path.join(cur_res_path, 'strict_consensus.tre')
    # copy_file(tar_tree, res_tree)
    tar_RF = os.path.join(cur_data_path, 'SC-RFSH.csv')
    res_RF = os.path.join(cur_res_path, 'RFSH.csv')

    copy_file(tar_RF, res_RF)

