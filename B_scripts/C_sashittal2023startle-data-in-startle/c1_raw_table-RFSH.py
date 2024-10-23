import os
import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
pd.set_option('future.no_silent_downcasting', True)
result_dir = '/fs/cbcb-lab/ekmolloy/jdai123/star-study/result_data_in_startle'
data_dir = "/fs/cbcb-lab/ekmolloy/jdai123/star-study/data/sashittal2023startle_data_in_startle"


def check(i1,i2,fn,fp,tp):
    if fp + tp != i2:
        raise Exception(f"fp:{fp} + tp:{tp} != i2:{i2}")
    elif i1 != fn + tp:
        raise Exception(f"fp:{fn} + tp:{tp} != i1:{i1}")

models = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]

reps = [str(i) for i in  range(21)]


model_parameters = [os.path.join(data_dir,model, rep) for model in models for rep in reps]
cells = [50, 100, 150, 200]
characters = [10,20,30]
dropouts = [0.15]
mutationrates = [0.1]

model_names = [f'cells_{cell}_characters_{character}_dropout_{dropout}_mutationrate_{mutationrate}' \
for cell in cells for character in characters for dropout in dropouts for mutationrate in mutationrates]

methdo2rf_file = {
    'cassiopeia-greedy': 'RFSH.csv',
    'startle_nni': 'RFSH.csv',
    'startle_nni_python': 'RFSH.csv',
    'startle_ilp': 'RFSH.csv',
    'laml': 'RFSH.csv',
    'paup': 'RFSH.csv',
    'star_cdp': 'RFSH.csv',
    'star_cdp-rand': 'Rand-RFSH.csv',
    'star_cdp-sc':'sc-RFSH.csv',
    'paup-sc':'sc-RFSH.csv'

}
method2folder = {
    'cassiopeia-greedy': 'cassiopeia-greedy',
    'startle_nni': 'startle_nni',
    'startle_nni_python': 'startle_nni_python',
    'startle_ilp': 'startle_ilp',
    'laml': 'laml',
    'paup': 'paup',
    'star_cdp': 'star_cdp',
    'star_cdp-rand': 'star_cdp',
    'star_cdp-sc':'star_cdp',
    'paup-sc':'paup'
}

table = {key: [] for key in ['cells', 'characters', 'dropout', 'mutationrate', 'rep','method','#branches','#FN', '#FP', '#TP','FN_rate','FP_rate','TP_rate','parsimony-score', 'time', 'normalized-parsimony-score']}
methods = ['cassiopeia-greedy','startle_nni','startle_nni_python','startle_ilp', 'laml', 'paup','star_cdp', 'star_cdp-rand',\
'paup-sc', 'star_cdp-sc','ground-truth']

for cell in cells:
    for character in characters:
        for dropout in dropouts:
            for mutationrate in mutationrates:
                for rep in reps:
                    for method in methods:
                        table['cells'].append(cell)
                        table['characters'].append(character)
                        table['dropout'].append(dropout)
                        table['mutationrate'].append(mutationrate)
                        table['rep'].append(rep)
                        table['method'].append(method)
                        
                        if method == 'ground-truth':
                            table['#FN'].append(0)
                            table['#FP'].append(0)
                            table['#TP'].append(i1)
                            table['#branches'].append(int(i1))
                            table['FN_rate'].append(0.0)
                            table['FP_rate'].append(0.0)
                            table['TP_rate'].append(1)
                            table['time'].append(pd.NA)
                            table['normalized-parsimony-score'].append(1)
                            
                            cur_data_path = os.path.join(data_dir,\
                            f'cells_{cell}_characters_{character}_dropout_{dropout}_mutationrate_{mutationrate}', rep)
                            print(cur_data_path)
                            score_file = os.path.join(cur_data_path, 'score.csv')

                            with open(score_file, 'r') as scf:
                                score = Decimal(scf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                                table['parsimony-score'].append(score)



                        else:
                            cur_res_path = os.path.join(result_dir, method2folder[method],\
                            f'cells_{cell}_characters_{character}_dropout_{dropout}_mutationrate_{mutationrate}', rep)
                            
                            # rf_file = os.path.join(cur_res_path, 'contract_RF.csv')
                            rf_file = os.path.join(cur_res_path, methdo2rf_file[method])
                            
                            # if method == 'laml':
                                # rf_file = os.path.join(cur_res_path, 'RF.csv')
                            
                            if not os.path.exists(rf_file):
                                table['#FN'].append(pd.NA)
                                table['#FP'].append(pd.NA)
                                table['#TP'].append(pd.NA)
                                table['#branches'].append(pd.NA)
                                table['FN_rate'].append(pd.NA)
                                table['FP_rate'].append(pd.NA)
                                table['TP_rate'].append(pd.NA)
                                
                            
                            else:

                                with open(rf_file, 'r') as rf:
                                    
                                    [nl, i1, i2, fn, fp, tp, fnrate, fprate,tprate] = [
                                        float(x) if x.strip() != 'N/A' else pd.NA for x in rf.readline().strip().split(',')
                                        ]
                                    if not all(pd.isna(x) for x in [nl, i1, i2, fn, fp, tp, fnrate, fprate, tprate]):

                                        check(i1,i2,fn,fp,tp)
                                        table['#FN'].append(int(fn))
                                        table['#FP'].append(int(fp))
                                        table['#TP'].append(int(tp))
                                        table['#branches'].append(int(i2))
                                        table['FN_rate'].append(fnrate)
                                        table['FP_rate'].append(fprate)
                                        table['TP_rate'].append(tprate)
                                    else:
                                        table['#FN'].append(pd.NA)
                                        table['#FP'].append(pd.NA)
                                        table['#TP'].append(pd.NA)
                                        table['#branches'].append(pd.NA)
                                        table['FN_rate'].append(pd.NA)
                                        table['FP_rate'].append(pd.NA)
                                        table['TP_rate'].append(pd.NA)
                        
                            time_file = os.path.join(cur_res_path, 'time.csv')
                            
                            if not os.path.exists(time_file):
                                table['time'].append(pd.NA)
                            else:
                                with open(time_file, 'r') as tf:
                                    time = Decimal(tf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                                    table['time'].append(time)

                            score_file = os.path.join(cur_res_path, 'score.csv')
                            
                            if not os.path.exists(score_file):
                                table['parsimony-score'].append(pd.NA)
                                table['normalized-parsimony-score'].append(pd.NA)
                            else:
                                with open(score_file, 'r') as scf:
                                    score = Decimal(scf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                                    table['parsimony-score'].append(score)

                                    cur_data_path = os.path.join(data_dir,f'cells_{cell}_characters_{character}_dropout_{dropout}_mutationrate_{mutationrate}', rep)
                                    score_file = os.path.join(cur_data_path, 'score.csv')

                                    with open(score_file, 'r') as scf:
                                        gscore = Decimal(scf.readline().strip()).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                                        table['normalized-parsimony-score'].append(score / gscore)
                                        print(score / gscore)


for k,v in table.items():
        print(f'k:{k}, len(v):{len(v)}')
df = pd.DataFrame(table)

# df['parsimony-score'] = pd.to_numeric(df['parsimony-score'], errors='coerce')
# ground_truth_score = df.loc[df['method'] == 'ground-truth', 'parsimony-score'].values[0]
# df['normalized-parsimony-score'] = df['parsimony-score'].apply(
#     lambda x: x / ground_truth_score if pd.notna(x) else pd.NA
# )

print(df)

df.to_csv('startle-sim_table-RFSH.csv', index=False)
exit(0)
# df = df.dropna(subset=['#branches_in_true_tree','#branches','#FN', '#FP', '#TP','FN_rate','FP_rate','TP_rate','parsimony-score', 'time'], how='all')

