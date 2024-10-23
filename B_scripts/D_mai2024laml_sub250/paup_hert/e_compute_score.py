import os
import subprocess as sp
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction



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


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/paup'

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
        cur_res_path = os.path.join(result_dir, folder)
            
      
        cmat_path = os.path.join(cur_data_path, "startle_format_cmat.csv")
            
        priors_path = os.path.join(cur_data_path, 'startle_format_priors.csv')
            
        score_path = os.path.join(cur_res_path, 'score.csv')

        all_paup_trees_path = os.path.join(cur_res_path, 'paup_trees.trees')

            
            


        data_prefix = folder
        print(data_prefix)

        if not os.path.exists(all_paup_trees_path):
            print(f'missing: {all_paup_trees_path}')
        else:
            if not os.path.exists(all_paup_trees_path):
                print(f'missing: {all_paup_trees_path}')
            else:
                score = float('inf')

                with open(all_paup_trees_path, 'r') as file:
                    newick_strings = file.read().strip().split('\n')
                        
                    for newick_string in newick_strings:
                        cur_tree_file = os.path.join(cur_res_path, 'one_nwk.newick')
                        with open(cur_tree_file, 'w') as out_file:
                            out_file.write(clean_newick_string(newick_string))
                                
                        if not os.path.exists(score_path) or True:
                            score_prefix = os.path.join(cur_res_path, 'paup_score')
                            score_res = sp.run([startle_exe, 'small', cmat_path, priors_path, cur_tree_file, '--output', score_prefix], capture_output=True, text=True)
                            if score_res.returncode == 0:
                                score_res = score_res.stdout
                                print(score_res)
                                score_res_match = re.search(score_pattern, score_res)
                            else:
                                print("%%")
                                print(score_res.stderr)
                                raise Exception("Failed to compute score for " + cur_res_path)

                            if score_res_match:
                                cur_score = Decimal(score_res_match.group(1)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                                    
                                score = min(cur_score, score)
                        break
            
                with open(score_path, 'w', newline="") as score_file:
                    score_file.write(f'{score}\n')
                    print(f'write {score_path}')

                
            #else:
                #os.remove(score_path)
                
if __name__ == '__main__':

    main()