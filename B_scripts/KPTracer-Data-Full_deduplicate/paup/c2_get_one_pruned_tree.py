import os
import subprocess as sp
import re
import sys

def main():


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/I_bio_result_Full_deduplicate/paup'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

    folders = ['3515_Lkb1_T1_Fam']
    
    score_pattern = r"small parsimony score = ([\d.]+)"

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        

        all_paup_trees_path = os.path.join(cur_res_path, 'paup_trees.trees')

            
        data_prefix = folder
        print(data_prefix)

        if not os.path.exists(all_paup_trees_path):
            print(f'missing: {all_paup_trees_path}')
        else:
            one_nwk = ""
            with open(all_paup_trees_path, 'r') as aptp:
                for line in aptp:
                    one_nwk += line.strip()

                    if one_nwk.endswith(';'):
                        break

            
            one_nwk_file = os.path.join(cur_res_path, 'deduplicated_paup_one_sol_trees.nwk')

            with open(one_nwk_file, 'w') as onf:
                onf.write(one_nwk)

            # os.remove(one_nwk_file)
                
            #else:
                #os.remove(score_path)
if __name__ == '__main__':

    main()