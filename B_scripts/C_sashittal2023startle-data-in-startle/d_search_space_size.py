import os
import pandas as pd
import numpy as np
import re
project_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study'
results_dir = os.path.join(project_dir, 'C_result_data_in_startle')
star_cdp_dir = os.path.join(results_dir, 'star_cdp')


folders = [f for f in os.listdir(star_cdp_dir) if os.path.isdir(os.path.join(star_cdp_dir, f))]
## 'cells_200_characters_30_dropout_0.15_mutationrate_0.1'
table = {k : [] for k in ['cells', 'characters', 'dropout', 'mutationrate', 'rep','search_space_size']}
#The size of the search space(subproblems): 287
regex = re.compile('The size of the search space\(subproblems\): (\d+)')

for folder in folders:
    cells, characters, dropout, mutationrate = folder.split('_')[1], folder.split('_')[3], folder.split('_')[5], folder.split('_')[7]
    reps = [rep for rep in os.listdir(os.path.join(star_cdp_dir, folder)) if os.path.isdir(os.path.join(star_cdp_dir, folder, rep))]
    for rep in reps:
        log_file = os.path.join(star_cdp_dir, folder, rep, 'star_cdp.log')
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                matched = re.search(regex, line)
                if matched:
                    search_space_size = int(matched.group(1))
                    table['cells'].append(int(cells))
                    table['characters'].append(int(characters))
                    table['dropout'].append(float(dropout))
                    table['mutationrate'].append(float(mutationrate))
                    table['rep'].append(int(rep))
                    table['search_space_size'].append(search_space_size)
                    break
    print('Done with', folder)

df = pd.DataFrame(table)
df = df.sort_values(by=['cells', 'characters', 'dropout', 'mutationrate', 'rep'])
print(df)
df.to_csv(os.path.join(results_dir, 'search_space_size.csv'), index=False)
exit(0)