import pandas
import numpy
import sys


def report_accuracy_fp_stats(df, mthds, nlin, nchr, amet):
    maxval = 0

    sys.stdout.write("%d & %d" % (nlin, nchr))

    xdf = df[(df["NLIN"] == nlin) &
             (df["NCHR"] == nchr)]

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

        if (len(vals) < 18) or (len(vals) > 21):
            print(vals)
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


def report_runtime_stats(df, mthds, nlin, nchr):
    minval = 172800

    sys.stdout.write("%d & %d" % (nlin, nchr))

    xdf = df[(df["NLIN"] == nlin) &
             (df["NCHR"] == nchr)]

    keep_avg = []
    keep_std = []
    for ind, mthd in enumerate(mthds):
        vals = xdf[(xdf["MTHD"] == mthd)].SECS.values

        if (len(vals) < 18) or (len(vals) > 21):
            print(vals)
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
    df = pandas.read_csv("../csvs/data-sashittal2023startle-shcontract.csv",
                         na_values='NA', keep_default_na=False)

    sys.stdout.write("\\begin{table}[!h]\n")
    sys.stdout.write("\\caption[")
    sys.stdout.write("Tree tree accuracy and runtime for Startle simulated data sets]{\\textbf{Tree accuracy and runtime (in seconds) for Startle simulated data sets.} ")
    sys.stdout.write("Mean $\\pm$ standard deviations are across replicates for each method. Tree accuracy metrics were computed after SH-contraction of both true and estimated trees.}\n")
    sys.stdout.write("\\label{tab:startle-sim}\n")
    sys.stdout.write("\\centering\n")
    sys.stdout.write("\\tiny\n")
    sys.stdout.write("\\begin{tabular}{c c c c c c c c c c c c}\n")
    sys.stdout.write("\\toprule \n")

    sys.stdout.write("\\# of & \\# of & Startle & LAML & Cassiopeia & StarCDP & StarCDP & PAUP* & Startle & Startle & StarCDP & PAUP* \\\\\n")
    sys.stdout.write("cells & chars & NNI (C++) & & Greedy & Rand & Bias & & NNI (Py) & ILP & SC & SC \\\\\n")
    sys.stdout.write("\\midrule\n")

    mthds = ["Startle-NNI (C++)",
             "LAML",
             "Cassiopeia-Greedy",
             "StarCDP-Rand",
             "StarCDP-Bias",
             "PAUP*",
             "Startle-NNI (Py)",
             "Startle-ILP",
             "StarCDP-SC",
             "PAUP*-SC"]

    sys.stdout.write("\\multicolumn{12}{l}{\\textit{Precision = TP / (TP + FP)}} \\\\[0.25em]\n")
    for nlin in [50, 100, 150, 200]:
        for nchr in [10, 20, 30]:
            report_accuracy_fp_stats(df, mthds, nlin, nchr, "PRECISION")

    sys.stdout.write("\\midrule\n")
    sys.stdout.write("\\multicolumn{12}{l}{\\textit{Recall = TP / (TP + FN)}} \\\\[0.25em]\n")
    for nlin in [50, 100, 150, 200]:
        for nchr in [10, 20, 30]:
            report_accuracy_fp_stats(df, mthds, nlin, nchr, "RECALL")

    sys.stdout.write("\\midrule\n")
    sys.stdout.write("\\multicolumn{12}{l}{\\textit{f1-score}} \\\\[0.25em]\n")
    for nlin in [50, 100, 150, 200]:
        for nchr in [10, 20, 30]:
            report_accuracy_fp_stats(df, mthds, nlin, nchr, "F1SCORE")

    sys.stdout.write("\\midrule\n")
    sys.stdout.write("\\multicolumn{9}{l}{\\textit{Runtime (in seconds)}} \\\\[0.25em]\n")
    for nlin in [50, 100, 150, 200]:
        for nchr in [10, 20, 30]:
            report_runtime_stats(df, mthds, nlin, nchr)

    sys.stdout.write("\\bottomrule\n")
    sys.stdout.write("\\end{tabular}\n")
    sys.stdout.write("\\end{table}\n")
