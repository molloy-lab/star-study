import os
import subprocess as sp
import re
import dendropy
import sys

def main():
    sys.setrecursionlimit(4000)

    result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_laml_sub250/startle_nni'

    data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250"
    
    software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/scripts/sashittal2023startle-sim"

    comp_exe = os.path.join(software_dir, 'compare_two_rooted_trees_under_star.py')


    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]


    for folder in folders:
        cur_data_path = os.path.join(data_dir, folder)
        cur_res_path = os.path.join(result_dir, folder)
        

        cmat_path = os.path.join(cur_data_path, "startle_format_cmat.csv")
  

        score_path = os.path.join(cur_res_path, 'RFSH.csv')
        
        true_tree_path = os.path.join(cur_data_path, 'SH_contract_true_tree.tre')

        star_cdp_tree_path = os.path.join(cur_res_path, 'nni_tree.newick')
        
        data_prefix = folder
        print(data_prefix)

        if not os.path.exists(score_path) or True:
              
            score_res = sp.run(['python3', comp_exe, '-t1', true_tree_path, '-t2', star_cdp_tree_path, '-c1','0', '-c2', '1', '-m', cmat_path], capture_output=True, text=True)

           
            if score_res.returncode == 0:
                score_res = score_res.stdout
                print(score_res)
                [nl, i1, i2, fn, fp, tp, fnrate, fprate,tprate] = [float(x) for x in score_res.split(',')]
                print(f'{fn}, {fp},{tp}')


            else:
                print("%%")
                print(score_res.stderr)
                raise Exception("Failed to compute score for " + cur_res_path)

            
            with open(score_path, 'w', newline="") as score_file:
                score_file.write(f'{nl},{i1},{i2},{fn},{fp},{tp}, {fnrate},{fprate},{tprate}\n')
                print(f'write {score_path}')
            #else:
                #os.remove(score_path)

if __name__ == '__main__':

    main()