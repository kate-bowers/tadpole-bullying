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
import plotAll
from utilities import mins

collision_masterlist = []  # every collision in every video
min_def_time = None
# 	TODO make constants module and import them
# TODO should i change from hardcoding row[8] ie for velocity, auto find velocity col # each time?
# TODO save results to a file output pleaseeeee
for file in glob.glob(os.path.join(fileIO.data_filepath, "*.xlsx")):  # for each video excel sheet
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
	#break  # just look at first vid


# Make plots for all videos combined
# collision_masterlist_flat_bytime = sum(collision_masterlist, []) # flattens from each video to all
# collision_masterlist_flat_bytime.sort(key=lambda x : x[0])
# print(collision_masterlist_flat_bytime)
# plotAll.makePlots(collision_masterlist_flat_bytime, min_def_time)
# # TODO LABEL THESE GRAPHS LOL THEYRE USELESS RN
# # Make summary bar plots
# import summaryBars