import numpy as np
import matplotlib.pyplot as plt

# Generate the data

sequence1 = [54, 58, 104, 55, 52]
# np.random.randint(0, 100, 100)

sequence2 = [79, 102, 62, 31]
# np.random.randint(25, 75, 100)

# sequence3 = np.random.randint(50, 80, 100)
fig = plt.figure()
ax = fig.add_subplot()
plt.ylabel("Collisions")
ax.set_title("WT-Deformed Collisions in 25-minute videos")

ax.boxplot((sequence1, sequence2), labels=("Experimental \n n=5", "Control \n n=4")) # sequence3))

plt.show()