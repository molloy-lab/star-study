import os
import sys
import pandas as pd

data_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250'

folders = [f for f in os.listdir(data_dir) if os.path.exists(os.path.join(data_dir, f))]

folders = [f for f in folders if f not in ['model_tree.txt', 'summary_stats.txt', 'true_missing_stats.txt']]

for folder in folders:
    cur_folder_path = os.path.join(data_dir, folder)
    files = [f for f in os.listdir(cur_folder_path) if os.path.exists(os.path.join(cur_folder_path, f))]

    for f in files:

        if f.endswith('character_matrix.csv'):
            cmat = pd.read_csv(os.path.join(cur_folder_path,f))
            cmat.replace('?', -1, inplace=True)
  
            headers = cmat.columns 
            headers = list(headers)
            headers = [header.replace('r', 'c', 1) if header.startswith('r') else header for header in headers]
            headers = [""] + [f'c{i}' for i in range(len(headers) - 1)]
            cmat.columns = headers
            cmat.to_csv(os.path.join(cur_folder_path, 'startle_format_cmat.csv'),index=False)
            
