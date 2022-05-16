import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
import math

t1 = np.asarray([13, 40, 44])
t2 = np.asarray([6, 36, 16])
t3 = np.asarray([5, 15, 21])
#  t4 = np.asarray([21, 101])  # removed None from immobile middle
t5 = np.asarray([16, 44, 30])
t6 = np.asarray([14, 30, 34])
# t8 = [5, 0, 9] # don't use
#  t9 = np.asarray([15, 20])  # removed none for immobile middle

# goal: be able to compare across these videos
# first do a plot comparing all of them raw
# don't want to do a plot w/ means and SD for that
# normalize along each video
# and then redo first plot
# and then do mean plot

all_controls = [13, 5, 16, 14, 21]
all_immobile = [40, 15, 44, 30, 45]
all_tailcut = [44, 21, 30, 34, 51]

# standard deviation
control_std = np.std(all_controls)
immobile_std = np.std(all_immobile)
tailcut_std = np.std(all_tailcut)
st = [control_std, immobile_std, tailcut_std]

labels = [1, 3, 5, 6, 12]

plt.bar(labels, all_controls)
plt.bar(["controls", "immobile", "tailcut"],
        [np.mean(all_controls, dtype=float), np.mean(all_immobile, dtype=float),
         np.mean(all_tailcut, dtype=float)], yerr=st)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
ax1.set_xticks([0])
ax2.set_xticks([0])
ax3.set_xticks([0])
# plt.plot([1, 1, 2, 2], [3, 3, 3, 3], linewidth=1, color='k')
# plt.plot([1, 1, 2, 2], [3, 3, 3, 3], linewidth=1, color='k')

'''plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
'''
BOLD = '\033[1m'
END = '\033[0m'

ax1.boxplot(all_controls)
ax1.set_xlabel("30wt + 1 pebble \n n=5")
'''plt.text(0.1, 0.9,'A',
     horizontalalignment='left',
     verticalalignment='top',
     transform = ax1.transAxes, fontweight='bold', fontsize = 14)
#ax1.axis("off")
plt.text(1.3, 0.9,'B',
     horizontalalignment='left',
     verticalalignment='top',
     transform = ax1.transAxes, fontweight='bold', fontsize = 14)
#ax2.axis("off")

plt.text(2.5, 0.9,'C',
     horizontalalignment='left',
     verticalalignment='top',
     transform = ax1.transAxes, fontweight='bold', fontsize = 14)
#ax3.axis("off")'''
ax2.boxplot(all_immobile)
ax2.set_xlabel("30wt + 1 ethanol-deformed \n n=5")
ax3.boxplot(all_tailcut)
ax3.set_xlabel("30wt + 1 tail-cut \n n=5")

ax1.set_ylabel("Number of collisions", x=0.95)
fig.suptitle('Collisions by wild-type against deformed tadpole or control pebble', y=0.99)

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.axes.yaxis.set_ticks([])

ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_visible(False)

plt.show()
