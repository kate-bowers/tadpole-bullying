# Kate Bowers
# Levin Lab Tufts University March-April 2021
# Beckman Scholars

import csv
import xlrd
import sys
import os
import math
import matplotlib.pyplot as plt
import glob
import numpy as np

global  ones
ones = 0

def dist(p1,p2):
	x1 = p1[0]
	y1 = p1[1]
	x2 = p2[0]
	y2 = p2[1]

	dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
	return dist # compute euclidean distance

def ExceltoCSV(excel_file, csv_file_base_path): # adapted from exceltab_to_csv by Github user billydh
    print("excel split starting now!")
    print("exc file is " + excel_file)
    print("path is " + csv_file_base_path)
    print(os.path.isfile(excel_file))
    workbook = xlrd.open_workbook(excel_file)
    print("opened workbook!")
    print(workbook.sheet_names())
    print("yep")
    for sheet_name in workbook.sheet_names():
        print('processing - ' + sheet_name)
        worksheet = workbook.sheet_by_name(sheet_name)
        csv_file_full_path = csv_file_base_path + sheet_name.lower().replace(" - ", "_").replace(" ","_") + '.csv'
        csvfile = open(csv_file_full_path, 'w')


        writetocsv = csv.writer(csvfile, quoting = csv.QUOTE_ALL)
        for rownum in range(worksheet.nrows):
            writetocsv.writerow([x for x in worksheet.row_values(rownum)])
        csvfile.close()
        print(sheet_name + ' has been saved at - ' + csv_file_full_path)

def mins(time): # puts seconds into minutes:seconds format
	t = float(time)
	m = math.floor(t / 60) # num of minutes
	s = t % 60
	return(str(m) + ":" + str(s)[:6])

def find_def_start_time(def_num, csvs_path):
	deformed_csv = os.path.join(csvs_path, f"track-arena_1-subject_{def_num}.csv")

	start_time = None

	with open(deformed_csv, newline='') as def_f:
		#print("starting " + str(wt_num))
		#proximity_times = open(os.path.join(folder_rv2, str(wt_num)+"output.txt"), "w") # should be path specific?
		def_reader = csv.reader(def_f)

		for _ in range(36): # skips the 36 header lines
			next(def_reader)

		for drow in def_reader: 
			not_started = (drow[2] == "-")  # is location of deformed tadpole undefined 
			if not not_started: # location is known!
				print(mins(drow[0]))
				return drow[0] 

def find_collisions_per_video(datfile, csvs_path):
	print(csvs_path)
	def_num = datfile[0] 
	wrong_distances = datfile[1]
	num_tads = datfile[2]

	# Calculate for all
	all_collisions = []
	total_collisions = 0

	# Know when the deformed tadpole shows up
	def_start_time = find_def_start_time(def_num, csvs_path)

	time_with_def = None
	for sub in range(1,num_tads): # calculate for all
		if sub == def_num: #skip deformed lol
			continue
		sub_collisions = find_collisions(sub, def_num, csvs_path, wrong_distances, def_start_time)
		all_collisions.append(sub_collisions[0])
		total_collisions += len(sub_collisions[0])
		time_with_def = sub_collisions[1]
		#print(sub, len(sub_collisions))
	print(str(total_collisions) + " by " + str(num_tads - 1) + " wt tadpoles") # + " in " + deformed_csv[14][1])
	print("in " + mins(time_with_def))


	# Flatten into time-based mega list
	all_collisions_flat_bytime = sum(all_collisions, []) # flattens from subjects to full video
	# sort by time
	all_collisions_flat_bytime.sort(key=lambda x : x[0])

	'''
	all_collisions_flat_times = list(map(lambda x: x[0], all_collisions_flat_bytime))
	if (wrong_distances == False):
		all_collisions_flat_disps = list(map(lambda x: x[1], all_collisions_flat_bytime))     
		all_collisions_flat_velocities = list(map(lambda x: x[2], all_collisions_flat_bytime))
	else:
		all_collisions_flat_disps = list(map(lambda x: x[1]/10, all_collisions_flat_bytime))      # 	DIVIDE BY 10 FOR NEW VIDEO 1 (and below)
		all_collisions_flat_velocities = list(map(lambda x: x[2]/10, all_collisions_flat_bytime))
	'''

	# would call plotting thigns now

	
	return (all_collisions_flat_bytime, time_with_def)

def find_collisions(wt_num, def_num, csvs_path, wrong_distances, def_start):
	global ones
	deformed_csv = os.path.join(csvs_path, f"track-arena_1-subject_{def_num}.csv")
	wt_csv = os.path.join(csvs_path, f"track-arena_1-subject_{wt_num}.csv")

	num_collisions = 0
	collisions = []

	time_with_def = 0
	# READING IN DATA & ISOLATING XY COORDS
	with open(deformed_csv, newline='') as def_f, open(wt_csv, newline='') as wt_f:
		#proximity_times = open(os.path.join(folder_rv2, str(wt_num)+"output.txt"), "w") # should be path specific?
		def_reader = csv.reader(def_f)
		wt_reader = csv.reader(wt_f)

		for _ in range(36): # skips the 36 header lines
			next(wt_reader)
			next(def_reader)
		
		already_in_proximity = False

		prox_start_time = None
		prox_duration = 0
		smallest_dist_so_far = None
		vel_of_smallest_dist = None
		time_of_smallest_dist = None
		dxy_of_smallest_dist = []
		drift_closed = False
		active_disp = None
		num_lost = 0
		w_lost = 0
		d_lost = 0

		last_dxy = None


		for drow, wrow in zip(def_reader, wt_reader):
			time_with_def = float(drow[0]) - float(def_start)

			dxy = drow[2:4]
			wxy = wrow[2:4]

			# Filter out lost timepoints
			if (wxy[0] == "-"):  # ok if doing individually but not if comparing more than 2 files here
				w_lost += 1
				continue

			if (dxy[0] == "-"): # would suck bc we dont wanna miss def anywhere
				d_lost += 1
				continue

			# Calculate distances
			dxy[0], dxy[1], wxy[0], wxy[1] = float(dxy[0]), float(dxy[1]), float(wxy[0]), float(wxy[1])

			distance = dist(dxy, wxy)

			if (wrong_distances):
				significant_distance = 40
				too_close_dist = 5
			else:
				significant_distance = 4
				too_close_dist = 0.5
			# Analyze collisions
			
			if ((distance <= significant_distance)): # within significant proximity to deformed
				#  and (distance >= 5 mm)
				if ((not already_in_proximity) and (distance >= too_close_dist)):
					
					# DEAL WITH OLD EVENT
					if (prox_start_time != None): # there was a previous collision
						if(not drift_closed): # previous collision is still open
							 #REPORTS
							'''
							proximity_times.write("new event found starting at " + mins(prox_start_time) + "\n")
							proximity_times.write("event smallest dist was " + str(smallest_dist_so_far) + '\n')
							proximity_times.write("collided at " + mins(time_of_smallest_dist) + '\n')
							proximity_times.write("velocity at collision: " + str(vel_of_smallest_dist) + '\n\n')
							'''
							disp = float(dist(dxy, dxy_of_smallest_dist))
							'''collisions.append( # -----------------------velocity change collision reports
								(time_of_smallest_dist, 
								disp, 
								float(vel_of_smallest_dist) if vel_of_smallest_dist != "-" else "-", 
								False,
								wt_num)
							) # false: not a clean collision (displacement is not the 2s window)
							'''
							
							# TEMPORARY CHANGE TO VELOCITY NANS
							if (prox_duration != 1):
								if(vel_of_smallest_dist != "-"):
									vel = float(vel_of_smallest_dist) if not wrong_distances else float(vel_of_smallest_dist)/10
									disp = disp / 10 if wrong_distances else disp    
									collisions.append(
										(float(time_of_smallest_dist) - float(def_start), #time corrected for when def shows up
										disp, 
										vel, #float(vel_of_smallest_dist), 
										False,
										wt_num, 
										wxy,
										def_num)
									)
									print(mins(time_of_smallest_dist), vel, def_num)
							else:
								ones += 1
					prox_start_time = wrow[0] 

					# DEAL WITH NEW EVENT
					#proximity_times.write("NEW EVENT at " + mins(prox_start_time) + "\n")
					drift_closed = False
					already_in_proximity = True # update
					prox_duration = 1
					num_collisions += 1
					smallest_dist_so_far = distance
					vel_of_smallest_dist = wrow[8]
					time_of_smallest_dist = float(wrow[0])
					dxy_of_smallest_dist = dxy
					sum_movement = 0
					sum_frdist = 0
					if (drow[7] != '-'): # set new active disp
						active_disp = float(drow[7])
					else:
						active_disp = 0

				elif(already_in_proximity): # existing event
					#proximity_times.write(str(distance) + "\n")   #	writes distance during event
					prox_duration += 1
					#print(time_of_smallest_dist)
					#print(distance)
					if (float(drow[0]) < float(time_of_smallest_dist) + 2): # it's been less than 2s since we found smallest dist
					#proximity_times.write("smallest at " + mins(time_of_smallest_dist) + "\n")
						if (distance < smallest_dist_so_far): # update if smaller dist found
							#proximity_times.write("UPDATED AT " + mins(drow[0]) + "\n")
							smallest_dist_so_far = distance
							vel_of_smallest_dist = wrow[8]
							time_of_smallest_dist = float(wrow[0])
							dxy_of_smallest_dist = dxy
							if (drow[7] != '-'):
								active_disp = float(drow[7])    # displacement resets when new small dist does
							else:
								active_disp = 0
						else: # not a new smaller dist
							if (drow[7] != '-'):
								#print(drow[0])
								active_disp += float(drow[7]) # update active displacement
					#print(drow)
					'''
					
					'''
					if(not drift_closed): # still moving
						#proximity_times.write(drow[0] + " " + str(dxy_of_smallest_dist[0]) + " " + str(dxy_of_smallest_dist[1]) + "\n")
						#proximity_times.write(drow[0] + " " + str(dxy[0]) + " " + str(dxy[1]) + "\n")
						frdist = (dist(dxy, last_dxy))
						#proximity_times.write('\n')
						#if (drow[7] != '-'):
							#proximity_times.write("diff is " + str((float(drow[7]) - frdist)/10) + "\n")
						if(drow[7] == '-'): # no movement
							sum_movement += 0 
						else:
							sum_movement += float(drow[7])
						sum_frdist += frdist
						#proximity_times.write("frdist so far: " + str(sum_frdist) + "\n")


				#proximity_times.write(str(drow[0]) + '\n') # report time in proxiity

			else: # not in proximity
				already_in_proximity = False # will end proximity event
				
			# Calculate displacements after 2s
			# this is a problem because just because there's A smallest dist doesn't mean it'll be THE smallest dist?
			# is it likely that the real collision will happen more than 3s after the proximity begins
			# collision is smallest dist within first 3s?

			#TODO THIS IS NOT WORKING WE COLLIDED AT 443.125 BUT NO i think it is now lol
			if (time_of_smallest_dist != None): #if there is an existing collision on record
				if ((float(drow[0]) >= float(time_of_smallest_dist) + 2) and (not drift_closed)): 
				# if at least 2 seconds since collision passed and displacement not yet calculated (this code hasn't yet run for it)
					'''
					proximity_times.write("collision by subject " + str(wt_num) + " at " + mins(time_of_smallest_dist) + "\n")
					proximity_times.write("displacement: " + str(dist(dxy, dxy_of_smallest_dist)) + "\n")
					proximity_times.write("velocity at collision: " + str(vel_of_smallest_dist) + '\n\n')
					'''
					'''
					disp = float(dist(dxy, dxy_of_smallest_dist))
					collisions.append(
								(time_of_smallest_dist, 
								disp, 
								float(vel_of_smallest_dist) if vel_of_smallest_dist != "-" else "-", 
								True,
								wt_num)
							)
					'''
					

					# TEMPORARY CHANGE TO VELOCITY NANS
					disp = float(dist(dxy, dxy_of_smallest_dist))
					if(prox_duration != 1):
						if(vel_of_smallest_dist != "-"):    
							vel = float(vel_of_smallest_dist) if not wrong_distances else float(vel_of_smallest_dist)/10 
							disp = disp / 10 if wrong_distances else disp    
							collisions.append(
								(float(time_of_smallest_dist) - float(def_start), 
								disp, 
								vel, #float(vel_of_smallest_dist), 
								True,
								wt_num,
								wxy,
								def_num)
							)
							print(mins(time_of_smallest_dist), vel, def_num)
					else:
						ones += 1
					# NaN velocities show up as "-"
					# True is because it's a clean collision (2s displacement after)

					#proximity_times.write("ends at " + mins(drow[0]) + "\n")
					#proximity_times.write("smallest dist was "+ str(smallest_dist_so_far) + "\n")
					#print(dxy_of_smallest_dist) # not necessarily defined but hopefully if statement fixes
					#print('\n')
					#proximity_times.write("disp calc w times of: " + mins(time_of_smallest_dist) + " to " + mins(drow[0]) + "\n")
					#proximity_times.write("sum mvmt: " + str(sum_movement) + "\n")
					#proximity_times.write("sum fr: " + str(sum_frdist) + "\n")
					#proximity_times.write("active disp: " + str(active_disp) + "\n")
					#proximity_times.write("diff: " + (str(dist(dxy, dxy_of_smallest_dist) - active_disp)) + "\n")
					#proximity_times.write("lost w:" + str(w_lost) + " lost d:" + str(d_lost) + "\n")
					
					#proximity_times.write("speed: " + str(vel_of_smallest_dist) + "\n")
					drift_closed = True
			last_dxy = dxy

		
		#proximity_times.write(str(num_collisions))
		#proximity_times.close()
	return (collisions, time_with_def)

base = "/Users/katharinebowers/Desktop/Tufts Files/Levin Lab/ethovision pipeline coding/"
data_filepath = os.path.join(base, "Ethovision Track Data Exports/")
video_csvs_folder = os.path.join(base, "CSVs for each video/")

datfiles = {   #specific to current list of info
	(os.path.join(data_filepath, "Raw data-Correction Copy NewVideo1_9_28_18 " +
		"-666 inj deformed - good - ALL SUBJECTS-Trial    14 (1).xlsx")): (38, True, 38),
	(os.path.join(data_filepath, "Raw data-Correction Copy NewVideo8_10_5_18_666 " +
		"inj deformed - good - Copy-Trial     2.xlsx")): (10, False, 38),
	(os.path.join(data_filepath, "Raw data-Correction Copy NewVideo9_10_5_18_666 " +
		"inj deformed - good - Copy-Trial     2.xlsx")): (20, False, 36),
	(os.path.join(data_filepath, "Raw data-RepeatVideo2_10_2_18_-_666_inj_deformed_" + 
		"-_good_---_35_tadpoles-Trial     2.xlsx")): (15, False, 36)
}

collision_masterlist = [] # every collision in every video
min_def_time = None

for file in glob.glob(os.path.join(data_filepath, "*.xlsx")): #for each video excel sheet
	# make output directory for all csvs
	output_path = os.path.join(video_csvs_folder, file[len(data_filepath):-5] + "/")
	#os.mkdir(output_path)
	#ExceltoCSV(file, output_path) # produce csvs for each video
	collision_output = find_collisions_per_video(datfiles[file], output_path)
	collision_masterlist.append(collision_output[0]) # add collisions from this video to masterlist
	#keep track of latest start time for deformed tadpole tracking
	if (min_def_time == None) or (collision_output[1] < min_def_time):
		min_def_time = collision_output[1]
	

print(len(collision_masterlist))
#print(collision_masterlist[1])
num_under = 0
for video in collision_masterlist:

	'''
	print(len(video))
	x = len(list(filter(lambda video: video[0] < min_def_time, 
	video)))
	print(x)
	num_under += x
	'''
	# Filter out the collisions after the minimum time with def (min def time)
	filtered_collision = list(filter(lambda collision: collision[0] < min_def_time, 
		video))
	print(len(filtered_collision))

	filtered_flat_times = list(map(lambda x: x[0], filtered_collision))
	filtered_flat_disps = list(map(lambda x: x[1], filtered_collision))     
	filtered_flat_velocities = list(map(lambda x: x[2], filtered_collision))
	filtered_flat_videoIDs = list(map(lambda x: x[6], filtered_collision))
	print(filtered_flat_videoIDs)
	
	plt.xlabel("Time (s)")
	plt.ylabel("Collision frequency")
	#plt.title("NewVideo1_9_28_18")
	plt.title("Collision frequency (bin = 5s)")
	res = plt.hist(filtered_flat_times, bins=list(x*5 for x in range(19 * 12)), density=False)   # bin for every 5 seconds ////minute
	#plt.hist(all_collisions_flat_times, bins=list(range(1450)))
	plt.show() 

print(mins(min_def_time))
print(num_under)
# Flatten into time-based mega list, sort by time

collision_masterlist_flat_bytime = sum(collision_masterlist, []) # flattens from each video to all
collision_masterlist_flat_bytime.sort(key=lambda x : x[0])
print(len(collision_masterlist_flat_bytime))
# Filter out the collisions after the minimum time with def (min def time)
filtered_collision_masterlist = list(filter(lambda collision: collision[0] < min_def_time, 
	collision_masterlist_flat_bytime))
print(len(filtered_collision_masterlist))

filtered_flat_times = list(map(lambda x: x[0], filtered_collision_masterlist))
filtered_flat_disps = list(map(lambda x: x[1], filtered_collision_masterlist))     
filtered_flat_velocities = list(map(lambda x: x[2], filtered_collision_masterlist))
filtered_flat_videoIDs = list(map(lambda x: x[6], filtered_collision_masterlist))
filtered_flat_WTcolliders = list(map(lambda x: x[4], filtered_collision_masterlist))


# PLOT VELOCITY VS DISPLACEMENT
'''

plt.scatter(all_collisions_flat_velocities, all_collisions_flat_disps) 
plt.xlabel("Velocity")
plt.ylabel("Displacement")
plt.show()
'''
'''
# THIS IS A SHITTY GRAPH BC THERE ARE SOME HUGE OUTLIERS (20,000 VELOCITY)

#plt.hist(list(filter(lambda x: x < 5000, all_collisions_flat_velocities)))
#plt.show()

'''
'''
plt.xlabel("Time (s)")
plt.ylabel("Collision frequency")
#plt.title("NewVideo1_9_28_18")
plt.title("Collision frequency (bin = 20s)") 
res = plt.hist(filtered_flat_times, bins=list(x*20 for x in range(19 * 3)), density=False)   # bin for every 20 seconds ////minute
#plt.hist(all_collisions_flat_times, bins=list(range(1450)))
plt.show() 

plt.xlabel("Time (s)")
plt.ylabel("Collision frequency")
#plt.title("NewVideo1_9_28_18")
plt.title("Collision frequency (bin = 10s)") 
res = plt.hist(filtered_flat_times, bins=list(x*10 for x in range(19 * 6)), density=False)   # bin for every 10 seconds ////minute
#plt.hist(all_collisions_flat_times, bins=list(range(1450)))
plt.show() 

plt.xlabel("Time (s)")
plt.ylabel("Collision frequency")
#plt.title("NewVideo1_9_28_18")
plt.title("Collision frequency (bin = 5s)")
res = plt.hist(filtered_flat_times, bins=list(x*5 for x in range(19 * 12)), density=False)   # bin for every 5 seconds ////minute
#plt.hist(all_collisions_flat_times, bins=list(range(1450)))
plt.show() 

'''
# PLOT VELOCITIES OVER TIME
outlier_vels = []
ok_times = []
ok_vels = []
ok_disps = []
under50_disps = []
under50_disps_times = []
for i in range(len(filtered_collision_masterlist)):
	#print(i)
	if filtered_flat_velocities[i] > 200: # temporary upper limit is 200
		outlier_vels.append(i)
		print(mins(filtered_flat_times[i]), filtered_flat_velocities[i], 
			" velocity", filtered_flat_videoIDs[i], 
			filtered_flat_WTcolliders[i])
	else:
		ok_vels.append(filtered_flat_velocities[i])
		ok_times.append(filtered_flat_times[i])
		ok_disps.append(filtered_flat_disps[i])
	if filtered_flat_disps[i] < 50:
		under50_disps.append(filtered_flat_disps[i])
		under50_disps_times.append(filtered_flat_times[i])
	else:
		print(mins(filtered_flat_times[i]), filtered_flat_disps[i], 
			" disp", filtered_flat_videoIDs[i],
			filtered_flat_WTcolliders[i])
print(outlier_vels)
print(len(outlier_vels))
print(max(filtered_flat_velocities))
print(max(filtered_flat_disps), "good to know for fun")

print(ones)
print(len(filtered_flat_velocities))
print(len(ok_vels))


#all_collisions_flat_velocities[x] < 500 for x in range(total_collisions
plt.scatter(filtered_flat_times, filtered_flat_velocities)
plt.xlabel("Time (s)")
plt.ylabel("Velocity (mm/s)")
#plt.title("NewVideo1_9_28_18")
plt.title("Collision velocities over time")
plt.show()

plt.xlabel("Time (s)")
plt.ylabel("Velocity (mm/s)")
#plt.title("NewVideo1_9_28_18, velocities under 200 mm/s")
plt.title("Collision velocities over time (under 200 mm/s)")
plt.scatter(ok_times, ok_vels)
plt.show()


# PLOT DISPLACEMENTS OVER TIME

'''
plt.scatter(filtered_flat_times, filtered_flat_disps)
plt.xlabel("Time (s)")
plt.ylabel("Displacement (mm)")
#plt.title("NewVideo1_9_28_18")
plt.title("Collision displacement over time")
plt.show()
'''
'''
plt.scatter(ok_times, ok_disps)
plt.xlabel("Time (s)")
plt.ylabel("Displacement (mm)")
#plt.title("NewVideo1_9_28_18")
plt.title("Collision displacement over time (for velocities under 200 mm/s)")
plt.show()

plt.scatter(under50_disps_times, under50_disps)
plt.xlabel("Time (s)")
plt.ylabel("Displacement (mm)")
#plt.title("NewVideo1_9_28_18")
plt.title("Collision displacement over time (under 50 mm)")
plt.show()
'''

# PLOT VELOCITY VS DISPLACEMENT
'''
plt.scatter(filtered_flat_velocities, filtered_flat_disps)
plt.xlabel("Velocity (mm/s)")
plt.ylabel("Displacement (mm)")
#plt.title("NewVideo1_9_28_18")
plt.title("Collision velocity vs displacement")
plt.show()
'''

'''
plt.scatter(ok_vels, ok_disps)
plt.xlabel("Velocity (mm/s)")
plt.ylabel("Displacement (mm)")
#plt.title("NewVideo1_9_28_18")
plt.title("Collision velocity vs displacement (under 200 mm/s)")
plt.show()
'''
'''
# HISTOGRAM VELOCITY AND DISPLACMENT
plt.xlabel("Velocity (mm/s)")
plt.ylabel("Frequency")
#plt.title("NewVideo1_9_28_18")
plt.title("Velocity distribution (under 200 mm/s)")
res = plt.hist(ok_vels)  
#plt.hist(all_collisions_flat_times, bins=list(range(1450)))
plt.show() 

plt.xlabel("Displacement (mm)")
plt.ylabel("Frequency")
#plt.title("NewVideo1_9_28_18")
plt.title("Displacement distribution (for velocities under 200 mm/s)")
res = plt.hist(ok_disps)  
#plt.hist(all_collisions_flat_times, bins=list(range(1450)))
plt.show() 


plt.xlabel("Displacement (mm/s)")
plt.ylabel("Frequency")
#plt.title("NewVideo1_9_28_18")
plt.title("Displacement distribution (under 30 mm)")
res = plt.hist(under50_disps)  
#plt.hist(all_collisions_flat_times, bins=list(range(1450)))
plt.show() 
'''


collis = [153/38, 196/36, 174/36, 233/38]
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
ax.set_ylabel('Number of collisions with deformed tadpole')
ax.set_xticks(x_pos)
ax.set_xticklabels(labels)
ax.set_title('Average collisions with deformed tadpole in 18:48, per wild-type tadpole')
ax.yaxis.grid(True)
plt.show()

#print(filtered_collision_masterlist)


'''
all_collisions_flat_times = list(map(lambda x: x[0], all_collisions_flat_bytime))
	if (wrong_distances == False):
		all_collisions_flat_disps = list(map(lambda x: x[1], all_collisions_flat_bytime))     
		all_collisions_flat_velocities = list(map(lambda x: x[2], all_collisions_flat_bytime))
	else:
		all_collisions_flat_disps = list(map(lambda x: x[1]/10, all_collisions_flat_bytime))      # 	DIVIDE BY 10 FOR NEW VIDEO 1 (and below)
		all_collisions_flat_velocities = list(map(lambda x: x[2]/10, all_collisions_flat_bytime))

'''
'''
# ***********************
def_num = 15 # UPDATE WITH DEFORMED TADPOLE SUBJ NUMBER
num_tads = 36   # num subjects

# Calculate for all
all_collisions = []
total_collisions = 0

for sub in range(1,num_tads): # calculate for all
	if sub == def_num: #skip deformed lol
		continue
	sub_collisions = find_collisions(sub)
	#breakpoint()
	all_collisions.append(sub_collisions)
	total_collisions += len(sub_collisions)
	#print(sub, len(sub_collisions))
print(str(total_collisions) + " by " + str(num_tads - 1) + " wt tadpoles") # + " in " + deformed_csv[14][1])



# Flatten into time-based mega list
all_collisions_flat_bytime = sum(all_collisions, []) # flattens
# sort by time
all_collisions_flat_bytime.sort(key=lambda x : x[0])

all_collisions_flat_times = list(map(lambda x: x[0], all_collisions_flat_bytime))
all_collisions_flat_disps = list(map(lambda x: x[1], all_collisions_flat_bytime))      # 	DIVIDE BY 10 FOR NEW VIDEO 1 (and below)
all_collisions_flat_velocities = list(map(lambda x: x[2], all_collisions_flat_bytime))


for x in all_collisions_flat_bytime:
	#print(x)
	if (x[3]): # is a clean hit for displacement
		print("look", mins(x[0]), x)
print(len(all_collisions_flat_bytime))

#print(all_collisions_flat_times)

# PLOT VELOCITY VS DISPLACEMENT
'''
'''
plt.scatter(all_collisions_flat_velocities, all_collisions_flat_disps) 
plt.xlabel("Velocity")
plt.ylabel("Displacement")
plt.show()
'''
# THIS IS A SHITTY GRAPH BC THERE ARE SOME HUGE OUTLIERS (20,000 VELOCITY)

#plt.hist(list(filter(lambda x: x < 5000, all_collisions_flat_velocities)))
#plt.show()

'''
binz = list(x*60 for x in range(24))
#print(binz)

plt.xlabel("Time (s)")
plt.ylabel("Collision frequency")
#plt.title("NewVideo1_9_28_18")
plt.title("Repeat Video 2")
res = plt.hist(all_collisions_flat_times, bins=list(x*60 for x in range(24)), density=False)   # bin for every minute
#plt.hist(all_collisions_flat_times, bins=list(range(1450)))
for ben in res[0]:
	print((ben))

print("twas bins")

plt.show() 

# manually bin the times for multi collisions



outlier_vels = []
ok_times = []
ok_vels = []
for i in range(total_collisions):
	#print(i)
	if all_collisions_flat_velocities[i] > 200: # temporary upper limit is 200
		outlier_vels.append(i)
	else:
		ok_vels.append(all_collisions_flat_velocities[i])
		ok_times.append(all_collisions_flat_times[i])
print(outlier_vels)
print(max(all_collisions_flat_velocities))


#all_collisions_flat_velocities[x] < 500 for x in range(total_collisions
plt.scatter(all_collisions_flat_times, all_collisions_flat_velocities)

plt.xlabel("Time (s)")
plt.ylabel("Velocity (mm/s)")
#plt.title("NewVideo1_9_28_18")
plt.title("Repeat Video 2")
plt.show()

plt.xlabel("Time (s)")
plt.ylabel("Velocity (mm/s)")
#plt.title("NewVideo1_9_28_18, velocities under 200 mm/s")
plt.title("Repeat Video 2, velocities under 200 mm/s")
plt.scatter(ok_times, ok_vels)
plt.show()

plt.scatter(all_collisions_flat_times, all_collisions_flat_disps)

plt.xlabel("Time (s)")
plt.ylabel("Displacement (mm)")
#plt.title("NewVideo1_9_28_18")
plt.title("Repeat Video 2")
plt.show()

'''

#IMPORTANT
#FOR VELOCITY PLOTTING PURPOSES - IF A VELOCITY WAS "-" I CHANGED IT TO NOT SAVE THAT COLLISION IN LIST

   # NOT DONE YET - concurrent hits stuff
'''
total_concurrents = 0
total_diff_subj_concurrent = 0
for x in all_collisions_flat_bytime: # at this collision time.....
	#num_concurrent = 0
	#diff_subj_concurrent = 0
	all_colliders = []
	self_collisions = 0
	for y in all_collisions_flat_bytime: # comparing with every other collision time....
		if (x != y): # not comparing with self
			if (math.sqrt((y[0]-x[0])**2) <= 0.5): # who is within a half second of me....
				print(mins(x[0]), mins(y[0]), x[4], y[4]) 
				#num_concurrent += 1
				total_concurrents += 1
				if (x[4] != y[4]): # if it's someone else.... 
					#print("YOOOOOOO")
					#diff_subj_concurrent += 1
					all_colliders.append((y[0], y[4])) # .....put them and their time on the list
				else:
					self_collisions += 1
	print(all_colliders)
	#print(len(all_colliders))
	total_diff_subj_concurrent += len(all_colliders)
	#print(num_concurrent)
	#total_diff_subj_concurrent += diff_subj_concurrent
print(total_concurrents)
print(total_diff_subj_concurrent)
# these numbers should be halved because they are counted twice?
'''
'''
multi_times = []
for x in all_collisions_flat_bytime: # at this collision time
	all_colliders = []
	self_collisions = 0
	for y in all_collisions_flat_bytime: # compare with every other time
		if (x != y): # not self
			if (math.sqrt((y[0]-x[0])**2) <= 0.5): # within a half second
				if y[0] > x[0]: # if the event is after me, count it   (if before me, then i am counted by it)
					if (x[4] != y[4]): # not the same
						#if(dist(x[5], y[5]) >= 0.5): # not overlapping wts (double tag)
						all_colliders.append([y[0], y[4], dist(x[5], y[5])]) # list of WTs colliding after me

					else: 
						self_collisions += 1
	if (len(all_colliders)) > 0:
		all_colliders.append([x[0], x[4], 0])
		multi_times.append(x[0]) # record multi collision
		print(mins(x[0]))
		print(all_colliders)



all_times_multi_or_not = []
for x in all_collisions_flat_times:
	if (x in multi_times):
		all_times_multi_or_not.append(1)
	else:
		all_times_multi_or_not.append(0)
'''
'''
plt.xlabel("Time (s)")
plt.ylabel("num_multicolls")
#plt.title("NewVideo1_9_28_18")
plt.title("Repeat Video 2")
plt.scatter(all_collisions_flat_times, all_times_multi_or_not)
plt.show()
'''
'''
# manually bin the times
multi_times_binned = [0]*24
for time in all_collisions_flat_times: # for all times
	if time in multi_times:
		multi_times_binned[math.floor(time/60)] += 1 # minute bin increases
print(multi_times_binned)

plt.xlabel("Time (m)")
plt.ylabel("Concurrent Hits")
plt.title("NewVideo1_9_28_18")
#plt.title("Repeat Video 2")
plt.scatter(range(24), multi_times_binned)
plt.show()
# plot x as times (binned?) and y as sum within bin
#print(all_collisions_flat_bytime)
	#print(x[0])
	#print(all_colliders)

'''
# Plot hits over time?

# Plot velocities over time
	# if nan then dont plot obv but do count and report percentage nan



