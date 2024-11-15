import pandas
import numpy
import sys


if __name__ == "__main__":
    pipelines = ["1a", "2a", "1b", "2b", "1c", "2c"]

    sys.stdout.write("\\begin{table}[!h]\n")
    sys.stdout.write("\\caption[Runtime for KP-Tracer tumors]")
    sys.stdout.write("{\\textbf{Runtime for KP-Tracer tumors.}}")
    sys.stdout.write("\\label{tab:kptracer-migration}\n")
    sys.stdout.write("\\centering\n")
    sys.stdout.write("\\tiny\n")
    sys.stdout.write("\\begin{tabular}{l c c c c c c c c}\n")
    sys.stdout.write("\\toprule \n")

    sys.stdout.write("Tumor & Analysis  & Startle   & StarCDP & StarCDP & StarCDP & PAUP* & PAUP*\\\\\n")
    sys.stdout.write("Data  & Pipeline  & NNI (C++) & Bias    & Rand    & SC      &       & SC\\\\\n")
    sys.stdout.write("\\midrule\n")

    mthds = ["startle_nni",
             "star_cdp_one_sol",
             "star_cdp_rand_sol",
             "star_cdp_sc",
             "paup_one_sol",
             "paup_sc"]

    for data in [3, 2, 1]:
        if data == 1:
            name = "3515\\_LKB1\\_T1\\_FAM"
            df = pandas.read_csv("../csvs/3515_Lkb1_T1_Fam_time_table.csv",
                                 na_values='NA', keep_default_na=False)
        elif data == 2:
            name = "3724\\_NT\\_All"
            df = pandas.read_csv("../csvs/3724_NT_All_time_table.csv",
                                 na_values='NA', keep_default_na=False)
        elif data == 3:
            name = "3513\\_NT\\_T1\\_Fam"
            df = pandas.read_csv("../csvs/3513_NT_T1_Fam_time_table.csv",
                                 na_values='NA', keep_default_na=False)
        else:
            sys.exit("Unrecognized data option")

        sys.stdout.write("\\multirow{6}{2cm}{%s}\n" % name)
        for pl in pipelines:
            sys.stdout.write("& %s" % pl)
            xdf = df[(df["pipeline"] == pl)]
            for mthd in mthds:
                vals = xdf[mthd].values
                if len(vals) != 1:
                    sys.exit("Something bad happened")
                elif vals[0] == '':
                    sys.stdout.write(" & NA")
                else:
                    sys.stdout.write(" & %1.1f" % round(round(float(vals[0]), 2), 1))
            sys.stdout.write(" \\\\\n")
        
        sys.stdout.write("\\midrule\n")

    sys.stdout.write("\\bottomrule\n")
    sys.stdout.write("\\end{tabular}\n")
    sys.stdout.write("\\end{table}\n\n")
