import pandas
import numpy
import sys

def report_error_stats(df, mthds, contract, miss, emet):
    minval = 500

    sys.stdout.write("%d" % (miss))

    xdf = df[(df["CONTRACT"] == contract) &
             (df["SILENCING"] == miss)]

    keep_avg = []
    keep_std = []
    for ind, mthd in enumerate(mthds):
        if emet == "RF":
            vals = xdf[(xdf["MTHD"] == mthd)].RF.values
        elif emet == "FP":
            vals = xdf[(xdf["MTHD"] == mthd)].FP.values
        elif emet == "FN":
            vals = xdf[(xdf["MTHD"] == mthd)].FN.values
        else:
            sys.exit("Unknown error metric\n")

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
    for i, x in enumerate(keep_avg):
        if i in minind:
            sys.stdout.write(" & $\\mathbf{%1.1f \\pm %1.1f}$" % (keep_avg[i], keep_std[i]))
        else:
            sys.stdout.write(" & $%1.1f \\pm %1.1f$" % (keep_avg[i], keep_std[i]))

    sys.stdout.write(" \\\\\n")


def report_accuracy_stats(df, mthds, contract, miss, amet):
    maxval = 0

    sys.stdout.write("%d" % (miss))

    xdf = df[(df["CONTRACT"] == contract) &
             (df["SILENCING"] == miss)]

    keep_avg = []
    keep_std = []
    for ind, mthd in enumerate(mthds):
        if amet == "TP":
            vals = xdf[(xdf["MTHD"] == mthd)].TP.values
        else:
            sys.exit("Unknown error metric\n")

        if len(vals) != 50:
            sys.exit("Wrong number of replicates")

        x = round(round(numpy.mean(vals), 2), 1)
        y = round(round(numpy.std(vals), 2), 1)
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
            sys.stdout.write("Tree error (no contraction) for LAML simulated data sets]{\\textbf{Tree error (\\textbf{no contraction}) for LAML simulated data sets with 250 cells.} ")
        else:
            sys.stdout.write("Tree error (SH contraction) for LAML simulated data sets]{\\textbf{Tree error (\\textbf{SH contraction}) for LAML simulated data sets with 250 cells.} ")
        sys.stdout.write("Mean $\\pm$ standard deviations are across 50 replicates for each method.}\n")
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

        sys.stdout.write("\\multicolumn{9}{l}{\\textit{RF distance = \\# FN + \\# FP}} \\\\[0.25em]\n")
        for miss in [0, 25, 50, 75, 100]:
            report_error_stats(df, mthds, contract, miss, "RF")

        sys.stdout.write("\\midrule\n")
        sys.stdout.write("\\multicolumn{9}{l}{\\textit{Number of false negative (FN) branches}} \\\\[0.25em]\n")
        for miss in [0, 25, 50, 75, 100]:
            report_error_stats(df, mthds, contract, miss, "FN")

        sys.stdout.write("\\midrule\n")
        sys.stdout.write("\\multicolumn{9}{l}{\\textit{Number of false positive (FP) branches}} \\\\[0.25em]\n")
        for miss in [0, 25, 50, 75, 100]:
            report_error_stats(df, mthds, contract, miss, "FP")

        sys.stdout.write("\\midrule\n")
        sys.stdout.write("\\multicolumn{9}{l}{\\textit{Number of true positive (TP) branches}} \\\\[0.25em]\n")
        
        for miss in [0, 25, 50, 75, 100]:
            report_accuracy_stats(df, mthds, contract, miss, "TP")

        sys.stdout.write("\\bottomrule\n")
        sys.stdout.write("\\end{tabular}\n")
        sys.stdout.write("\\end{table}\n")
