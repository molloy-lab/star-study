import os
import subprocess as sp
import shutil


def copy_file(tar:str, res: str):
    if not os.path.exists(res):
        shutil.copy(tar, res)
        print(f"copy {tar} into {res}")



data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/paup'
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/paup-sc'

folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
for folder in folders:
    cur_data_path = os.path.join(data_path, folder)
    reps = [rep for rep in os.listdir(cur_data_path) if os.path.isdir(os.path.join(cur_data_path, rep))]
    cur_res_path = os.path.join(result_dir, folder)
    for rep in reps:
        cur_res_rep_path = os.path.join(cur_res_path, rep)
        cur_data_rep_path = os.path.join(cur_data_path, rep)
        # tar_tree= os.path.join(cur_data_rep_path, 'strict_consensus.tre')
        # res_tree = os.path.join(cur_res_rep_path, 'strict_consensus.tre')
        # copy_file(tar_tree, res_tree)

        # tar_RF = os.path.join(cur_data_rep_path, 'SC-RF0.csv')
        # res_RF = os.path.join(cur_res_rep_path, 'RF0.csv')

        tar_RF = os.path.join(cur_data_rep_path, 'SC-RFSH.csv')
        res_RF = os.path.join(cur_res_rep_path, 'RFSH.csv')

        copy_file(tar_RF, res_RF)

