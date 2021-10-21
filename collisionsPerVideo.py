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

    for subject in range(1, num_tads + 1):  # calculate for all
        if subject == def_num:  # skip deformed lol
            continue
        result = findCollisionsClasses.find_collisions(subject, def_num, csvs_path, wrong_distances, \
                                                       def_start_time, all_collisions)
        # this is where I would add the plot stuff
        subj_collisions = result[2]
        timeline = result[3]
        timer = 28500 # TODO this is just the limit in steps for testing (ie first 15 min = 28500 slots)
        print("making steps for ", subject)
        subj_steps = makeSteps(subj_collisions, list(timeline))   # [:timer + 1])) removing timer for now
        all_steps.append(list(subj_steps))


        all_collisions = list(result[0]) # because all colliisons is reset every time
        time_with_def = result[1]  # this is a stupid way to find this

    #  do the plot here TODO ayy
    cmap = plt.cm.get_cmap("hsv", len(all_steps))
    print("made cmap")
    fig, (axoutlier, axmost) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios':[6,12]})
    fig.subplots_adjust(hspace=0.05)

    print("made fig ax")

    #plt.xticks(timeline)
    #print("made xticks")

    for i in np.arange(0, len(all_steps)):
        axmost.step(timeline, all_steps[i], c=cmap(i), where='post')
        axoutlier.step(timeline, all_steps[i], c=cmap(i), where='post')
        #break
        #scatter(X, Y, c=cmap(i))

    axmost.set_ylim(0, 12.5)
    axoutlier.set_yticks([25, 50, 75, 100, 125, 150, 175])
    #axmost.set_xlim(250, 400)
    axoutlier.set_ylim(12.5, 140)
    #axoutlier.set_xlim(250, 400)

    # box = axoutlier.get_position()
    # print(box)
    # box2 = axmost.get_position()
    # print(box)
    # plt.show()

    # axoutlier.spines.bottom.set_visible(False)
    # axmost.spines.top.set_visible(False)
    # axoutlier.xaxis.tick_top()
    #axoutlier.tick_params(labeltop=False)  # don't put tick labels at the top
    #axmost.xaxis.tick_bottom()

    # Now, let's turn towards the cut-out slanted lines.
    # We create line objects in axes coordinates, in which (0,0), (0,1),
    # (1,0), and (1,1) are the four corners of the axes.
    # The slanted lines themselves are markers at those locations, such that the
    # lines keep their angle and position, independent of the axes size or scale
    # Finally, we need to disable clipping.

    d = .5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                  linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    axoutlier.plot([0, 1], [0, 0], transform=axoutlier.transAxes, **kwargs)
    axmost.plot([0, 1], [1, 1], transform=axmost.transAxes, **kwargs)

    plt.xlabel("Time(s)")
    plt.ylabel("Collision Velocity (mm/s)")
    axoutlier.set_title("Collision duration and velocity over time \n"
              "in 15:45 min. video" )
    plt.show()

    print("made show")
    #
    # ##### TODO this is where i did the zoom in plot
    # cmap = plt.cm.get_cmap("hsv", len(all_steps))
    # print("made cmap")
    # axmost = plt.subplots(figsize=(8,4.8))
    # #fig.subplots_adjust(hspace=0.05)
    #
    # print("made fig ax")
    #
    # # plt.xticks(timeline)
    # # print("made xticks")
    #
    # for i in np.arange(0, len(all_steps)):
    #     plt.step(timeline, all_steps[i], c=cmap(i), where='post')
    #     #axoutlier.step(timeline, all_steps[i], c=cmap(i), where='post')
    #     # break
    #     # scatter(X, Y, c=cmap(i))
    #
    # plt.ylim(0, 12.5)
    # #axoutlier.set_yticks([25, 50, 75, 100, 125, 150, 175])
    # plt.xlim(250, 400)
    # #axoutlier.set_ylim(12.5, 140)
    # #axoutlier.set_xlim(250, 400)
    #
    #
    # # plt.show()
    # #
    # # d = .5  # proportion of vertical to horizontal extent of the slanted line
    # # kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
    # #               linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    # # axoutlier.plot([0, 1], [0, 0], transform=axoutlier.transAxes, **kwargs)
    # # axmost.plot([0, 1], [1, 1], transform=axmost.transAxes, **kwargs)
    #
    # plt.xlabel("Time(s)")
    # plt.ylabel("Collision Velocity (mm/s)")
    # plt.show()
    # print("made show")
    #



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

