import treeswift as ts 
import pandas as pd
import os 
import subprocess as sp
import re
import dendropy
import sys

score_pattern = r"small parsimony score = ([\d.]+)"

software_dir = "/fs/cbcb-lab/ekmolloy/jdai123/clt-missing-data-study/software"

startle_dir = os.path.join(software_dir, 'startle')

startle_nni_dir = os.path.join(startle_dir, 'build')
startle_nni_dir = os.path.join(startle_nni_dir, 'src')

startle_exe = os.path.join(startle_nni_dir, 'startle')

def count_migration(tre, labels_list, taxon2order):
    optimal_labeling = {}
    score = {}
    trace_back = {}
    count = 0
    internalnode2label = {}
    first_primary_tumor_id = min(labels_list)
    for node in tre.traverse_postorder():
        score[node] = {}
        trace_back[node] = {}
        if not node.is_leaf():
            if not node.is_root():
                internalnode2label[node] = f'I{count}'
                count += 1
                node.label = internalnode2label[node]
            else:
                node.label = 'root'
                internalnode2label[node] = 'root'

        for lab in labels_list:
            if node.is_leaf():
                if str(node.get_label()) not in taxon2order:
                    print("Warning Missing some taxon in dict!!!")
                if lab == taxon2order[str(node.get_label())]:
                    score[node][lab] = 0
                else:
                    score[node][lab] = float('inf')
            else:
                tot_cost = 0
                trace_back[node][lab] = {}

                for child in node.child_nodes():
                    #if len(node.child_nodes()) != 2:
                        #print(f"Warring non-binary tree!! len: {len(node.child_nodes())}")


                    best_child_lab = []
                    best_child_contr = float('inf')
                    
                    for child_lab in labels_list:

                        cost = 1 if child_lab != lab else 0
                        
                        if score[child][child_lab] == float('inf'):
                            continue

                        if best_child_contr > cost + score[child][child_lab] and score[child][child_lab] != float('inf'):
                            best_child_contr = cost + score[child][child_lab]
                            best_child_lab = [child_lab]
                        elif best_child_contr == cost + score[child][child_lab] and best_child_contr != float('inf'):
                            best_child_lab.append(child_lab)

                    tot_cost += best_child_contr
                    trace_back[node][lab][child] = best_child_lab
                
                score[node][lab] = tot_cost
        #print(f'{score[node]}||{node.label}')
    print(f'The number of internal nodes(include root): {count-1}')
    print(f'The number of total nodes: {len(list(tre.traverse_postorder()))}')
    return score[tre.root][first_primary_tumor_id],trace_back


def top_down(tre,trace_back,labels_list,order2site, site2order):
    # print(len(list(tre.traverse_postorder())))
    # print(len(trace_back))
    
    for node in tre.traverse_postorder():
        if node not in trace_back:
            print(f"Node label: {node.label} missing in trace_back")
    que = []
    
    first_primary_tumor_id = min(labels_list)
    
    que.append((tre.root,order2site[first_primary_tumor_id]))
    
    optimal_label = {tre.root:order2site[first_primary_tumor_id]}
    
    migration_count = {'p2n_transition':0, 'n2n_transition' : 0, 'n2p_transition':0, 'not_transition':0, 'p2p_transition':0, 'migration':0, 'reseeding':0}
    
    migration_count_all = {}
    primary = order2site[first_primary_tumor_id]
    while que:
        node,lab = que.pop(0)
        for child in node.child_nodes():
            # print(trace_back[node][child])
            
            optimal_label[child] = order2site[min(trace_back[node][site2order[lab]][child])]
            # print(optimal_label[child])
            if lab != optimal_label[child]:
                if f'{lab} -> {optimal_label[child]}' not in migration_count_all:
                    migration_count_all[f'{lab} -> {optimal_label[child]}'] = 1
                else:
                    migration_count_all[f'{lab} -> {optimal_label[child]}'] += 1

                if lab == primary and optimal_label[child] != primary:
                    migration_count['p2n_transition'] += 1
                elif lab != primary and optimal_label[child] != primary:
                    migration_count['n2n_transition'] += 1
                elif lab != primary and optimal_label[child] == primary:
                    migration_count['n2p_transition'] += 1
                    migration_count['reseeding'] += 1
                else:
                    print(f"warnning: parent lab: {lab}; child lab: {optimal_label[child]}")
                migration_count['migration'] += 1
                
            else:
                migration_count['not_transition'] += 1
                # print(f'parent lab: {lab} == child lab {optimal_label[child]}')
            
            que.append((child, optimal_label[child]))
    node_label2site_label = {}
    for node,lab in optimal_label.items():
        node_label2site_label[node.label] = lab
    return node_label2site_label,migration_count,migration_count_all







def process_method(folder, result_dir, data_dir, startle_exe, index_for_dp_list, taxon2order, 
                   index_to_site_map, name_to_index_map, method_name):

    # Prepare result containers
    data = []
    metric = []
    star_cdp_res = []

    # Process tree for the given method
    cur_tree_path = os.path.join(result_dir, folder, f'deduplicated_star_cdp_{method_name}_trees.nwk')
    cur_tree = ts.read_tree_newick(cur_tree_path)
    score, trace_back = count_migration(cur_tree, index_for_dp_list, taxon2order)
    node2site_label, migration_count, migration_count_all = top_down(
        cur_tree, trace_back, index_for_dp_list, index_to_site_map, name_to_index_map
    )
    
    # Record migration and reseeding counts
    data.append(folder)
    metric.append('migration')
    star_cdp_res.append(migration_count['migration'])

    data.append(folder)
    metric.append('reseeding')
    star_cdp_res.append(migration_count['reseeding'])

    # Process SH contracted tree
    cur_sh_tree_path = os.path.join(result_dir, folder, f'deduplicated_star_cdp_{method_name}_sh_trees.nwk')
    cur_sh_tree = ts.read_tree_newick(cur_sh_tree_path)
    score, trace_back = count_migration(cur_sh_tree, index_for_dp_list, taxon2order)
    node2site_label, migration_count, migration_count_all = top_down(
        cur_sh_tree, trace_back, index_for_dp_list, index_to_site_map, name_to_index_map
    )

    # Record SH contract migration and reseeding counts
    data.append(folder)
    metric.append('migration SH Contract')
    star_cdp_res.append(migration_count['migration'])

    data.append(folder)
    metric.append('reseeding SH Contract')
    star_cdp_res.append(migration_count['reseeding'])

    # Compute parsimony score
    priors_path = os.path.join(os.path.join(data_dir, folder), f'{folder}_priors.csv')
    score_prefix = os.path.join(result_dir, folder, f'{method_name}_score')
    
    score_res = sp.run([startle_exe, 'small', os.path.join(data_dir, folder, f'{folder}_deduplicated_character_matrix.csv'),
                        priors_path, cur_tree_path, '--output', score_prefix], capture_output=True, text=True)
    
    if score_res.returncode == 0:
        score_res = score_res.stdout
  
        score_res_match = re.search(r"small parsimony score = ([\d.]+)", score_res)  # Adjust regex as needed

        if score_res_match:
            print(score_res_match)
            score = float(score_res_match.group(1))
            data.append(folder)
            metric.append('parsimony score')
            star_cdp_res.append(score)

    else:
        print("%%")
        print(score_res.stderr)
        raise Exception(f"Failed to compute score for {cur_tree_path}")

    


    # return data, metric, star_cdp_res

    return star_cdp_res















df_kp_meta = pd.read_csv('../KPTracer_meta.csv', index_col = 0)
# print(df_kp_meta)

result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/H_bio_result_Full/star_cdp'

data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full"
tumor_table_for_dp = pd.read_csv('../tumor_info_table_for_dp.csv', sep=',')
print(tumor_table_for_dp)


# folders = ['3457_Apc_T4_Fam', \
#     '3513_NT_T1_Fam', \
#     '3508_Apc_T2_Fam', \
#     '3519_Lkb1_T1_Fam', \
#     '3457_Apc_T1_Fam',\
#     '3460_Lkb1_T1_Fam',\
#     '3519_Lkb1_All',\
#     '3454_Lkb1_All',\
#     '3508_Apc_All',\
#     '3515_Lkb1_T1_Fam',\
#     '3515_Lkb1_All']

# 3457_Apc_T4_Fam' #P = 1, tot: 3
#     '3513_NT_T1_Fam' #P = 1, tot: 3
#     '3508_Apc_T2_Fam'  #P = 1 tot: 9
#     '3519_Lkb1_T1_Fam', #P = 1 tot: 2
#     '3457_Apc_T1_Fam', #P = 1 tot: 3
#     '3460_Lkb1_T1_Fam' #P = 1 tot: 6
#     '3519_Lkb1_All',#P = 3 tot: 4
#     '3454_Lkb1_All',#P = 2 tot: 4
#     '3508_Apc_All',#P = 2 tot: 10
#     '3515_Lkb1_T1_Fam',#P = 1 tot: 7
#     '3515_Lkb1_All' #P = 3 tot: 9

folders = [
    '3515_Lkb1_T1_Fam']




data = []
metirc = []
star_cdp_res = []
star_cdp_rand_res = []
star_cdp_sc_res = []

for folder in folders:
    
    
    pruned_cmat = pd.read_csv(os.path.join(data_dir, folder, folder + '_deduplicated_character_matrix.csv'), index_col=0, dtype=str)
    taxon2site = df_kp_meta.loc[pruned_cmat.index]['SubTumor']
    
    for cell, site in taxon2site.items():
        if len(site.split('_')) > 3:
            taxon2site[cell] = '_'.join(site.split('_')[:-1])
    
    cur_info_table_for_dp = tumor_table_for_dp[tumor_table_for_dp['family'] == folder]

    
    index_for_dp_list = cur_info_table_for_dp['index_for_dp'].tolist()

    # KPtracer paper define site label -> human readable site label
    name_to_full_site_name_map = dict(zip(cur_info_table_for_dp['name'], cur_info_table_for_dp['full_site_name']))

    # human readable site label -> index 
    name_to_index_map = dict(zip(cur_info_table_for_dp['full_site_name'], cur_info_table_for_dp['index_for_dp']))
    #
    index_to_site_map = dict(zip(cur_info_table_for_dp['index_for_dp'], cur_info_table_for_dp['full_site_name']))
    
    # leaf cell name -> human readable site label 
    for cell,site in taxon2site.items():
        taxon2site[cell] = name_to_full_site_name_map[site]


    taxon2order = {}
    for cell,site in taxon2site.items():
        taxon2order[cell] = name_to_index_map[site]
    

    cur_tree_path = os.path.join(result_dir, folder, 'deduplicated_star_cdp_one_sol_trees.nwk')
    cur_tree = ts.read_tree_newick(cur_tree_path)
    score,trace_back = count_migration(cur_tree, index_for_dp_list, taxon2order)
    node2site_label, migration_count, migration_count_all = top_down(cur_tree,trace_back,index_for_dp_list,index_to_site_map,name_to_index_map)
    
    data.append(folder)

    metirc.append('migration')
    star_cdp_res.append(migration_count['migration'])

    data.append(folder)

    metirc.append('reseeding')
    star_cdp_res.append(migration_count['reseeding'])
    

    cur_sh_tree_path = os.path.join(result_dir, folder, 'deduplicated_star_cdp_one_sol_sh_trees.nwk')
    cur_sh_tree = ts.read_tree_newick(cur_sh_tree_path)
  

    score,trace_back = count_migration(cur_sh_tree, index_for_dp_list, taxon2order)
    node2site_label, migration_count, migration_count_all = top_down(cur_sh_tree,trace_back,index_for_dp_list,index_to_site_map,name_to_index_map)

    data.append(folder)

    metirc.append('migration SH Contract')
    star_cdp_res.append(migration_count['migration'])

    data.append(folder)

    metirc.append('reseeding SH Contract')
    star_cdp_res.append(migration_count['reseeding'])



    priors_path = os.path.join(os.path.join(data_dir, folder), folder + '_priors.csv')
    score_prefix = os.path.join(result_dir, folder, 'star_cdp_score')
    
    score_res = sp.run([startle_exe, 'small', os.path.join(data_dir, folder, folder + '_deduplicated_character_matrix.csv'), priors_path, cur_tree_path, '--output', score_prefix], capture_output=True, text=True)
            
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

        data.append(folder)

        metirc.append('parsimony score')
        star_cdp_res.append(score)



    cur_star_cdp_rand_res = process_method(folder, result_dir, data_dir, startle_exe, index_for_dp_list, taxon2order, 
                   index_to_site_map, name_to_index_map, 'rand_sol')

    star_cdp_rand_res  = star_cdp_rand_res + cur_star_cdp_rand_res

    cur_star_cdp_sc_res = process_method(folder, result_dir, data_dir, startle_exe, index_for_dp_list, taxon2order, 
                   index_to_site_map, name_to_index_map, 'sc')


    star_cdp_sc_res  = star_cdp_sc_res + cur_star_cdp_sc_res

    print(len(data))
    print(len(metirc))
    print(len(star_cdp_res))
    print(len(star_cdp_rand_res))
    print(len(star_cdp_sc_res))
    table_df = pd.DataFrame({
        'Data' : data,
        'Metric' : metirc,
        'StarCDP': star_cdp_res,
        'StarCDP-Rand':star_cdp_rand_res,
        'StarCDP-Sc':star_cdp_sc_res
    })
    
    print(table_df)
    table_df.to_csv('migration_table.csv',sep=',',index=False)
