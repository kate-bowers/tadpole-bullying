# Kate Bowers
# Scratch testing file to figure out new data-dense plot to show tadpole interactions
import matplotlib.pyplot as plt
import numpy as np

time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

class Coll:
    def __init__(self, start, end, vel):
        self.start = start
        self.end = end
        self.vel = vel


def makeSteps(collisions, num_timepoints):
    steps = [0]*num_timepoints
    for c in collisions:
        i = c.start
        while i < c.end:
            steps[i] = c.vel
            i += 1
    return steps


# imagine for one wild type right now
c1 = Coll(1, 4, 3)
c2 = Coll(7, 10, 5)
c3 = Coll(14,15,1)
c4 = Coll(18, 19, 10)

c5 = Coll(3, 5, 4)
c6 = Coll(8, 14, 2)

c7 = Coll(2, 9, 2)
c8 = Coll(12, 14, 2)


colls = [c1, c2, c3, c4]
colls2 = [c5, c6]

wt = [0]*len(time)
for c in colls:   # start # end # vel
    i = c.start
    while i < c.end:
        wt[i] = c.vel
        i += 1

wt2 = [0]*len(time)
for c in colls2:   # start # end # vel
    i = c.start
    while i < c.end:
        wt2[i] = c.vel
        i += 1

def get_cmap(n, name='hsv'): # from stack overflow
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


cmap = get_cmap(len(data))
for i, (X, Y) in enumerate(num_wts):
   scatter(X, Y, c=cmap(i))

fig, ax = plt.subplots(figsize=(12, 6))
plt.xticks(np.arange(0, 21, 1.0))
x = np.arange(0, 21, 1.0)
#ax.plot(wt, color='blue', label='wt')
plt.step(x, makeSteps(colls, len(time)), 'b', where='post')
plt.step(x, makeSteps(colls2, len(time)), 'g', where='post')

#ax.plot(z, color='black', label='Cosine wave')

plt.show()

# have a list of colls for each
# make program that takes in wt list, makes 0/vel list



# given all of these steps -- use matplot colors (rgb/hex?)