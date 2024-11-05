import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import seaborn as sns
import ptitprince as pt
import os
import statistics as stats
from plotter_definitions import *

dirname = os.path.dirname(__file__)

min_igd_plus = 1.0
max_igd_plus = 0.0
for dtlz in dtlzs:
    for n in ns:
        for m in ms:
            for solver in solvers:
                filename = os.path.join(dirname, "igd_plus/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solver + ".txt")
                with open(filename) as csv_file:
                    data = csv.reader(csv_file)
                    for row in data:
                        min_higd_plus = min(min_igd_plus, float(row[0]))
                        max_igd_plus = max(max_igd_plus, float(row[0]))
delta_igd_plus = max_igd_plus - min_igd_plus
min_igd_plus = max(min_igd_plus - round(0.025 * delta_igd_plus), 0.00)
max_igd_plus = min(max_igd_plus + round(0.025 * delta_igd_plus), 1.00)

for dtlz in dtlzs:
    for n in ns:
        for m in ms:
            plt.figure(figsize = (11, 11))
            plt.title("DTLZ" + str(dtlz) + "_" + str(n) + "_" + str(m), fontsize = "xx-large")
            plt.xlabel("Modified Inverted Generational Distance", fontsize = "x-large")
            xs = []
            for solver in solvers:
                filename = os.path.join(dirname, "igd_plus/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solver + ".txt")
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
            filename = os.path.join(dirname, "igd_plus/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + ".png")
            plt.savefig(filename, format = "png")
            plt.close()

for dtlz in dtlzs:
    plt.figure(figsize = (11, 11))
    plt.title("DTLZ" + str(dtlz), fontsize = "xx-large")
    plt.xlabel("Modified Inverted Generational Distance", fontsize = "x-large")
    xs = []
    for solver in solvers:
        x = []
        for n in ns:
            for m in ms:
                filename = os.path.join(dirname, "igd_plus/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solver + ".txt")
                with open(filename) as csv_file:
                    data = csv.reader(csv_file)
                    for row in data:
                        x.append(float(row[0]))
        xs.append(x)
    pt.half_violinplot(data = xs, palette = colors, orient = "h", width = 0.6, cut = 0.0, inner = None)
    sns.stripplot(data = xs, palette = colors, orient = "h", size = 2, zorder = 0)
    sns.boxplot(data = xs, orient = "h", width = 0.20, color = "black", zorder = 10, showcaps = True, boxprops = {'facecolor' : 'none', "zorder" : 10}, showfliers = True, whiskerprops = {'linewidth' : 2, "zorder" : 10}, flierprops = {'markersize' : 2})
    plt.yticks(ticks = list(range(len(solvers))), labels = [solver_labels[solver] for solver in solvers], fontsize = "large")
    filename = os.path.join(dirname, "igd_plus/dtlz" + str(dtlz) + ".png")
    plt.savefig(filename, format = "png")
    plt.close()

igd_plus = []

for solver in solvers:
    igd_plus.append([])

for dtlz in dtlzs:
    for n in ns:
        for m in ms:
            for i in range(len(solvers)):
                for seed in seeds:
                    filename = os.path.join(dirname, "igd_plus/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solvers[i] + "_" + str(seed) + ".txt")
                    if os.path.exists(filename):
                        with open(filename) as csv_file:
                            data = csv.reader(csv_file, delimiter = ",")
                            for row in data:
                                igd_plus[i].append(float(row[0]))
                            csv_file.close()

plt.figure()
plt.xlabel("Modified Inverted Generational Distance")
pt.half_violinplot(data = igd_plus, palette = colors, orient = "h", width = 0.6, cut = 0.0, inner = None)
sns.stripplot(data = igd_plus, palette = colors, orient = "h", size = 2, zorder = 0)
sns.boxplot(data = igd_plus, orient = "h", width = 0.20, color = "black", zorder = 10, showcaps = True, boxprops = {'facecolor' : 'none', "zorder" : 10}, showfliers = True, whiskerprops = {'linewidth' : 2, "zorder" : 10}, flierprops = {'markersize' : 2})
plt.yticks(ticks = list(range(len(solvers))), labels = [solver_labels[solver] for solver in solvers], fontsize = "large")
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus.png")
plt.savefig(filename, format = "png")
plt.close()

igd_plus_per_n = {}

for solver in solvers:
    igd_plus_per_n[solver] = {}
    for n in ns:
        igd_plus_per_n[solver][n] = []

for n in ns:
    for dtlz in dtlzs:
        for m in ms:
            for solver in solvers:
                for seed in seeds:
                    filename = os.path.join(dirname, "igd_plus/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solvers + "_" + str(seed) + ".txt")
                    if os.path.exists(filename):
                        with open(filename) as csv_file:
                            data = csv.reader(csv_file, delimiter = ",")
                            for row in data:
                                igd_plus_per_n[solver][n].append(float(row[0]))
                            csv_file.close()

plt.figure()
plt.xlabel("Number of Variables")
plt.ylabel("Modified Inverted Generational Distance")
plt.grid(alpha=0.5, color='gray', linestyle='dashed', linewidth=0.5, which='both')
for i in range(len(solvers)):
    y = []
    for n in ns:
        y.append(stats.mean(igd_plus_per_n[solvers[i]][n]))
    plt.plot(ns, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.xscale("log")
plt.yscale("log")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.gca().yaxis.set_minor_formatter(FormatStrFormatter('%.2f'))
plt.legend(loc = "best")
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus_mean_per_n.png")
plt.savefig(filename, format = "png")
plt.close()

plt.figure()
plt.xlabel("Number of Variables")
plt.ylabel("Modified Inverted Generational Distance")
plt.grid(alpha=0.5, color='gray', linestyle='dashed', linewidth=0.5, which='both')
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for n in ns:
        quantiles = stats.quantiles(igd_plus_per_n[solvers[i]][n])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(ns, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for n in ns:
        quantiles = stats.quantiles(igd_plus_per_n[solvers[i]][n])
        y1.append(quantiles[1])
    plt.plot(ns, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.xscale("log")
plt.yscale("log")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.gca().yaxis.set_minor_formatter(FormatStrFormatter('%.2f'))
plt.legend(loc = "best")
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus_quartiles_per_n.png")
plt.savefig(filename, format = "png")
plt.close()

igd_plus_per_m = {}

for solver in solvers:
    igd_plus_per_m[solver] = {}
    for m in ms:
        igd_plus_per_m[solver][m] = []

for m in ms:
    for dtlz in dtlzs:
        for n in ns:
            for solver in solvers:
                for seed in seeds:
                    filename = os.path.join(dirname, "igd_plus/dtlz" + str(dtlz) + "_" + str(n) + "_" + str(m) + "_" + solvers + "_" + str(seed) + ".txt")
                    if os.path.exists(filename):
                        with open(filename) as csv_file:
                            data = csv.reader(csv_file, delimiter = ",")
                            for row in data:
                                igd_plus_per_m[solver][m].append(float(row[0]))
                            csv_file.close()

plt.figure()
plt.xlabel("Number of Objectives")
plt.ylabel("Modified Inverted Generational Distance")
plt.xticks(ms)
plt.grid(alpha=0.5, color='gray', linestyle='dashed', linewidth=0.5, which='both')
for i in range(len(solvers)):
    y = []
    for m in ms:
        y.append(stats.mean(igd_plus_per_m[solvers[i]][m]))
    plt.plot(ms, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.yscale("log")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.gca().yaxis.set_minor_formatter(FormatStrFormatter('%.2f'))
plt.legend(loc = "best")
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus_mean_per_m.png")
plt.savefig(filename, format = "png")
plt.close()

plt.figure()
plt.xlabel("Number of Objectives")
plt.ylabel("Modified Inverted Generational Distance")
plt.xticks(ms)
plt.grid(alpha=0.5, color='gray', linestyle='dashed', linewidth=0.5, which='both')
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for m in ms:
        quantiles = stats.quantiles(igd_plus_per_m[solvers[i]][m])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(ms, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for m in ms:
        quantiles = stats.quantiles(igd_plus_per_m[solvers[i]][m])
        y1.append(quantiles[1])
    plt.plot(ms, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.yscale("log")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.gca().yaxis.set_minor_formatter(FormatStrFormatter('%.2f'))
plt.legend(loc = "best")
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus_quartiles_per_m.png")
plt.savefig(filename, format = "png")
plt.close()
