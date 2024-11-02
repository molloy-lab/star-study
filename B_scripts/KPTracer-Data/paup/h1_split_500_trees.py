import os
import subprocess as sp
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('all_paup_trees_path', type=str, help="all_paup_trees_path")
parser.add_argument('opt_trees_dir', type=str, help="opt_trees_dir")
args = parser.parse_args()
all_paup_trees_path = args.all_paup_trees_path
opt_trees_dir = args.opt_trees_dir

score_pattern = r"small parsimony score = ([\d.]+)"

def get_opt_score(score_path):
    with open(score_path, 'r') as file:
        content = file.read().strip()
        decimal_number = Decimal(content).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    return decimal_number


def clean_newick_string(newick_str):
    # Remove all whitespace characters
    cleaned_newick_str = re.sub(r'\s+', '', newick_str)
    
    # Validate the Newick string (basic validation)
    if cleaned_newick_str.count('(') != cleaned_newick_str.count(')'):
        raise ValueError("Invalid Newick string: unmatched parentheses")
    
    if not cleaned_newick_str.endswith(';'):
        raise ValueError("Invalid Newick string: must end with a semicolon ';'")
    
    return cleaned_newick_str

def main():


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/bio_result/paup'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/KPTracer-Data"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

    startle_dir = os.path.join(software_dir, 'startle')

    startle_nni_dir = os.path.join(startle_dir, 'build')
    startle_nni_dir = os.path.join(startle_nni_dir, 'src')

    startle_exe = os.path.join(startle_nni_dir, 'startle')

    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    # folders = [f for f in folders if f.split("-")[0]=='nlin_50' and f.split("-")[1]!='ncas_20']

    # score_pattern = r"small parsimony score = ([\d.]+)"
    
    print(folders)

    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
            
        opt_trees_dir = os.path.join(cur_res_path, 'pruned_optimal_trees')

        if not os.path.exists(opt_trees_dir):
            os.mkdir(opt_trees_dir)
            print(opt_trees_dir)
        else:
            print(f'{opt_trees_dir}: Done!')
            continue
            
        # cmat_path = os.path.join(cur_data_path, folder + '_character_matrix.csv')
        cmat_path = os.path.join(cur_data_path, folder + '_pruned_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv')
        score_path = os.path.join(cur_res_path, 'score.csv')

        score = get_opt_score(score_path)

        # all_paup_trees_path = os.path.join(cur_res_path, 'replaced_paup.trees')
        # all_paup_trees_path = os.path.join(cur_res_path, 'paup_trees.trees')

        all_paup_trees_path = os.path.join(cur_res_path, all_paup_trees_path)

        if not os.path.exists(all_paup_trees_path):
            print(f'missing: {all_paup_trees_path}')
        else:
            with open(all_paup_trees_path, 'r') as file:
                newick_strings = file.read().strip().split('\n')

            
            data_prefix = folder
            print(data_prefix)
            count = 1
            for newick_string in newick_strings:
                    
                cur_tree_file = os.path.join(opt_trees_dir, f'{count}.newick')
                    
                with open(cur_tree_file, 'w') as out_file:
                    out_file.write(clean_newick_string(newick_string))
                    
                score_prefix = os.path.join(opt_trees_dir, 'paup_score')
                score_res = sp.run([startle_exe,'small',cmat_path,priors_path,cur_tree_file,'--output',score_prefix], capture_output=True, text=True)
                    
                if score_res.returncode == 0:
                    score_res = score_res.stdout
                    print(score_res)
                
                    score_res_match = re.search(score_pattern, score_res)
                else:
                    print("%%")
                    print(score_res.stderr)
                    raise Exception("Failed to compute score for " + cur_res_path)
                    
                if score_res_match:
                    cur_tree_score = Decimal(score_res_match.group(1)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                    
                print(f'curent score: {cur_tree_score}, score: {score}')

                if cur_tree_score < score:
                    raise Exception(f"Error current score {cur_tree_score} < {score}")
                elif cur_tree_score > score:
                    os.remove(cur_tree_file)
                    print('current tree is not opt')
                else:
                    print('current tree is opt')
                    count += 1
            print(f'finished: {cur_res_path}')
               
if __name__ == '__main__':

    main()