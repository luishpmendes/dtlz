import csv
import matplotlib.pyplot as plt
import seaborn as sns
import ptitprince as pt
import os
import statistics as stats
from plotter_definitions import *

dirname = os.path.dirname(__file__)

min_multiplicative_epsilon = 1.0
max_multiplicative_epsilon = 0.0
for dtlz in dtlzs:
    for n in ns:
        for m in ms:
            for solver in solvers:
                filename = os.path.join(dirname, "multiplicative_epsilon/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solver + ".txt")
                with open(filename) as csv_file:
                    data = csv.reader(csv_file)
                    for row in data:
                        min_multiplicative_epsilon = min(min_multiplicative_epsilon, float(row[0]))
                        max_multiplicative_epsilon = max(max_multiplicative_epsilon, float(row[0]))
delta_multiplicative_epsilon = max_multiplicative_epsilon - min_multiplicative_epsilon
min_multiplicative_epsilon = max(min_multiplicative_epsilon - round(0.025 * delta_multiplicative_epsilon), 0.00)
max_multiplicative_epsilon = min(max_multiplicative_epsilon + round(0.025 * delta_multiplicative_epsilon), 1.00)

for dtlz in dtlzs:
    for n in ns:
        for m in ms:
            plt.figure(figsize = (11, 11))
            plt.title("DTLZ" + str(dtlz) + "_" + str(n) + "_" + str(m), fontsize = "xx-large")
            plt.xlabel("Multiplicative Epsilon Indicator", fontsize = "x-large")
            xs = []
            for solver in solvers:
                filename = os.path.join(dirname, "multiplicative_epsilon/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solver + ".txt")
                x = []
                with open(filename) as csv_file:
                    data = csv.reader(csv_file)
                    for row in data:
                        x.append(float(row[0]))
                xs.append(x)
            pt.half_violinplot(data = xs, palette = colors, orient = "h", width = 0.6, cut = 0.0, inner = None)
            sns.stripplot(data = xs, palette = colors, orient = "h", size = 2, zorder = 0)
            sns.boxplot(data = xs, orient = "h", width = 0.20, color = "black", zorder = 10, showcaps = True, boxprops = {'facecolor' : 'none', "zorder" : 10}, showfliers = True, whiskerprops = {'linewidth' : 2, "zorder" : 10}, flierprops = {'markersize' : 2})
            plt.yticks(ticks = list(range(len(solvers))), labels = [solver_labels[solver] for solver in solvers], fontsize = "large")
            filename = os.path.join(dirname, "multiplicative_epsilon/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + ".png")
            plt.savefig(filename, format = "png")
            plt.close()

for dtlz in dtlzs:
    plt.figure(figsize = (11, 11))
    plt.title("DTLZ" + str(dtlz), fontsize = "xx-large")
    plt.xlabel("Multiplicative Epsilon Indicator", fontsize = "x-large")
    xs = []
    for solver in solvers:
        x = []
        for n in ns:
            for m in ms:
                filename = os.path.join(dirname, "multiplicative_epsilon/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solver + ".txt")
                with open(filename) as csv_file:
                    data = csv.reader(csv_file)
                    for row in data:
                        x.append(float(row[0]))
        xs.append(x)
    pt.half_violinplot(data = xs, palette = colors, orient = "h", width = 0.6, cut = 0.0, inner = None)
    sns.stripplot(data = xs, palette = colors, orient = "h", size = 2, zorder = 0)
    sns.boxplot(data = xs, orient = "h", width = 0.20, color = "black", zorder = 10, showcaps = True, boxprops = {'facecolor' : 'none', "zorder" : 10}, showfliers = True, whiskerprops = {'linewidth' : 2, "zorder" : 10}, flierprops = {'markersize' : 2})
    plt.yticks(ticks = list(range(len(solvers))), labels = [solver_labels[solver] for solver in solvers], fontsize = "large")
    filename = os.path.join(dirname, "multiplicative_epsilon/dtlz" + str(dtlz) + ".png")
    plt.savefig(filename, format = "png")
    plt.close()

multiplicative_epsilon = []

for solver in solvers:
    multiplicative_epsilon.append([])

for dtlz in dtlzs:
    for n in ns:
        for m in ms:
            for i in range(len(solvers)):
                for seed in seeds:
                    filename = os.path.join(dirname, "multiplicative_epsilon/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solvers[i] + "_" + str(seed) + ".txt")
                    if os.path.exists(filename):
                        with open(filename) as csv_file:
                            data = csv.reader(csv_file, delimiter = ",")
                            for row in data:
                                multiplicative_epsilon[i].append(float(row[0]))
                            csv_file.close()

plt.figure(figsize = (11, 11))
plt.title("DTLZ", fontsize = "xx-large")
plt.xlabel("Multiplicative Epsilon Indicator", fontsize = "x-large")
pt.half_violinplot(data = multiplicative_epsilon, palette = colors, orient = "h", width = 0.6, cut = 0.0, inner = None)
sns.stripplot(data = multiplicative_epsilon, palette = colors, orient = "h", size = 2, zorder = 0)
sns.boxplot(data = multiplicative_epsilon, orient = "h", width = 0.20, color = "black", zorder = 10, showcaps = True, boxprops = {'facecolor' : 'none', "zorder" : 10}, showfliers = True, whiskerprops = {'linewidth' : 2, "zorder" : 10}, flierprops = {'markersize' : 2})
plt.yticks(ticks = list(range(len(solvers))), labels = [solver_labels[solver] for solver in solvers], fontsize = "large")
filename = os.path.join(dirname, "multiplicative_epsilon/multiplicative_epsilon.png")
plt.savefig(filename, format = "png")
plt.close()

multiplicative_epsilon_per_n = {}

for solver in solvers:
    multiplicative_epsilon_per_n[solver] = {}
    for n in ns:
        multiplicative_epsilon_per_n[solver][n] = []

for n in ns:
    for dtlz in dtlzs:
        for m in ms:
            for solver in solvers:
                for seed in seeds:
                    filename = os.path.join(dirname, "multiplicative_epsilon/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solvers + "_" + str(seed) + ".txt")
                    if os.path.exists(filename):
                        with open(filename) as csv_file:
                            data = csv.reader(csv_file, delimiter = ",")
                            for row in data:
                                multiplicative_epsilon_per_n[solver][n].append(float(row[0]))
                            csv_file.close()

plt.figure()
plt.title("DTLZ", fontsize = "xx-large")
plt.xlabel("n", fontsize = "x-large")
plt.ylabel("Multiplicative Epsilon Indicator", fontsize = "x-large")
plt.xticks(ns)
for i in range(len(solvers)):
    y = []
    for n in ns:
        y.append(stats.mean(multiplicative_epsilon_per_n[solvers[i]][n]))
    plt.plot(ns, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.xlim(left = max(min(ns) - 1, 0), right = max(ns) + 1)
plt.ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
plt.legend(loc = "best", fontsize = "large")
filename = os.path.join(dirname, "multiplicative_epsilon/multiplicative_epsilon_mean_per_n.png")
plt.savefig(filename, format = "png")
plt.close()

plt.figure()
plt.title("DTLZ", fontsize = "xx-large")
plt.xlabel("n", fontsize = "x-large")
plt.ylabel("Multiplicative Epsilon Indicator", fontsize = "x-large")
plt.xticks(ns)
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for n in ns:
        quantiles = stats.quantiles(multiplicative_epsilon_per_n[solvers[i]][n])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(ns, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for n in ns:
        quantiles = stats.quantiles(multiplicative_epsilon_per_n[solvers[i]][n])
        y1.append(quantiles[1])
    plt.plot(ns, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.xlim(left = max(min(ns) - 1, 0), right = max(ns) + 1)
plt.ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
plt.legend(loc = "best", fontsize = "large")
filename = os.path.join(dirname, "multiplicative_epsilon/multiplicative_epsilon_quartiles_per_n.png")
plt.savefig(filename, format = "png")
plt.close()

multiplicative_epsilon_per_m = {}

for solver in solvers:
    multiplicative_epsilon_per_m[solver] = {}
    for m in ms:
        multiplicative_epsilon_per_m[solver][m] = []

for m in ms:
    for dtlz in dtlzs:
        for n in ns:
            for solver in solvers:
                for seed in seeds:
                    filename = os.path.join(dirname, "multiplicative_epsilon/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solvers + "_" + str(seed) + ".txt")
                    if os.path.exists(filename):
                        with open(filename) as csv_file:
                            data = csv.reader(csv_file, delimiter = ",")
                            for row in data:
                                multiplicative_epsilon_per_m[solver][m].append(float(row[0]))
                            csv_file.close()

plt.figure()
plt.title("DTLZ", fontsize = "xx-large")
plt.xlabel("m", fontsize = "x-large")
plt.ylabel("Multiplicative Epsilon Indicator", fontsize = "x-large")
plt.xticks(ms)
for i in range(len(solvers)):
    y = []
    for m in ms:
        y.append(stats.mean(multiplicative_epsilon_per_m[solvers[i]][m]))
    plt.plot(ms, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.xlim(left = max(min(ms) - 1, 0), right = max(ms) + 1)
plt.ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
plt.legend(loc = "best", fontsize = "large")
filename = os.path.join(dirname, "multiplicative_epsilon/multiplicative_epsilon_mean_per_m.png")
plt.savefig(filename, format = "png")
plt.close()

plt.figure()
plt.title("DTLZ", fontsize = "xx-large")
plt.xlabel("m", fontsize = "x-large")
plt.ylabel("Multiplicative Epsilon Indicator", fontsize = "x-large")
plt.xticks(ms)
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for m in ms:
        quantiles = stats.quantiles(multiplicative_epsilon_per_m[solvers[i]][m])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(ms, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for m in ms:
        quantiles = stats.quantiles(multiplicative_epsilon_per_m[solvers[i]][m])
        y1.append(quantiles[1])
    plt.plot(ms, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.xlim(left = max(min(ms) - 1, 0), right = max(ms) + 1)
plt.ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
plt.legend(loc = "best", fontsize = "large")
filename = os.path.join(dirname, "multiplicative_epsilon/multiplicative_epsilon_quartiles_per_m.png")
plt.savefig(filename, format = "png")
plt.close()
