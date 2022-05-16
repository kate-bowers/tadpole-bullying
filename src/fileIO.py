# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# fileIO.py -- establishes data file paths and dictionary with video data and info

import os
import glob
import tkinter as tk
from tkinter.filedialog import askdirectory
root = tk.Tk()
root.withdraw()

print("Welcome! Select the directory which includes your Ethovision track export Excel files.")
print("This folder should include only experimental OR only control videos: they have different collision distance thresholds.")
print("The program assumes that the deformed tadpole is Subject #1, and there are 31 total tadpoles. It is possible to "
	  "change these settings by editing the source code.")
print("The output track CSVs and collision lists for each video will also be saved to this folder.")
print("\n ........................................")

data_filepath = askdirectory(title='Select Data Folder')


userinput = input("Enter the proximity distance and necessary distance (mm) and experiment type, ie 5.5 4.2 tail-cut   :"
			  "\nHint: As a good default, use 5.5 as proximity distance,"
			  " 4.2 for experimental necessary distance, and 5 for control/pebble necessary distance.").split()
if len(userinput) != 3:
	while len(userinput) != 3:
		print("Oops, that's not right. Please input the 3 values as directed.")
		userinput = input("Enter the proximity distance and necessary distance (mm) and "
						  "experiment type, ie 5.5 4.2 tail-cut   :").split()

video_csvs_folder = os.path.join(data_filepath, "CSVs for each video/")
if not os.path.isdir(video_csvs_folder):
	os.mkdir(video_csvs_folder)

colls_path = os.path.join(data_filepath, "Collisions in each video/")
if not os.path.isdir(colls_path):
	os.mkdir(colls_path)

datfiles = {
	# format: filepath corresponds to (deformed tadpole ID number,
	#                                  True if distances are off by a factor of 10, number of tadpoles
	# (os.path.join(data_filepath, "Raw data-2021-05-21-30-tadpoles-control-vids-Trial     5.xlsx")): (1, False, 31),

}

excel_files = glob.glob(os.path.join(data_filepath, "*.xlsx"))  # for each video excel sheet
for vid in excel_files:
	datfiles[vid] = (1, False, 31)  # each of these new videos has 30 wt and the def is subj#1 and distances are right

# datfiles should now be loaded