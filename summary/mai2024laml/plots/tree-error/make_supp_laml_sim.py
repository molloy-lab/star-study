import numpy
import pandas
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import rc
import sys


plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{helvet} \usepackage{sfmath}')


letters = [r"\textbf{a)}", 
           r"\textbf{b)}", 
           r"\textbf{c)}", 
           r"\textbf{d)}", 
           r"\textbf{e)}", 
           r"\textbf{f)}",
           r"\textbf{g)}", 
           r"\textbf{h)}", 
           r"\textbf{i)}"]

upperletters = [r"\textbf{A}", 
                r"\textbf{B}", 
                r"\textbf{C}", 
                r"\textbf{D}", 
                r"\textbf{E}", 
                r"\textbf{F}",
                r"\textbf{G}", 
                r"\textbf{H}", 
                r"\textbf{I}",]

# Tableau 20 colors in RGB.
darkblue = [(31, 119, 180), (174, 199, 232)]
orange = [(255, 127, 14), (255, 187, 120)]
green = [(44, 160, 44), (152, 223, 138)]
red = [(214, 39, 40), (255, 152, 150)]
purple = [(148, 103, 189), (197, 176, 213)]
brown = [(140, 86, 75), (196, 156, 148)]
pink = [(227, 119, 194), (247, 182, 210)]
gray = [(127, 127, 127), (199, 199, 199)]
yellow = [(188, 189, 34), (219, 219, 141)]
lightblue = [(23, 190, 207), (158, 218, 229)]

tableau20 =  pink  + lightblue + brown  + gray + darkblue + orange + green
print(tableau20)

# Map RGB values to the [0, 1]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)


# Color grouped boxplots
def setBoxColors(bp):
    n = len(bp['boxes'])
    for i in range(n):
        j = i

        plt.setp(bp['boxes'][i], 
                 color=tableau20[j*2],
                 linewidth=1.75)
        plt.setp(bp['boxes'][i], 
                 facecolor=tableau20[j*2+1])
        plt.setp(bp['caps'][i*2:i*2+2],
                 color=tableau20[j*2],
                 linewidth=1.75)
        plt.setp(bp['whiskers'][i*2:i*2+2],
                 color=tableau20[j*2],
                 linewidth=1.75,
                 linestyle='-')
        plt.setp(bp['medians'][i],
                 color=[0.3, 0.3, 0.3],
                 linewidth=1.75)
                 #color=tableau20[i*2], linewidth=1.75)
        plt.setp(bp['means'][i],
                 markerfacecolor=[0.3, 0.3, 0.3],
                 markeredgecolor=[0.3, 0.3, 0.3],
                 markersize=3)
        #plt.setp(bp['fliers'][i], marker=".",
        #         markerfacecolor=[0.3, 0.3, 0.3],
        #         markeredgecolor=[0.3, 0.3, 0.3],
        #         markersize=4)


# https://stackoverflow.com/questions/25812255/row-and-column-headers-in-matplotlibs-subplots
# https://stackoverflow.com/questions/27426668/row-titles-for-matplotlib-subplot


def make_figure(df, output):
    modls = ["0%", "25%", "50%", "75%", "100%"]
    n = len(modls)

    mthds = [#"Cassiopeia-Greedy",
             "StarCDP-Bias",
             "StarCDP-Rand",
             "PAUP*",
             "PAUP*-SC",
             "StarCDP-SC",
             "Startle-NNI (C++)",
             "LAML"]
    m = len(mthds)

    box_pos = numpy.arange(1, m+1)
    print(box_pos)

    fig = plt.figure(figsize=(14.4, 12))

    gs = gridspec.GridSpec(4, 2)

    ax00 = plt.subplot(gs[0,0])
    ax01 = plt.subplot(gs[0,1])

    ax10 = plt.subplot(gs[1,0])
    ax11 = plt.subplot(gs[1,1])

    ax20 = plt.subplot(gs[2,0])
    ax21 = plt.subplot(gs[2,1])

    ax30 = plt.subplot(gs[3,0])
    ax31 = plt.subplot(gs[3,1])

    grid = [ax00, ax01, 
            ax10, ax11,
            ax20, ax21,
            ax30, ax31]

    for i in range(len(grid)):
        ax = grid[i]

        # Collect data
        vals = [None] * n
        for j, modl in enumerate(modls):
            vals[j] = []
            for k, mthd in enumerate(mthds):
                if i % 2 == 0:
                    ydf = df[(df["LABL"] == modl) &
                             (df["MTHD"] == mthd) &
                             (df["CONTRACT"] == "NONE")]
                else:
                    ydf = df[(df["LABL"] == modl) &
                             (df["MTHD"] == mthd) &
                             (df["CONTRACT"] == "SH")]
                ydf = ydf.sort_values(by=["REPL"], ascending=True)

                if i < 2:
                    val = ydf["RF"].values
                    yticks = [0, 50, 100, 150, 200, 250, 300, 350, 400]
                    ydraws = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400]
                    if i == 0:
                        ax.set_ylabel(r"RF", fontsize=18)
                    elif i == 1:
                        ax.set_ylabel(r"RF, SH-contract", fontsize=18)
                elif i < 4:
                    val = ydf["FP"].values
                    yticks = [0, 25, 50, 75, 100, 125, 150, 175, 200]
                    ydraws = [0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100, 112.5, 125, 137.5, 150, 162.5, 175, 187.5, 200]
                    if i == 2:
                        ax.set_ylabel(r"\# FP branches", fontsize=18)
                    elif i == 3:
                        ax.set_ylabel(r"FP, SH-contract", fontsize=18)
                elif i < 6:
                    val = ydf["TP"].values
                    yticks = [25, 50, 75, 100, 125, 150, 175, 200, 225]
                    ydraws = [25, 37.5, 50, 62.5, 75, 87.5, 100, 112.5, 125, 137.5, 150, 162.5, 175, 187.5, 200, 212.5, 225]
                    if i == 4:
                        ax.set_ylabel(r"\# TP branches", fontsize=18)
                    elif i == 5:
                        ax.set_ylabel(r"TP, SH-contract", fontsize=18)
                else:
                    val = ydf["F1SCORE"].values
                    yticks = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
                    ydraws = [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
                    if i == 6:
                        ax.set_ylabel(r"f1-score", fontsize=18)
                    elif i == 7:
                        ax.set_ylabel(r"f1-score, SH-contract", fontsize=18)                   

                nrep = len(val)
                if nrep != 50:
                    sys.stdout.write("Found %d replicates - some are missing!\n" % nrep)

                vals[j].append(list(val))

        # Plot data
        xs = []
        ys = []
        inds = modls
        for ind, val in zip(inds, vals):
            if val != []:
                xs.append(ind)
                ys.append(val)
        labs = modls
        vals = ys

        xminor = []
        xmajor = []
        base = numpy.arange(1, m + 1) 
        for j, modl in enumerate(modls):
            pos = base + ((m + 1) * j)
            xminor = xminor + list(pos)
            xmajor = xmajor + [numpy.mean(pos)]
            bp = ax.boxplot(vals[j],
                             positions=pos,
                             widths=0.75,
                             showfliers=False,
                             showmeans=True,
                             patch_artist=True)
            setBoxColors(bp)

        # X tick labels
        ax.tick_params(axis='x', labelsize=18)
        ax.set_xlim(xminor[0]-1, xminor[-1]+1)
        ax.set_xticks(xmajor)
        ax.set_xticklabels(modls)

        # Set labels
        ax.set_title(letters[i],
                     fontdict={'horizontalalignment':'center'},
                     x=0.0, y=1.05, fontsize=18)
            
        ax.tick_params(axis='x', labelsize=16)
        if i > 5:
            ax.set_xlabel(r"\% missing data from silencing (vs. dropout)", fontsize=18)

        # Y ticks            
        ymin = ydraws[0]
        ymax = ydraws[-1]
        ax.set_ylim(ymin, ymax)
        ax.set_yticks(yticks)
        ax.tick_params(axis='y', labelsize=14)

        # Add horizontal line
        xs = numpy.arange(xminor[0]-1, xminor[-1]+2)
        for y in ydraws[1:]:
            ax.plot(xs, [y] * len(xs), "--", dashes=(3, 3), lw=0.5, color="black", alpha=0.3)

        # Set plot axis parameters
        ax.tick_params(axis=u'both', which=u'both',length=0) # removes tiny ticks
        ax.get_xaxis().tick_bottom() 
        ax.get_yaxis().tick_left()

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # Add legend at bottom
    gs.tight_layout(fig, rect=[0, 0.075, 1, 1])

    ax = grid[-1]
    hs = []
    for k in range(len(mthds)):
        print(mthds[k])
        h, = ax.plot([1], [1], '-', color=tableau20[k*2], lw=10)
        hs.append(h)

    hsx = [hs[0], hs[4],
           hs[1], hs[5], 
           hs[2], hs[6],
           hs[3]]
    mthdsx = [mthds[0], mthds[4], 
              mthds[1], mthds[5],
              mthds[2], mthds[6], 
              mthds[3]]

    ax.legend(hsx, mthdsx, 
              frameon=False,
              ncol=4, 
              fontsize=16,
              loc='lower center', 
              bbox_to_anchor=(-0.065, -0.85))

    # # Save plot
    plt.savefig(output, format='pdf', dpi=300)


# Read and plot data
df = pandas.read_csv("../../csvs/data-mai2024laml.csv")
make_figure(df, "laml-sim-supp.pdf")

"""
Information on RF distance
In [1]: (248 + 248) * 0.2
Out[1]: 99.2

In [2]: (248 + 248) * 0.3
Out[2]: 148.79999999999998

In [3]: (248 + 248) * 0.4
Out[3]: 198.4

In [4]: (248 + 248) * 0.5
Out[4]: 248.0

In [5]: (248 + 248) * 0.6
Out[5]: 297.59999999999997

In [6]: (248 + 248) * 0.7
Out[6]: 347.2

In [1]: (248 + 248) * 0.8
Out[1]: 396.8

In [2]: (248 + 248) * 0.9
Out[2]: 446.40000000000003
"""
