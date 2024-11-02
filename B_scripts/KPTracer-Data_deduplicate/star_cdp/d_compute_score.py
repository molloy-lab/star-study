import os
import subprocess as sp
import re
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('tree_path', type=str, help="tree_path")
parser.add_argument('score_path', type=str, help="score_path")

args = parser.parse_args()
tree_path = args.tree_path
score_path = args.score_path

def main():


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/F_bio_result_deduplicate/star_cdp'

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
        
        if not os.path.exists(cur_res_path):
            os.mkdir(cur_res_path)
        

            
        # cmat_path = os.path.join(cur_data_path, folder + '_deduplicated_character_matrix.csv')
        cmat_path = os.path.join(cur_data_path, folder + '_character_matrix.csv')
        priors_path = os.path.join(cur_data_path, folder + '_priors.csv')
        # score_path = os.path.join(cur_res_path, 'sc_score.csv')
        score_path = os.path.join(cur_res_path, score_path)

        # replaced_tree_path = os.path.join(cur_res_path, 'removed_outg_star_cdp_sc_strict_consensus.tre')   
        replaced_tree_path = os.path.join(cur_res_path, tree_path)    

        data_prefix = folder
        print(data_prefix)

        if not os.path.exists(replaced_tree_path):
            print(f'missing: {replaced_tree_path}')
        else:
            if not os.path.exists(score_path) or True:
                score_prefix = os.path.join(cur_res_path, 'paup_score')
                score_res = sp.run([startle_exe, 'small', cmat_path, priors_path, replaced_tree_path, '--output', score_prefix], capture_output=True, text=True)
            
                if score_res.returncode == 0:
                    score_res = score_res.stdout
                    print(score_res)
                
                    score_res_match = re.search(score_pattern, score_res)
                else:
                    print("%%")
                    print(score_res.stderr)
                    raise Exception("Failed to compute score for " + cur_res_path)

                if score_res_match:
                    score = float(score_res_match.group(1))
            
                with open(score_path, 'w', newline="") as score_file:
                    score_file.write(f'{score}\n')
                    print(f'write {score_path}')

            # os.remove(one_nwk_file)
                
            #else:
                #os.remove(score_path)
if __name__ == '__main__':

    main()