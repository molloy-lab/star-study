import os
import subprocess as sp
import re
import dendropy
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

def main():
    sys.setrecursionlimit(4000)

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/cassiopeia-greedy'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle_data_in_startle"
    
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
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        
        reps = [rep for rep in os.listdir(cur_data_path) if os.path.isdir(os.path.join(cur_data_path, rep))]
        
        avg_score = Decimal(0)
        num_reps = len(reps)
        print(reps)
        for rep in reps:
            cur_res_rep_path = os.path.join(cur_res_path, rep)
            if not os.path.exists(cur_res_rep_path):
                os.mkdir(cur_res_rep_path)
            
            cur_rep_data_path = os.path.join(cur_data_path, rep)

            cmat_path = os.path.join(cur_rep_data_path,next(\
            (file for file in os.listdir(cur_rep_data_path) if file.endswith('_character_matrix.csv')), None))
            
            priors_path = os.path.join(cur_rep_data_path,next(\
            (file for file in os.listdir(cur_rep_data_path) if file.endswith('_mutation_prior.csv')), None))
            
            score_path = os.path.join(cur_res_rep_path, 'score.csv')
            star_cdp_tree_path = os.path.join(cur_res_rep_path, 'cassiopeia_greedy.tre')
            data_prefix = folder + "/"+rep
            print(data_prefix)

            if not os.path.exists(score_path) or True:
                score_prefix = os.path.join(cur_res_rep_path, 'Cassiopeia_Greedy_score')
                score_res = sp.run([startle_exe, 'small', cmat_path, priors_path, star_cdp_tree_path, '--output', score_prefix], capture_output=True, text=True)
            
                if score_res.returncode == 0:
                    score_res = score_res.stdout
                    print(score_res)
                
                    score_res_match = re.search(score_pattern, score_res)
                else:
                    print("%%")
                    print(score_res.stderr)
                    raise Exception("Failed to compute score for " + cur_res_rep_path)

                if score_res_match:
                    score = Decimal(score_res_match.group(1)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                   
                    avg_score += score
            
                with open(score_path, 'w', newline="") as score_file:
                    score_file.write(f'{score}\n')
                    print(f'write {score_path}')
            #else:
                #os.remove(score_path)
            
        avg_score = avg_score / num_reps

        avg_score_file = os.path.join(cur_res_path, 'avg_score.csv')
        with open(avg_score_file, 'w', newline="") as avgf:
            avgf.write(f'{avg_score}\n')
            print((f'write {avg_score_file}'))

if __name__ == '__main__':

    main()