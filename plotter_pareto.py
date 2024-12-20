import csv
import matplotlib.pyplot as plt
import os
import seaborn as sns
from plotter_definitions import *

dirname = os.path.dirname(__file__)

for dtlz in dtlzs:
    for n in ns:
        for m in ms:
            for version in versions:
                min_ys = []
                max_ys = []
                for i in range(2):
                    min_ys.append(-1)
                    max_ys.append(-1)
                for solver in solvers:
                    filename = os.path.join(dirname, "pareto/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solver + "_" + version + ".txt")
                    if os.path.exists(filename):
                        with open(filename) as csv_file:
                            data = csv.reader(csv_file, delimiter=" ")
                            for row in data:
                                for i in range(2):
                                    if min_ys[i] == -1 or min_ys[i] > float(row[i]):
                                        min_ys[i] = float(row[i])
                                    if max_ys[i] == -1 or max_ys[i] < float(row[i]):
                                        max_ys[i] = float(row[i])
                            csv_file.close()
                for i in range(2):
                    delta_y = max_ys[i] - min_ys[i]
                    min_ys[i] = min_ys[i] - round(0.025 * delta_y)
                    max_ys[i] = max_ys[i] + round(0.025 * delta_y)
                fig, axs = plt.subplots(nrows = 2, ncols = 2, figsize = (5.0 * 2, 5.0 * 2), squeeze = False, num = 1, clear = True)
                fig.set_size_inches(5.0 * 2, 5.0 * 2)
                fig.suptitle("dtlz" + str(dtlz), fontsize = "xx-large")
                for i in range(len(solvers)):
                    filename = os.path.join(dirname, "pareto/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solver + "_" + version + ".txt")
                    if os.path.exists(filename):
                        ys = []
                        for j in range(2):
                            ys.append([])
                        with open(filename) as csv_file:
                            data = csv.reader(csv_file, delimiter = " ")
                            for row in data:
                                for j in range(2):
                                    ys[j].append(float(row[j]))
                            csv_file.close()
                        for j in range(2):
                            axs[j][j].set_xlim(left = min_ys[j], right = max_ys[j])
                            axs[j][j].set_xlabel(xlabel = "$f_{" + str(j + 1) + "}$", fontsize = "x-large")
                            axs[j][j].set_yticks([])
                            axs[j][j].set_ylabel(ylabel = "Density", fontsize = "x-large")
                            sns.kdeplot(data = ys[j], ax = axs[j][j], color = colors[i], label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), alpha = 0.80)
                            axs[j][j].legend(loc = "best")
                            for l in range(2):
                                if j != l:
                                    axs[j][l].set_xlim(left = min_ys[l], right = max_ys[l])
                                    axs[j][l].set_ylim(bottom = min_ys[j], top = max_ys[j])
                                    axs[j][l].set_xlabel(xlabel = "$f_{" + str(l + 1) + "}$", fontsize = "x-large")
                                    axs[j][l].set_ylabel(ylabel = "$f_{" + str(j + 1) + "}$", fontsize = "x-large")
                                    axs[j][l].scatter(x = ys[l], y = ys[j], color = colors[i], label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), alpha = 0.80)
                                    axs[j][l].legend(loc = "best", fontsize = "large")
                        del ys
                plt.subplots_adjust(wspace = 0.16 + 0.07 * 2, hspace = 0.16 + 0.07 * 2)
                filename = os.path.join(dirname, "pareto/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + version + ".png")
                plt.savefig(filename, format = "png")
