# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# main.py -- driver for tadpole collision ID/analysis program

import fileIO  # establishes files and paths
import exceltabToCSV
import glob
import os
import collisionsPerVideo as perVideo
import matplotlib.pyplot as plt
import numpy as np
import plotAll
from utilities import mins

collision_masterlist = []  # every collision in every video
plot_steps = []
timelines = []
min_def_time = None
# 	TODO make constants module and import them
# TODO should i change from hardcoding row[8] ie for velocity, auto find velocity col # each time?
# TODO save results to a file output pleaseeeee
for file in glob.glob(os.path.join(fileIO.data_filepath, "*.xlsx"))[1:2]:  # for each video excel sheet
	# Make output directory for csvs if it doesn't exist yet
	print(file)
	subfolder = file[len(fileIO.data_filepath)+1:-5]
	output_path = os.path.join(fileIO.video_csvs_folder, subfolder + "/")

	print(fileIO.video_csvs_folder)
	print(file[len(fileIO.data_filepath):-5] + "/")
	print(output_path)
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	else:
		print("folder already exists")
	#breakpoint()
	if not os.listdir(output_path):  # if folder is empty, make CSVs
		exceltabToCSV.excelToCSV(file, output_path)
	else:
		print("CSVs already exist")

	#breakpoint()

	# Find collisions for this video
	collision_output = perVideo.find_collisions_per_video(fileIO.datfiles[file], output_path)
	collision_masterlist.append(collision_output[0])  # add collisions from this video to masterlist
	plot_steps.append(collision_output[2])
	timelines.append(collision_output[3])

	# Keep track of latest start time for deformed tadpole tracking
	if (min_def_time is None) or (collision_output[1] < min_def_time):
		min_def_time = collision_output[1]
	print("yoinks")  # just look at first vid



# Make plots for each video
for video in collision_masterlist:
	# plotAll.makePlots(video, min_def_time)
	print(" video ")
	for coll in video:
		coll.printSelf()  # mins(coll[8]), coll)
	print(len(video))
	# just look at first vid

# OCT 26 2021
# making plot showing min and max of control video
# index 0 is min (31) and index 2 is max (102) colls in 25 min
'''
print(" compare time min max controls")

fig, (axoutlier, axmost) = plt.subplots(2, 1, sharex='all', gridspec_kw={'height_ratios':[6,12]})
fig.subplots_adjust(hspace=0.05)

print("made fig ax")
#plt.xticks(timeline)
#print("made xticks")
breakpoint()
minvid = plot_steps[0]
maxvid = plot_steps[2]
for i in np.arange(0, len(maxvid)):
	axmost.step(timelines[2], maxvid[i], c='b', where='post')
	axoutlier.step(timelines[2], maxvid[i], c='b', where='post')
for i in np.arange(0, len(minvid)):
	axmost.step(timelines[0], minvid[i], c='r', where='post')
	axoutlier.step(timelines[0], minvid[i], c='r', where='post')
	#break
	#scatter(X, Y, c=cmap(i))

axmost.set_ylim(0, 12.5)
axoutlier.set_yticks([25, 50, 75, 100, 125, 150, 175])
#axmost.set_xlim(250, 400)
axoutlier.set_ylim(12.5, 140)
#axoutlier.set_xlim(250, 400)


d = .5  # proportion of vertical to horizontal extent of the slanted line
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
			  linestyle="none", color='k', mec='k', mew=1, clip_on=False)
axoutlier.plot([0, 1], [0, 0], transform=axoutlier.transAxes, **kwargs)
axmost.plot([0, 1], [1, 1], transform=axmost.transAxes, **kwargs)

plt.xlabel("Time(s)")
plt.ylabel("Collision Velocity (mm/s)")
this_title = "Comparison of minimum (31) and maximum (102) collision occurrences \n" \
			"in control tadpole videos"
axoutlier.set_title(this_title)
plt.show()
# breakpoint()
print("made show")
'''


# Make plots for all videos combined
# collision_masterlist_flat_bytime = sum(collision_masterlist, []) # flattens from each video to all
# collision_masterlist_flat_bytime.sort(key=lambda x : x[0])
# print(collision_masterlist_flat_bytime)
# plotAll.makePlots(collision_masterlist_flat_bytime, min_def_time)
# # TODO LABEL THESE GRAPHS LOL THEYRE USELESS RN
# # Make summary bar plots
# import summaryBars