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

tableau20 =  orange + green + purple + lightblue + pink + brown + yellow  + red + darkblue+ gray
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
    modls = ["50x10", "100x20", "200x30"]
    n = len(modls)

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
    m = len(mthds)

    box_pos = numpy.arange(1, m+1)
    print(box_pos)
    nlins = [50, 100, 150, 200]

    fig = plt.figure(figsize=(14.4, 8))

    gs = gridspec.GridSpec(2,2)

    ax00 = plt.subplot(gs[0,0])
    ax01 = plt.subplot(gs[0,1])
    ax10 = plt.subplot(gs[1,0])
    ax11 = plt.subplot(gs[1,1])

    grid = [ax00, ax01, ax10, ax11]

    for i in range(len(grid)):
        ax = grid[i]

        # Collect data
        vals = [None] * n
        for j, modl in enumerate(modls):
            vals[j] = []
            for k, mthd in enumerate(mthds):
                ydf = df[(df["LABL"] == modl) &
                         (df["MTHD"] == mthd)]
                ydf = ydf.sort_values(by=["REPL"], ascending=True)

                if i == 0:
                    ax.set_ylabel(r"RF = \#FN + \#FP", fontsize=18)
                    val = ydf["RF"].values
                    yticks = [0,  20, 40, 60, 80, 100]
                    ydraws = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
                elif i == 1:
                    ax.set_ylabel(r"\# FP branches", fontsize=18)
                    val = ydf["FP"].values
                    yticks = [0, 10, 20, 30, 40, 50, 60]
                    ydraws = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
                elif i == 2:
                    ax.set_ylabel(r"\# TP branches", fontsize=18)
                    val = ydf["TP"].values
                    yticks = [0, 10, 20, 30, 40, 50, 60, 70, 80]
                    ydraws = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
                else:
                    ax.set_ylabel(r"f1-score", fontsize=18)
                    val = ydf["F1SCORE"].values
                    yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
                    ydraws = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

                nrep = len(val)
                if nrep != 21:
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
        if (i == 2) or (i == 3):
            ax.set_xlabel(r"\# cells x \# characters", fontsize=18)

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
    gs.tight_layout(fig, rect=[0, 0.125, 1, 1])

    ax = grid[3]
    hs = []
    for k in range(len(mthds)):
        print(mthds[k])
        h, = ax.plot([1], [1], '-', color=tableau20[k*2], lw=10)
        hs.append(h)

    hsx = [hs[0], hs[5],
           hs[1], hs[6], 
           hs[2], hs[7],
           hs[3], hs[8], 
           hs[4], hs[9]]
    mthdsx = [mthds[0], mthds[5], 
              mthds[1], mthds[6],
              mthds[2], mthds[7], 
              mthds[3], mthds[8], 
              mthds[4], mthds[9]]

    ax.legend(hsx, mthdsx, 
              frameon=False,
              ncol=5, 
              fontsize=16,
              loc='lower center', 
              bbox_to_anchor=(-0.065, -0.65))

    # # Save plot
    plt.savefig(output, format='pdf', dpi=300)


# Read and plot data
df = pandas.read_csv("../../csvs/data-sashittal2023startle-shcontract.csv")
make_figure(df, "startle-sim-main.pdf")

#df = pandas.read_csv("../../csvs/data-sim-tree-error-c1-2.csv")
#make_figure(df, "tp-c1-2-2x2.pdf")
