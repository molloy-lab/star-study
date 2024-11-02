import os
import shutil





data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data'
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/E_bio_result_pruned/star_cdp'
#paup_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/E_bio_result/paup'
target_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/G_bio_result_pruned_deduplicate/star_cdp'
folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
print(folders)

for folder in folders:
    if not os.path.exists(os.path.join(target_dir, folder)):
        os.mkdir(os.path.join(target_dir, folder))
    
    full_sc_path = os.path.join(result_dir, folder, 'replaced_consensus_star_cdp_strict_consensus.tre')
    full_one_sol_path = os.path.join(result_dir, folder, 'replaced_star_cdp_one_sol.tre')
    full_rand_sol_path = os.path.join(result_dir, folder, 'replaced_star_cdp-rand_one_sol.tre')

    depruned_sc_path = os.path.join(target_dir, folder, 'star_cdp_sc_depruned.tre')
    depruned_one_sol_path = os.path.join(target_dir, folder, 'star_cdp_one_sol_depruned.tre')
    depruned_rand_sol_path = os.path.join(target_dir, folder, 'star_cdp_rand_depruned.tre')
    shutil.copy(full_sc_path, depruned_sc_path)
    shutil.copy(full_one_sol_path, depruned_one_sol_path)
    shutil.copy(full_rand_sol_path, depruned_rand_sol_path)
    #print(depruned_one_sol_path)
    #print(depruned_sc_path)
    #exit(0)
