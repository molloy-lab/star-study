import pandas as pd
import math
import os 
import re

df_kp_meta = pd.read_csv('KPTracer_meta.csv', index_col = 0)
# print(df_kp_meta)
subtumor_unique = df_kp_meta['SubTumor'].drop_duplicates().tolist()

subtumor_unique = [x for x in subtumor_unique if not (isinstance(x, float) and math.isnan(x))]
# print(subtumor_unique)
prefixs = list(set([f.split('_')[0]+"_" + f.split('_')[1] for f in subtumor_unique]))

data_df = pd.read_csv('cells_number.csv')
sorted_df = data_df.sort_values(by='rest_cell_num')
folders = sorted_df['data'].values
folders = folders.tolist()
# folders.remove('3724_NT_All')

data_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/A_data/KPTracer-Data-Full/'

# print(folders)
all_family = [f for f in folders if f.endswith('_Fam') or f.endswith('All')]
all_family_df = sorted_df[sorted_df['data'].isin(all_family)]

sorted_all_family_df = all_family_df.sort_values(by='rest_cell_num')

all_faimily_vec = []
for index, row in sorted_all_family_df.iterrows():
    print(f"{row['data']}: {row['rest_cell_num']}")
    all_faimily_vec.append(row['data'])

# print(all_faimily_vec)

token2meta = {
    'Rib': 'Rib-cage',
    'S': 'Soft-tissue',
    'N': 'Lymph-tissue',
    'K' :'Kidney',
    'Liv':'Liver',
    'Spl':'Spleen',
    'DN':'Draining-lymph',
    'PF': 'Pleural-fluid',
    'B':'Blood',
    'T': 'Primary-tumor',
    'L': 'Lung'
}

meta2index_prefix = {
    'Rib-cage':10,
    'Soft-tissue':9,
    'Lymph-tissue':8,
    'Kidney':7,
    'Liver':6,
    'Spleen':5,
    'Draining-lymph':4,
    'Pleural-fluid':3,
    'Blood':2,
    'Primary-tumor':0,
    'Lung':1
}


## return tumor name,site labeling, number id
def parse_subtumor(subtumor):
    print(f'parsing {subtumor}')
    tokens = subtumor.split('_')
    identifier = tokens[0]
    mice_type = tokens[1]
    tumor_type = tokens[2]
    num_id = 0
    if tumor_type[-1].isdigit():
        tumor_loc = token2meta[tumor_type[:-1]]
        num_id = int(tumor_type[-1])
    else:
        tumor_loc = token2meta[tumor_type]
        
    return subtumor, tumor_loc, num_id


count = 0
tumor_family = []
tumor_name = []
tumor_site = []
tumor_id = []
tumor_index_for_dp = []
tumors_vec = []
human_readable = []
tumor_full_site_name = []

for faimily in all_faimily_vec:
    pruned_cmat = pd.read_csv(os.path.join(data_dir, faimily, faimily + '_deduplicated_character_matrix.csv'), index_col=0, dtype=str)
    taxon2site = df_kp_meta.loc[pruned_cmat.index]['SubTumor']
    non_null_taxon2site = taxon2site[taxon2site.notna()]
    null_taxon2site = taxon2site[taxon2site.isna()]
    print(f"Number of taxons with SubTumor: {len(non_null_taxon2site)}")
    print(f"Number of taxons without SubTumor: {len(null_taxon2site)}")
    if len(null_taxon2site) != 0:
        count += 1
# 3457_Apc_T4_Fam: 31
# 3513_NT_T1_Fam: 86
# 3508_Apc_T2_Fam: 105
# 3519_Lkb1_T1_Fam: 126
# 3457_Apc_T1_Fam: 144
# 3460_Lkb1_T1_Fam: 270
# 3519_Lkb1_All: 342
# 3454_Lkb1_All: 509
# 3508_Apc_All: 567
# 3515_Lkb1_T1_Fam: 878
# 3515_Lkb1_All: 1095

    for cell, site in taxon2site.items():
        if len(site.split('_')) > 3:
            taxon2site[cell] = '_'.join(site.split('_')[:-1])

    unique_values = set(taxon2site)
    tumors_vec.append(list(unique_values))
    
    
    
    for subtumor in unique_values:
        tumor,site, num_id = parse_subtumor(subtumor)
        tumor_name.append(tumor)
        tumor_site.append(site)
        tumor_id.append(num_id)
        tumor_family.append(faimily)
        tumor_index_for_dp.append(meta2index_prefix[site]*10 + num_id)
        if site != 'Primary-tumor':
            tumor_full_site_name.append(f'{site}-metastasis-{num_id}')
        else:
            tumor_full_site_name.append(f'{site}-{num_id}')
        

    
    
    print(f'# tumor sites: {len(unique_values)}')
print(f'taxon without subtumor: {count}')

tumor_table = {
    'family':tumor_family,
    'name': tumor_name,
    'site': tumor_site,
    'num_id':tumor_id,
    'index_for_dp':tumor_index_for_dp,
    'full_site_name': tumor_full_site_name
}

tumor_df = pd.DataFrame(tumor_table)
print(tumor_df)

# print(tumors_vec)
# print(len(tumors_vec))

tumor_df.to_csv('tumor_info_table_for_dp.csv', sep=',',index=False)
    

