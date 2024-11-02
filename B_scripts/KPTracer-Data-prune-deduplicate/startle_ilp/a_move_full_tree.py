import os
import shutil





data_path = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data'
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/E_bio_result_pruned/startle_ilp'
#paup_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/E_bio_result/paup'
target_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/G_bio_result_pruned_deduplicate/startle_ilp'
folders = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]
folders = ['3513_NT_T1_Fam']
print(folders)

for folder in folders:
    if not os.path.exists(os.path.join(target_dir, folder)):
        os.mkdir(os.path.join(target_dir, folder))
    
    
    full_one_sol_path = os.path.join(result_dir, folder, 'replaced_startle_tree.newick')
   

    
    depruned_one_sol_path = os.path.join(target_dir, folder, 'startle_ilp_depruned.tre')
    
    shutil.copy(full_one_sol_path, depruned_one_sol_path)

    #print(depruned_one_sol_path)
    #print(depruned_sc_path)
    #exit(0)
