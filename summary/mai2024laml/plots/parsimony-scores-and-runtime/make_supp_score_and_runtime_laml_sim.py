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

tableau20 =  purple + pink  + lightblue + brown  + orange + green
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

    mthds = ["Cassiopeia-Greedy",
             "StarCDP-Bias",
             "StarCDP-Rand",
             "PAUP*",
             "Startle-NNI (C++)",
             "LAML"]
    m = len(mthds)

    box_pos = numpy.arange(1, m+1)
    print(box_pos)

    fig = plt.figure(figsize=(14.4, 4.25))

    gs = gridspec.GridSpec(1,2)

    ax00 = plt.subplot(gs[0,0])  ## 0.0
    ax01 = plt.subplot(gs[0,1])  ## 0.05

    grid = [ax00, ax01]

    for i in range(len(grid)):
        ax = grid[i]

        # Collect data
        vals = [None] * n
        for j, modl in enumerate(modls):
            vals[j] = []
            for k, mthd in enumerate(mthds):
                ydf = df[(df["LABL"] == modl) &
                             (df["MTHD"] == mthd) &
                             (df["CONTRACT"] == "NONE")]
                ydf = ydf.sort_values(by=["REPL"], ascending=True)

                if i == 0:
                    val = ydf["NORM_PSCORE"].values
                    yticks = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8]
                    ydraws = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8]
                    ax.set_ylabel(r"Norm SHP score", fontsize=18)
                else:
                    val = ydf["SECS"].values / 60
                    yticks = [0, 50, 100, 150, 200, 250, 300]
                    ydraws = [-10, 0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300]
                    ax.set_ylabel(r"Runtime (min)", fontsize=18)

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
    gs.tight_layout(fig, rect=[0, 0.125, 1, 1])

    ax = grid[-1]
    hs = []
    for k in range(len(mthds)):
        print(mthds[k])
        h, = ax.plot([1], [1], '-', color=tableau20[k*2], lw=10)
        hs.append(h)

    ax.legend(hs, mthds, 
              frameon=False,
              ncol=6, 
              fontsize=16,
              loc='lower center', 
              bbox_to_anchor=(-0.08, -0.525))

    # # Save plot
    plt.savefig(output, format='pdf', dpi=300)


# Read and plot data
df = pandas.read_csv("../../csvs/data-mai2024laml.csv")
make_figure(df, "laml-sim-supp-pscore-and-runtime.pdf")
