import os
import shutil





data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data'
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/E_bio_result_pruned/paup'
#paup_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/E_bio_result/paup'
target_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/G_bio_result_pruned_deduplicate/paup'
folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
print(folders)

for folder in folders:
    if not os.path.exists(os.path.join(target_dir, folder)):
        os.mkdir(os.path.join(target_dir, folder))
    
    full_sc_path = os.path.join(result_dir, folder, 'strict_consensus.tre')
    full_one_sol_path = os.path.join(result_dir, folder, 'one_nwk.newick')
    
    depruned_sc_path = os.path.join(target_dir, folder, 'paup_sc_depruned.tre')
    depruned_one_sol_path = os.path.join(target_dir, folder, 'paup_one_sol_depruned.tre')
    
    shutil.copy(full_sc_path, depruned_sc_path)
    shutil.copy(full_one_sol_path, depruned_one_sol_path)
    #print(depruned_one_sol_path)
    #print(depruned_sc_path)
    #exit(0)
