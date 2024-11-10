import pandas
import numpy
import sys


def report_error_stats(df, mthds, nlin, nchr, emet):
    minval = 500

    sys.stdout.write("%d & %d" % (nlin, nchr))

    xdf = df[(df["NLIN"] == nlin) &
             (df["NCHR"] == nchr)]

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
    for i, x in enumerate(keep_avg):
        if i in minind:
            sys.stdout.write(" & $\\mathbf{%1.1f \\pm %1.1f}$" % (keep_avg[i], keep_std[i]))
        else:
            sys.stdout.write(" & $%1.1f \\pm %1.1f$" % (keep_avg[i], keep_std[i]))

    sys.stdout.write(" \\\\\n")


def report_accuracy_stats(df, mthds, nlin, nchr, amet):
    maxval = 0

    sys.stdout.write("%d & %d" % (nlin, nchr))

    xdf = df[(df["NLIN"] == nlin) &
             (df["NCHR"] == nchr)]

    keep_avg = []
    keep_std = []
    for ind, mthd in enumerate(mthds):
        if amet == "TP":
            vals = xdf[(xdf["MTHD"] == mthd)].TP.values
        else:
            sys.exit("Unknown error metric\n")

        if (len(vals) < 18) or (len(vals) > 21):
            print(vals)
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
    df = pandas.read_csv("../csvs/data-sashittal2023startle-shcontract.csv",
                         na_values='NA', keep_default_na=False)

    sys.stdout.write("\\begin{table}[!h]\n")
    sys.stdout.write("\\caption[")
    sys.stdout.write("Tree error for Startle simulated data sets]{\\textbf{Tree error for Startle simulated data sets.} ")
    sys.stdout.write("Mean $\\pm$ standard deviations are across replicates for each method. Tree error merics were computed after SH-contraction of both the true and estimated trees.}\n")
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

    sys.stdout.write("\\multicolumn{12}{l}{\\textit{RF distance = FN + FP}} \\\\[0.25em]\n")
    for nlin in [50, 100, 150, 200]:
        for nchr in [10, 20, 30]:
            report_error_stats(df, mthds, nlin, nchr, "RF")

    sys.stdout.write("\\midrule\n")
    sys.stdout.write("\\multicolumn{12}{l}{\\textit{Number of false negative (FN) branches/clades}} \\\\[0.25em]\n")
    for nlin in [50, 100, 150, 200]:
        for nchr in [10, 20, 30]:
            report_error_stats(df, mthds, nlin, nchr, "FN")

    sys.stdout.write("\\midrule\n")
    sys.stdout.write("\\multicolumn{12}{l}{\\textit{Number of false positive (FP) branches/clades}} \\\\[0.25em]\n")
    for nlin in [50, 100, 150, 200]:
        for nchr in [10, 20, 30]:
            report_error_stats(df, mthds, nlin, nchr, "FP")
    
    sys.stdout.write("\\midrule\n")
    sys.stdout.write("\\multicolumn{12}{l}{\\textit{Number of true positive (TP) branches/clades}} \\\\[0.25em]\n")
        
    for nlin in [50, 100, 150, 200]:
        for nchr in [10, 20, 30]:
            report_accuracy_stats(df, mthds, nlin, nchr, "TP")

    sys.stdout.write("\\bottomrule\n")
    sys.stdout.write("\\end{tabular}\n")
    sys.stdout.write("\\end{table}\n")
