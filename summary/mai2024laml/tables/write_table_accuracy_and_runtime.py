import pandas
import numpy
import sys


def report_accuracy_fp_stats(df, mthds, contract, miss, amet):
    maxval = 0

    sys.stdout.write("%d" % (miss))

    xdf = df[(df["CONTRACT"] == contract) &
             (df["SILENCING"] == miss)]

    keep_avg = []
    keep_std = []
    for ind, mthd in enumerate(mthds):
        if amet == "F1SCORE":
            vals = xdf[(xdf["MTHD"] == mthd)].F1SCORE.values
        elif amet == "PRECISION":
            vals = xdf[(xdf["MTHD"] == mthd)].PRECISION.values
        elif amet == "RECALL":
            vals = xdf[(xdf["MTHD"] == mthd)].RECALL.values
        else:
            sys.exit("Unknown error metric\n")

        if len(vals) != 50:
            sys.exit("Wrong number of replicates")

        x = round(round(numpy.mean(vals), 3), 2)
        y = round(round(numpy.std(vals), 3), 2)
        keep_avg.append(x)
        keep_std.append(y)

        if x > maxval:
            maxval = x
            maxind = []
            maxind.append(ind)
        elif x == maxval:
            maxind.append(ind)

    minind = set(maxind)
    for i, x in enumerate(keep_avg):
        if i in maxind:
            sys.stdout.write(" & $\\mathbf{%1.2f \\pm %1.2f}$" % (keep_avg[i], keep_std[i]))
        else:
            sys.stdout.write(" & $%1.2f \\pm %1.2f$" % (keep_avg[i], keep_std[i]))

    sys.stdout.write(" \\\\\n")


def report_runtime_stats(df, mthds, contract, miss):
    minval = 172800

    sys.stdout.write("%d" % (miss))

    xdf = df[(df["CONTRACT"] == contract) &
             (df["SILENCING"] == miss)]

    keep_avg = []
    keep_std = []
    for ind, mthd in enumerate(mthds):
        vals = xdf[(xdf["MTHD"] == mthd)].SECS.values

        if len(vals) != 50:
            sys.exit("Wrong number of replicates")

        x = round(round(numpy.mean(vals), 2), 1)
        y = round(round(numpy.std(vals), 2), 1)
        keep_avg.append(x)
        keep_std.append(y)

        if x < minval:
            minval = x
            minind = []
            minind.append(ind)
        elif x == minval:
            minind.append(ind)

    minind = set(minind)
    for i, mthd in enumerate(mthds):
        if (mthd == "StarCDP-SC") or (mthd == "PAUP*-SC"):
            sys.stdout.write(" & NA")
        elif i in minind:
            sys.stdout.write(" & $\\mathbf{%1.1f \\pm %1.1f}$" % (keep_avg[i], keep_std[i]))
        else:
            sys.stdout.write(" & $%1.1f \\pm %1.1f$" % (keep_avg[i], keep_std[i]))

    sys.stdout.write(" \\\\\n")


if __name__ == "__main__":
    df = pandas.read_csv("../csvs/data-mai2024laml.csv",
                         na_values='NA', keep_default_na=False)

    for contract in ["NONE", "SH"]:
        sys.stdout.write("\\begin{table}[!h]\n")
        sys.stdout.write("\\caption[")
        if contract == "NONE":
            sys.stdout.write("Tree accuracy (no contraction) and runtime for LAML simulated data sets]{\\textbf{Tree accuracy (\\textbf{no contraction}) and runtime (in seconds) for LAML simulated data sets with 250 cells.} ")
        else:
            sys.stdout.write("Tree accuracy (SH contraction) and runtime for LAML simulated data sets]{\\textbf{Tree accuracy (\\textbf{SH contraction}) and runtime (in seconds) for LAML simulated data sets with 250 cells.} ")
        sys.stdout.write("Mean $\\pm$ standard deviations are across replicates for each method.}\n")
        sys.stdout.write("\\label{tab:startle-sim}\n")
        sys.stdout.write("\\centering\n")
        sys.stdout.write("\\footnotesize\n")
        sys.stdout.write("\\begin{tabular}{c c c c c c c c c}\n")
        sys.stdout.write("\\toprule \n")

        sys.stdout.write("Proportion & Cassiopeia & StarCDP & StarCDP & PAUP* & PAUP* & StarCDP & Startle   & LAML \\\\\n")
        sys.stdout.write("silencing  & Greedy     & Bias    & Rand    &       & SC    & SC      & NNI (C++) & \\\\\n")
        sys.stdout.write("\\midrule\n")

        mthds = ["Cassiopeia-Greedy",
                 "StarCDP-Bias",
                 "StarCDP-Rand",
                 "PAUP*",
                 "PAUP*-SC",
                 "StarCDP-SC",
                 "Startle-NNI (C++)",
                 "LAML"]

        sys.stdout.write("\\multicolumn{9}{l}{\\textit{Precision = TP / (TP + FP)}} \\\\[0.25em]\n")
        for miss in [0, 25, 50, 75, 100]:
            report_accuracy_fp_stats(df, mthds, contract, miss, "PRECISION")

        sys.stdout.write("\\multicolumn{9}{l}{\\textit{Recall = TP / (TP + FN)}} \\\\[0.25em]\n")
        for miss in [0, 25, 50, 75, 100]:
            report_accuracy_fp_stats(df, mthds, contract, miss, "RECALL")

        sys.stdout.write("\\multicolumn{9}{l}{\\textit{f1-score}} \\\\[0.25em]\n")
        for miss in [0, 25, 50, 75, 100]:
            report_accuracy_fp_stats(df, mthds, contract, miss, "F1SCORE")

        sys.stdout.write("\\midrule\n")
        sys.stdout.write("\\multicolumn{9}{l}{\\textit{Runtime (in seconds)}} \\\\[0.25em]\n")
        for miss in [0, 25, 50, 75, 100]:
            report_runtime_stats(df, mthds, contract, miss)

        sys.stdout.write("\\bottomrule\n")
        sys.stdout.write("\\end{tabular}\n")
        sys.stdout.write("\\end{table}\n")

