import csv
import pandas
import numpy
import sys

sys.exit("DONE RUNNING")

"""
cells,characters,dropout,mutationrate,rep,

cells: 50, 100, 150, 200
characters: 10, 20, 30
dropout: 0.15
mutation rate: 0.10
rep: 0-20

paup-sc - 50 10 19 : 0 branches! <- only one in main figure
paup-sc - 50 20 19 : 0 branches!
paup-sc - 100 10 17 : 0 branches!
paup-sc - 100 10 19 : 0 branches!
"""

# Methods
methods = ["startle_nni",
           "laml",
           "cassiopeia-greedy",
           "startle_nni_python",
           "star_cdp-rand",
           "star_cdp",
           "paup",
           "paup-sc",
           "star_cdp-sc",
           "startle_ilp"]

namemap = {}
namemap["startle_nni"] = "Startle-NNI (C++)"
namemap["laml"] = "LAML"
namemap["cassiopeia-greedy"] = "Cassiopeia-Greedy"
namemap["startle_nni_python"] = "Startle-NNI (Py)"
namemap["star_cdp-rand"] = "StarCDP-Rand"
namemap["star_cdp"] = "StarCDP-Bias"
namemap["paup"] = "PAUP*"
namemap["paup-sc"] = "PAUP*-SC"
namemap["star_cdp-sc"] = "StarCDP-SC"
namemap["startle_ilp"] = "Startle-ILP"

# Data to keep
cols = ["NLIN",
        "NCHR", 
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
        "SECS"]

if True:
    df = pandas.read_csv("startle_sim-RFSH.csv", keep_default_na=False)

    rows = []

    for nlin in [50, 100, 150, 200]:
        for nchr in [10, 20, 30]:
            repls = [x for x in range(0, 21)]
            if nlin == 50 and nchr == 10:
                repls.remove(8)   # <- startle_nni_python failed on this replicate
                repls.remove(9)   # <- startle_nni_python failed on this replicate
                repls.remove(10)  # <- startle_nni_python failed on this replicate
            if nlin == 50 and nchr == 20:
                repls.remove(1)   # <- startle_ilp failed on this replicate
            for repl in repls:
                xdf = df[(df["cells"] == nlin) &
                         (df["characters"] == nchr) &
                         (df["dropout"] == 0.15) &
                         (df["mutationrate"] == 0.1) &
                         (df["rep"] == repl)]
                ydf = xdf[xdf["method"] == "ground-truth"]

                if ydf.shape[0] != 1:
                    sys.exit(f"Unable to find row - ground-truth {nlin} {nchr} {repl}\n")

                score_true = float(ydf["parsimony-score"].values[0])
                nibr_true = int(ydf["#branches"].values[0])

                for mthd in methods:
                    zdf = xdf[xdf["method"] == mthd]
                             
                    if zdf.shape[0] != 1:
                        sys.exit(f"Unable to find row - {mthd} {nlin} {nchr} {repl}\n")

                    try:
                        if mthd == "paup-sc" or mthd == "star_cdp-sc":
                            secs = "NA"
                        else:
                            secs = float(zdf["time"].values[0])

                        score_esti = float(zdf["parsimony-score"].values[0])

                        nibr_esti = int(zdf["#branches"].values[0])

                        if nibr_esti == 0:
                            sys.stdout.write(f"{mthd} - {nlin} {nchr} {repl} : 0 branches!\n")

                        fn = int(zdf["#FN"].values[0])
                        fp = int(zdf["#FP"].values[0])
                        tp = int(zdf["#TP"].values[0])
                        fn_rate = float(zdf["FN_rate"].values[0])
                        fp_rate = float(zdf["FP_rate"].values[0])
                        tp_rate = float(zdf["TP_rate"].values[0])

                        if nibr_esti != fp + tp:
                            sys.stdout.write(f"{mthd} - {nlin} {nchr} {repl} : NIBR_ESTI != FP + TP\n")

                        if nibr_true != fn + tp:
                            sys.stdout.write(f"{mthd} - {nlin} {nchr} {repl} : NIBR_TRUE != FN + TP\n") 

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
                        row["NLIN"] = nlin
                        row["NCHR"] = nchr
                        row["LABL"] = f"{nlin}x{nchr}"
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
                        row["NORM_PSCORE"] = score_esti / score_true
                        row["SECS"] = secs

                        rows.append(row)
                    except ValueError:
                        sys.exit(f"Unable to find data for row - {mthd} {nlin} {nchr} {repl}\n")

    outdf = pandas.DataFrame(rows, columns=cols)
    outdf.to_csv("data-sashittal2023startle-shcontract.csv", sep=',', na_rep="NA",
                 header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)


