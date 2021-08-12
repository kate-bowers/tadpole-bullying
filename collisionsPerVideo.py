# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# collisionsPerVideo.py -- for a given video csv folder, computes all collisions between WT and deformed tadpoles

from utilities import mins, find_def_start_time, makeSteps
import findCollisionsClasses # UPDATED FOR CLASSES BRANCH
import matplotlib.pyplot as plt
import numpy as np

def find_collisions_per_video(datfile, csvs_path):
    # datfile - wt num, wrong_distances, num of tadpoles
    print(csvs_path)
    def_num = datfile[0]
    wrong_distances = datfile[1]
    num_tads = datfile[2]

    # Calculate for all
    all_collisions = []
    all_steps = [] # for plotting
    total_collisions = 0

    # Know when the deformed tadpole shows up
    def_start_time = find_def_start_time(def_num, csvs_path)
    time_with_def = None

    for subject in range(1, num_tads):  # calculate for all
        if subject == def_num:  # skip deformed lol
            continue
        result = findCollisionsClasses.find_collisions(subject, def_num, csvs_path, wrong_distances, \
                                                       def_start_time, all_collisions)
        # this is where I would add the plot stuff
        subj_collisions = result[2]
        timeline = result[3]
        timer = 28500 # TODO this is just the limit in steps for testing (ie first 15 min = 28500 slots)
        print("making steps for ", subject)
        subj_steps = makeSteps(subj_collisions, list(timeline[:timer + 1]))
        all_steps.append(list(subj_steps))


        all_collisions = list(result[0]) # because all colliisons is reset every time
        time_with_def = result[1]  # this is a stupid way to find this

    #  do the plot here TODO ayy
    cmap = plt.cm.get_cmap("hsv", len(all_steps))
    print("made cmap")
    fig, ax = plt.subplots(figsize=(12, 6))
    print("made fig ax")
    plt.ylim(0,20)
    #plt.xlim(0,25)
    #plt.xticks(timeline)
    #print("made xticks")

    for i in np.arange(0, len(all_steps)):
        print("steppping")
        plt.step(timeline, all_steps[i], c=cmap(i), where='post')
        print("done")
        #break
        #scatter(X, Y, c=cmap(i))
    plt.xlabel("Time(s)")
    plt.ylabel("Collision Velocity (mm/s)")
    plt.show()
    print("made show")

    #####

    total_collisions = len(all_collisions)
    print(str(total_collisions) + " by " + str(num_tads - 1) + " wt tadpoles")  # + " in " + deformed_csv[14][1])
    print("in " + mins(time_with_def))
    # Flatten into time-based mega list
    # print(all_collisions)
    # all_collisions_flat_bytime = sum(all_collisions, []) # flattens from subjects to full video
    # sort by time
    all_collisions_flat_bytime = all_collisions
    all_collisions_flat_bytime.sort(key=lambda x: x.time)

    # report_concurrents(all_collisions_flat_bytime, def_num, csvs_path, def_start_time, num_tads)   # concurrents

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

