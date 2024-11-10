import csv
import pandas
import numpy
import sys

sys.exit("DONE RUNNING")

"""
silencing,dropout,prior,rep

silencing: 0, 25, 50, 75, 100
dropout: 100, 75, 50, 25, 0 (don't need)
prior: 01, 02, 03, 04, 05, 06, 07, 08, 09, 10
rep: 01, 02, 03, 04, 05
"""

# Methods
methods = ["startle_nni",
           "laml",
           "cassiopeia_greedy",
           "star_cdp-rand",
           "star_cdp",
           "paup",
           "paup-sc",
           "star_cdp-sc"]

namemap = {}
namemap["startle_nni"] = "Startle-NNI (C++)"
namemap["laml"] = "LAML"
namemap["cassiopeia_greedy"] = "Cassiopeia-Greedy"
namemap["startle_nni_python"] = "Startle-NNI (Py)"
namemap["star_cdp-rand"] = "StarCDP-Rand"
namemap["star_cdp"] = "StarCDP-Bias"
namemap["paup"] = "PAUP*"
namemap["paup-sc"] = "PAUP*-SC"
namemap["star_cdp-sc"] = "StarCDP-SC"
namemap["startle_ilp"] = "Startle-ILP"

# Data to keep
cols = ["SILENCING",
        "PRIOR",
        "LABL",
        "REPL", 
        "MTHD",
        "NIBR_TRUE",
        "NIBR_ESTI",
        "FN",
        "FP",
        "TP",
        "FN_RATE",
        "FP_RATE",
        "TP_RATE",
        "PRECISION",
        "RECALL",
        "F1SCORE",
        "RF",
        "PSCORE",
        "NORM_PSCORE",
        "SECS",
        "CONTRACT"]

df1 = pandas.read_csv("mai2024laml_sub250_raw_table-RF0.csv", keep_default_na=False)
df1["contract"] = "NONE"
df2 = pandas.read_csv("mai2024laml_sub250_raw_table-RFSH.csv", keep_default_na=False)
df2["contract"] = "SH"
df = pandas.concat([df1, df2])

rows = []

for contract in ["NONE", "SH"]:
    for miss in [0, 25, 50, 75, 100]:
        for prior in range(1, 11):
            repls = [x for x in range(1, 6)]
            for repl in repls:
                xdf = df[(df["silencing"] == miss) &
                         (df["prior"] == prior) &
                         (df["rep"] == repl) & 
                         (df["contract"] == contract)]
                
                ydf = xdf[xdf["method"] == "ground-truth"]

                if ydf.shape[0] != 1:
                    sys.exit(f"Unable to find row - ground-truth {contract} {miss} {prior} {repl}\n")

                score_true = float(ydf["parsimony-score"].values[0])
                nibr_true = int(ydf["#branches"].values[0])

                for mthd in methods:
                    zdf = xdf[xdf["method"] == mthd]
                             
                    if zdf.shape[0] != 1:
                        sys.exit(f"Unable to find row - {mthd} {contract} {miss} {prior} {repl}\n")

                    try:
                        if mthd == "paup-sc" or mthd == "star_cdp-sc":
                            secs = "NA"
                            score_esti = "NA"
                            norm_score_esti = "NA"
                        else:
                            secs = float(zdf["time"].values[0])
                            score_esti = float(zdf["parsimony-score"].values[0])
                            norm_score_esti = score_esti / score_true

                        nibr_esti = int(zdf["#branches"].values[0])

                        if nibr_esti == 0:
                            sys.stdout.write(f"{mthd} - {contract} {miss} {prior} {repl} : 0 branches!\n")

                        fn = int(zdf["#FN"].values[0])
                        fp = int(zdf["#FP"].values[0])
                        tp = int(zdf["#TP"].values[0])
                        fn_rate = float(zdf["FN_rate"].values[0])
                        fp_rate = float(zdf["FP_rate"].values[0])
                        tp_rate = float(zdf["TP_rate"].values[0])

                        if nibr_esti != fp + tp:
                            sys.stdout.write(f"{mthd} - {contract} {miss} {prior} {repl} : NIBR_ESTI {nibr_esti} != FP {fp} + TP {tp} = {fp + tp}\n")

                        if nibr_true != fn + tp:
                            sys.stdout.write(f"{mthd} - {contract} {miss} {prior} {repl} : NIBR_TRUE {nibr_true} != FN {fn} + TP {tp} = {fn + tp}\n") 

                        if (nibr_true > 0) and (nibr_esti > 0):
                            precision = tp / nibr_esti
                            recall = tp / nibr_true
                            if tp > 0:
                                f1score = 2 / ((1.0 / precision) + (1.0 / recall))
                            else:
                                f1score = 0
                        else:
                            precision = 0
                            recall = 0
                            f1score = 0

                        row = {}
                        row["SILENCING"] = miss
                        row["PRIOR"] = prior
                        row["LABL"] = f"{miss}%"
                        row["REPL"] = repl
                        row["MTHD"] = namemap[mthd]
                        row["NIBR_ESTI"] = nibr_esti
                        row["NIBR_TRUE"] = nibr_true
                        row["FN"] = fn
                        row["FP"] = fp
                        row["TP"] = tp
                        row["FN_RATE"] = fn_rate
                        row["FP_RATE"] = fp_rate
                        row["TP_RATE"] = tp_rate
                        row["PRECISION"] = precision
                        row["RECALL"] = recall
                        row["F1SCORE"] = f1score
                        row["RF"] = fn + fp
                        row["PSCORE"] = score_esti
                        row["NORM_PSCORE"] = norm_score_esti
                        row["SECS"] = secs
                        row["CONTRACT"] = contract

                        rows.append(row)
                    except ValueError:
                        print(zdf)
                        sys.exit(f"Unable to find data for row - {mthd} {contract} {miss} {repl}\n")

outdf = pandas.DataFrame(rows, columns=cols)
outdf.to_csv("data-mai2024laml.csv", sep=',', na_rep="NA",
             header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)


