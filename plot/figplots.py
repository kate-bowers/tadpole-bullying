import numpy as np
import matplotlib.pyplot as plt
# Kate Bowers
'''
collis = [0.875, 0.652, 0.6985, 0.746]
#collis_mean = np.mean(collis)
#collis_std = np.std(collis)

# Define labels, positions, bar heights and error bar heights
labels = ['200/2000 baseline \n n = 1', '620/1159 baseline \n n = 1', '620/1159 final \n n = 4', '620/2000 \n n = 4']
x_pos = np.arange(len(labels))
CTEs = [collis[0], collis[1], collis[2], collis[3]]
error = [0, 0, 0.283, 0.374]

# Build the plot
fig, ax = plt.subplots()
ax.bar(x_pos, CTEs,
       yerr=error,
       align='center',
       alpha=0.5,
       ecolor='black',
       capsize=10)
ax.set_ylabel('Identity loss errors per minute')
ax.set_xticks(x_pos)
ax.set_xticklabels(labels)
ax.set_title('Identity loss errors per minute for each profile')
ax.yaxis.grid(True)
plt.show()
'''
'''
collis = []
#collis_mean = np.mean(collis)
#collis_std = np.std(collis)

# Define labels, positions, bar heights and error bar heights
labels = ['Average', 'Video 1', 'Video 2', 'Video 3', 'Video 4']
x_pos = np.arange(len(labels))
CTEs = [collis[0], collis[1], collis[2], collis[3]]
error = [0, 0, 0.283, 0.374]

# Build the plot
fig, ax = plt.subplots()
ax.bar(x_pos, CTEs,
       yerr=error,
       align='center',
       alpha=0.5,
       ecolor='black',
       capsize=10)
ax.set_ylabel('Identity loss errors per minute')
ax.set_xticks(x_pos)
ax.set_xticklabels(labels)
ax.set_title('Identity loss errors per minute for each profile')
ax.yaxis.grid(True)
plt.show()
'''
#collis = [153/38, 196/36, 174/36, 233/38]
collis = [109, 130, 139, 156]
collis_mean = np.mean(collis)
collis_std = np.std(collis)

# Define labels, positions, bar heights and error bar heights
labels = ['Average', 'Video 1', 'Video 9', 'Video 2', 'Video 8']
x_pos = np.arange(len(labels))
CTEs = [collis_mean, collis[0], collis[1], collis[2], collis[3]]
error = [collis_std, 0, 0, 0, 0]

# Build the plot
fig, ax = plt.subplots()
ax.bar(x_pos, CTEs,
       yerr=error,
       align='center',
       alpha=0.5,
       ecolor='black',
       capsize=10)
ax.set_ylabel('Number of collisions')
ax.set_xticks(x_pos)
ax.set_xticklabels(labels)
ax.set_title('Calculated collisions with deformed tadpole')
ax.yaxis.grid(True)
plt.show()

#collis = [0.875, 0.652, 0.6985, 0.746]
#collis_mean = np.mean(collis)
#collis_std = np.std(collis)
'''
truths = [57, 49, 49, 39]
befores = [91, 98, 78, 66]
latests = [66, 58, 67, 40]
truth_mean = np.mean(truths)
truth_std = np.std(truths)
bef_mean = np.mean(befores)
bef_std = np.std(befores)
lat_mean = np.mean(latests)
lat_std = np.std(latests)

# Define labels, positions, bar heights and error bar heights
labels = ['Observed collisions', 'Identified collisions \n Before filtering', 'Identified collisions \n After filtering']
x_pos = np.arange(len(labels))
CTEs = [truth_mean, bef_mean, lat_mean]
error = [truth_std, bef_std, lat_std]

# Build the plot
fig, ax = plt.subplots()
ax.bar(x_pos, CTEs,
       yerr=error,
       align='center',
       alpha=0.5,
       ecolor='black',
       capsize=10)
ax.set_ylabel('Number of collisions with deformed tadpole')
ax.set_xticks(x_pos)
ax.set_xticklabels(labels)
ax.set_title('Accuracy of collision identification script with filtering (n = 4 videos)')
ax.yaxis.grid(True)
#fig.text(0.5, 0, "n = 4 videos", ha='center')
plt.show()
'''