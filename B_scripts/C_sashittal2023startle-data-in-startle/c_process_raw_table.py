import pandas as pd

df = pd.read_csv('raw_table.csv')
df = df.dropna(subset=['#branches','#FN', '#FP', '#TP','FN_rate','FP_rate','TP_rate','parsimony-score'], how='all')

cells = df['cells'].drop_duplicates().tolist()
chars = df['characters'].drop_duplicates().tolist()
dropouts = df['dropout'].drop_duplicates().tolist()
mutationrates = df['mutationrate'].drop_duplicates().tolist()
reps = df['rep'].drop_duplicates().tolist()
methods = df['method'].drop_duplicates().tolist()
column_names = df.columns.tolist()

metrics = [x for x in column_names if x not in ['cells', 'characters', 'dropout', 'mutationrate', 'rep', 'method', '#branches']]

our_methods = ['star_cdp', 'star_cdp-sc']
other_methods = [x for x in methods if x not in our_methods]
other_methods = [x for x in methods if x != 'ground-truth']



table = {key: [] for key in ['cells', 'characters', 'dropout', 'mutationrate','method','#FN(b/w)', '#FP(b/w)','#TP(b/w)','FN_rate(b/w)','FP_rate(b/w)','TP_rate(b/w)','parsimony-score(b/w)', 'weighted-parsimony-score(b/w)','time(b/w)']}


for cell in cells:
    for chart in chars:
        for d in dropouts:
            for mut in mutationrates:
                        for our_method in our_methods:

                            table['cells'].append(cell)
                            table['characters'].append(chart)
                            table['dropout'].append(d)
                            table['mutationrate'].append(mut)
                            table['method'].append(our_method)

                            for metric in metrics:

                                
                            
                                b,w = 0,0
                                for rep in reps:
                                    cur_metric_over_reps_df = df[(df['cells'] == cell) & \
                                    (df['characters'] == chart) & (df['dropout'] == d) & \
                                    (df['mutationrate'] == mut) & (df['rep'] == rep) & \
                                    (df['method'] != 'ground-truth')]

                                    min_value = cur_metric_over_reps_df[metric].min()
                                    max_value = cur_metric_over_reps_df[metric].max()
                                    
                                    our_value = cur_metric_over_reps_df[(cur_metric_over_reps_df['method'] == our_method)]
                                    our_value = our_value[metric].values[0]

                                    if our_value == min_value:
                                        if metric != '#TP(b/w)':
                                            b += 1
                                        else:
                                            w += 1
                                    
                                    if our_value == max_value:
                                        if metric != '#TP(b/w)':
                                            w += 1
                                        else:
                                            b += 1
                                table[metric+'(b/w)'].append(f'{b}/{w}')
for k,v in table.items():
        print(f'k:{k}, len(v):{len(v)}')
df = pd.DataFrame(table)
df.to_csv('processed_table.csv', index=False)                               

                                




