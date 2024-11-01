import os
import subprocess as sp
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import pandas as pd


def main():
    
    sys.setrecursionlimit(4000)
    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')
    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    
    score_pattern = r"small parsimony score = ([\d.]+)"

    for folder in folders:
        
        cur_data_path = os.path.join(data_dir, folder)
        
      

        cmat_path = os.path.join(cur_data_path, "startle_format_cmat.csv")
            
        priors_path = os.path.join(cur_data_path, 'startle_format_priors.csv')

        score_path = os.path.join(cur_data_path, 'score.csv')
        ilp_tree_path = os.path.join(cur_data_path,'tree.nwk')

        with open(ilp_tree_path, 'r') as tf:
            content = tf.read()
        
        tree_content = content.replace('[&R] ', '')
   
        true_tree_path = os.path.join(cur_data_path, 'true_tree.tre')
        
        with open(true_tree_path, 'w') as ttf:
            ttf.write(tree_content)

        data_prefix = folder
        print(data_prefix)

        if not os.path.exists(score_path) or True:
            score_prefix = os.path.join(cur_data_path, 'true_tree_score')
            score_res = sp.run([startle_exe, 'small', cmat_path, priors_path, true_tree_path, '--output', score_prefix], capture_output=True, text=True)
            
            if score_res.returncode == 0:
                score_res = score_res.stdout
                print(score_res)
                
                score_res_match = re.search(score_pattern, score_res)
            else:
                print("%%")
                print(score_res.stderr)
                raise Exception("Failed to compute score for " + cur_data_path)

            if score_res_match:
                score = Decimal(score_res_match.group(1)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                    # table['true-tree-score-under-est-prior'].append(score)
            
            with open(score_path, 'w', newline="") as score_file:
                score_file.write(f'{score}\n')
                print(f'write {score_path}')
                
            #else:
                #os.remove(score_path)
    # print(table)
    # table_df = pd.DataFrame(table)
    # table_df = table_df.dropna(subset=['true-tree-score-under-est-prior'], how='all')
    # table_df.to_csv(os.path.join(data_dir, 'true_trees_scores.csv'), index=False)

if __name__ == '__main__':

    main()