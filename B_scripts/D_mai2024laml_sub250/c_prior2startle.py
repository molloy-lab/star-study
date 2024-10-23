import pandas as pd
import os
import sys


data_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/mai2024laml_sub250'

folders = [f for f in os.listdir(data_dir) if os.path.exists(os.path.join(data_dir, f))]

folders = [f for f in folders if f not in ['model_tree.txt', 'summary_stats.txt', 'true_missing_stats.txt']]

for folder in folders:
    cur_folder_path = os.path.join(data_dir, folder)
    files = [f for f in os.listdir(cur_folder_path) if os.path.exists(os.path.join(cur_folder_path, f))]
    print(folder)
    for f in files:

        if f.startswith('prior_'):
            
            prior = pd.read_csv(os.path.join(cur_folder_path,f), header=None)
            prior.columns = ['character', 'state', 'probability']
            prior['character'] = 'c' + prior['character'].astype(str)

            prior.to_csv(os.path.join(cur_folder_path, 'startle_format_priors.csv'),index=False)