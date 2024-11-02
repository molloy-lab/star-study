import os
import subprocess as sp
import re
import dendropy
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

def main():
    sys.setrecursionlimit(4000)

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/F_bio_result_deduplicate/laml'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]


    
    score_pattern = r"small parsimony score = ([\d.]+)"

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        

        sh_contract_folders = os.path.join(cur_res_path, 'sh_contract')

        sh_trees = [f for f in os.listdir(sh_contract_folders) if os.path.exists(os.path.join(sh_contract_folders, f))]


        # cmat_path = os.path.join(cur_data_path, folder + '_deduplicated_character_matrix.csv')
        cmat_path = os.path.join(cur_data_path, folder + '_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv') 
            
        for sh_tree in sh_trees:
            if not sh_tree.endswith(".nwk"):
                continue
            method_name = sh_tree[:-17]

            output_prefix = method_name + '_branch'
        
            score_path = os.path.join(sh_contract_folders, output_prefix+'-score.csv')
            star_cdp_tree_path = os.path.join(sh_contract_folders, sh_tree)
            data_prefix = folder
            print(data_prefix)


            if not os.path.exists(score_path) or True:
                score_prefix = os.path.join(sh_contract_folders, 'star_cdp_score')
                score_res = sp.run([startle_exe, 'small', cmat_path, priors_path, star_cdp_tree_path, '--output', score_prefix], capture_output=True, text=True)
            
                if score_res.returncode == 0:
                    score_res = score_res.stdout
                    print(score_res)
                
                    score_res_match = re.search(score_pattern, score_res)
                else:
                    print("%%")
                    print(score_res.stderr)
                    raise Exception("Failed to compute score for " + sh_contract_folders + ' ' + sh_tree)

                if score_res_match:
                    score = Decimal(score_res_match.group(1)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                   
                   
            
                with open(score_path, 'w', newline="") as score_file:
                    score_file.write(f'{score}\n')
                    print(f'write {score_path}')
            #else:
                #os.remove(score_path)

if __name__ == '__main__':

    main()