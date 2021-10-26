# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# fileIO.py -- establishes data file paths and dictionary with video data and info

import os
import glob

#base_old = "/Users/katharinebowers/Desktop/Levin Lab/ethovision pipeline coding/"
base = "/Users/katharinebowers/Desktop/fall21 tadpole track exports/"
data_filepath = os.path.join(base, "Ethovision Track Data Exports/May 2021 Pebble Control Tracks")
# experimental september 2021 - cut tail")
# May 2021 Pebble Control Tracks")
video_csvs_folder = os.path.join(base, "CSVs for each video/")

# old data file list from first making this - before distances, tadpole #, and def subj # were standard
datfiles_old = {   # specific to current list of info  --
	# format: filepath corresponds to (deformed tadpole ID number,
	#                                  True if distances are off by a factor of 10, number of tadpoles
	(os.path.join(data_filepath, "Raw data-Correction Copy NewVideo1_9_28_18 " +
		"-666 inj deformed - good - ALL SUBJECTS-Trial    14 (1).xlsx")): (38, True, 38),
	(os.path.join(data_filepath, "Raw data-Correction Copy NewVideo8_10_5_18_666 " +
		"inj deformed - good - Copy-Trial     2.xlsx")): (10, False, 38),
	(os.path.join(data_filepath, "Raw data-Correction Copy NewVideo9_10_5_18_666 " +
		"inj deformed - good - Copy-Trial     2.xlsx")): (20, False, 36),
	(os.path.join(data_filepath, "Raw data-RepeatVideo2_10_2_18_-_666_inj_deformed_" +
		"-_good_---_35_tadpoles-Trial     2.xlsx")): (15, False, 36)
}


datfiles = {
	# format: filepath corresponds to (deformed tadpole ID number,
	#                                  True if distances are off by a factor of 10, number of tadpoles
	# (os.path.join(data_filepath, "Raw data-2021-05-21-30-tadpoles-control-vids-Trial     5.xlsx")): (1, False, 31),

}

excel_files = glob.glob(os.path.join(data_filepath, "*.xlsx"))  # for each video excel sheet
for vid in excel_files:
	datfiles[vid] = (1, False, 31)  # each of these new videos has 30 wt and the def is subj#1 and distances are right

# datfiles should now be loaded