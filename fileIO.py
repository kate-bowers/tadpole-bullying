# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# fileIO.py -- establishes data file paths and dictionary with video data and info

import os

base = "/Users/katharinebowers/Desktop/Levin Lab/ethovision pipeline coding/"
data_filepath = os.path.join(base, "Ethovision Track Data Exports/")
video_csvs_folder = os.path.join(base, "CSVs for each video/")


datfiles = {   # specific to current list of info  -- TODO create filelist file?
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