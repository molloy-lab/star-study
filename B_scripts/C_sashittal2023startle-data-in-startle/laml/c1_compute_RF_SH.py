import os
import subprocess as sp
import re
import sys

def main():


    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle/laml'

    data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle_data_in_startle'
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/scripts/sashittal2023startle-sim"

    comp_exe = os.path.join(software_dir, 'compare_two_rooted_trees_under_star.py')

    folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]


    for folder in folders:
        
        cur_data_path = os.path.join(data_path, folder)
        cur_res_path = os.path.join(result_dir, folder)

        reps = [rep for rep in os.listdir(cur_data_path) if os.path.isdir(os.path.join(cur_data_path, rep))]

        for rep in reps:

            cur_rep_res_path = os.path.join(cur_res_path, rep)
            cur_rep_data_path = os.path.join(cur_data_path, rep)
            cmat_path = os.path.join(cur_rep_data_path,next((file for file in os.listdir(cur_rep_data_path) if file.endswith('_character_matrix.csv')), None))
            
            priors_path = os.path.join(cur_rep_data_path,next((file for file in os.listdir(cur_rep_data_path) if file.endswith('_mutation_prior.csv')), None))
       
            score_path = os.path.join(cur_rep_res_path, 'RFSH.csv')
 
            
            true_tree_path = os.path.join( cur_rep_data_path, 'contracted_true_tree.newick')


            data_prefix = folder +  '\\' + rep
            print(data_prefix)

            
            one_nwk_file = os.path.join(cur_rep_res_path, 'laml_output-1_trees.nwk')


            if not os.path.exists(score_path):
                    
                score_res = sp.run(['python3', comp_exe, '-t1', true_tree_path, '-t2', one_nwk_file, '-c1','0', '-c2', '1', '-m', cmat_path], capture_output=True, text=True)
                    

                if score_res.returncode == 0:
                    score_res = score_res.stdout
                    print(score_res)
                    [nl, i1, i2, fn, fp, tp, fnrate, fprate,tprate] = [float(x) for x in score_res.split(',')]
                    print(f'{fn}, {fp},{tp}')

                else:
                    print("%%")
                    print(score_res.stderr)
            
                with open(score_path, 'w', newline="") as score_file:
                    score_file.write(f'{nl},{i1},{i2},{fn},{fp},{tp}, {fnrate},{fprate},{tprate}\n')
                    print(f'write {score_path}')

                # os.remove(one_nwk_file)
                
            #else:
                #os.remove(score_path)


if __name__ == '__main__':

    main()