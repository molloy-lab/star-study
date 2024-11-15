import pandas
import numpy
import sys


if __name__ == "__main__":
    pipelines = ["1a", "2a", "1b", "2b", "1c", "2c"]

    for data in [3]:

        if data == 1:
            name = "3515\\_LKB1\\_T1\\_FAM"
            df = pandas.read_csv("../csvs/3515_Lkb1_T1_Fam_migration_table.csv",
                                 na_values='NA', keep_default_na=False)
            #This metastasis family has a primary tumor, with two lung mets and three kidney mets, as well as one lymph met; see Figure 7 in \cite{yang2022lineage}.
        elif data == 2:
            name = "3724\\_NT\\_All"
            df = pandas.read_csv("../csvs/3724_NT_All_migration_table.csv",
                                 na_values='NA', keep_default_na=False)
            #This metastasis family has a primary tumor, with three lung mets  as well as one soft tissue met; see Figure 7 in \cite{yang2022lineage}.
            #It was previously analyzed by Mai \textit{et al.} for the LAML \cite{mai2024maximum-laml} study.
            #Mai \textit{et al.} reported 119 migrations (56 reseedings) for the Startle-NNI (Python) tree, 99 migrations (42 reseedings) for the LAML tree, which starts its search from the Startle-NNI (Python) tree, 136 migrations (68 reseedings) for the Cassiopeia-Hybrid tree.
            #Our analysis also found 136 migrations (68 migrations) for pipeline 1a, although simply pruning and unpruning cells with missing data (as part of pipeline 2a) drops the number of migrations and reseedings down to 114 and 32, respectively, lowering the number of migrations and reseedings below those reported for the Startle-NNI (Python) tree.
        elif data == 3:
            name = "3513\\_NT\\_T1\\_Fam"
            df = pandas.read_csv("../csvs/3513_NT_T1_Fam_migration_table.csv",
                                 na_values='NA', keep_default_na=False)
        else:
            sys.exit("Unrecognized ata option")

        migrations = list(set(df["migration type"].tolist()))
        migrations.remove('migration')
        migrations.remove('reseeding')
        migrations.insert(0, "reseeding")
        migrations.insert(0, "migration")

        for x in migrations:
            if x[:3] == "Pri":
                print(x)
        exit()

        sys.stdout.write("\\begin{table}[!h]\n")
        sys.stdout.write("\\caption[Number of migrations inferred for KP-Tracer tumor %s]" % name)
        sys.stdout.write("{\\textbf{Number of migrations inferred for KP-Tracer tumor %s.}}" % name)
        sys.stdout.write("\\label{tab:kptracer-migration-%d}\n" % data)
        sys.stdout.write("\\centering\n")
        sys.stdout.write("\\tiny\n")
        sys.stdout.write("\\begin{tabular}{l c c c c c c c c}\n")
        sys.stdout.write("\\toprule \n")

        sys.stdout.write("Migration & Analysis & Cassiopeia & Startle   & StarCDP & StarCDP & StarCDP & PAUP* & PAUP*\\\\\n")
        sys.stdout.write("Type      & Pipeline & Hybrid     & NNI (C++) & Bias    & Rand    & SC      &       & SC\\\\\n")
        sys.stdout.write("\\midrule\n")

        mthds = ["Cassiopeia-Hybird",
                 "startle_nni",
                 "star_cdp_one_sol",
                 "star_cdp_rand_sol",
                 "star_cdp_sc",
                 "paup_one_sol",
                 "paup_sc"]

        for mg in migrations:
            sys.stdout.write("\\multirow{6}{2cm}{%s}\n" % mg.replace('->', '$\\mapsto$'))
            for pl in pipelines:
                sys.stdout.write("& %s" % pl)
                xdf = df[(df["migration type"] == mg) & (df["pipeline"] == pl)]
                for mthd in mthds:
                    vals = xdf[mthd].values
                    if len(vals) != 1:
                        sys.exit("Something bad happened")
                    elif vals[0] == '':
                        sys.stdout.write(" & NA")
                    else:
                        sys.stdout.write(" & %d" % int(vals[0]))
                sys.stdout.write(" \\\\\n")
            sys.stdout.write("\\midrule\n")

        sys.stdout.write("\\bottomrule\n")
        sys.stdout.write("\\end{tabular}\n")
        sys.stdout.write("\\end{table}\n\n")
