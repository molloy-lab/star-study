import os
import subprocess as sp
import shutil


def copy_file(tar:str, res: str):
    if not os.path.exists(res) or True:
        shutil.copy(tar, res)
        print(f"copy {tar} into {res}")



data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/star_cdp'
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/star_cdp-sc'

folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
for folder in folders:
    cur_data_path = os.path.join(data_path, folder)
    cur_res_path = os.path.join(result_dir, folder)


    # tar_tree= os.path.join(cur_data_path, 'consensus_star_cdp_strict_consensus.tre')
    # res_tree = os.path.join(cur_res_path, 'consensus_star_cdp_strict_consensus.tre')
    # copy_file(tar_tree, res_tree)
    tar_RF = os.path.join(cur_data_path, 'SC-RFEX.csv')
    res_RF = os.path.join(cur_res_path, 'RFEX.csv')

    copy_file(tar_RF, res_RF)

