# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# findCollisions.py -- compare paths of a wild-type and the deformed tadpole, identify collisions

import os
import csv
from utilities import dist
from isRedundant import is_redundant

# branching this is probably best bet

def find_collisions(wt_num, def_num, csvs_path, wrong_distances, def_start, all_collisions):
    deformed_csv = os.path.join(csvs_path, f"track-arena_1-subject_{def_num}.csv")
    wt_csv = os.path.join(csvs_path, f"track-arena_1-subject_{wt_num}.csv")

    num_collisions = 0
    # collisions = []

    time_with_def = 0
    # READING IN DATA & ISOLATING XY COORDS
    with open(deformed_csv, newline='') as def_f, open(wt_csv, newline='') as wt_f:
        # proximity_times = open(os.path.join(folder_rv2, str(wt_num)+"output.txt"), "w") # should be path specific?
        def_reader = csv.reader(def_f)
        wt_reader = csv.reader(wt_f)

        for _ in range(36):  # skips the 36 header lines
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
            if (time_with_def < 0): continue

            dxy = drow[2:4]
            wxy = wrow[2:4]

            # Filter out lost timepoints
            if (wxy[0] == "-"):  # ok if doing individually but not if comparing more than 2 files here
                w_lost += 1
                continue

            if (dxy[0] == "-"):  # would suck bc we dont wanna miss def anywhere
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

            if ((distance <= significant_distance)):  # within significant proximity to deformed
                #  and (distance >= 5 mm)
                if ((not already_in_proximity) and (distance > too_close_dist)):

                    # DEAL WITH OLD EVENT
                    if (prox_start_time != None):  # there was a previous collision
                        if (not drift_closed):  # previous collision is still open
                            # REPORTS
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

                            # exclude velocity nans
                            if (prox_duration != 1):
                                # if (time_of_smallest_dist not in coll_times):
                                if (vel_of_smallest_dist != "-"):
                                    time = (float(time_of_smallest_dist) - float(
                                        def_start) + 1.034)  # @@@@@ woooo change mee back when u need to compare
                                    vel = float(vel_of_smallest_dist) if not wrong_distances else float(
                                        vel_of_smallest_dist) / 10
                                    disp = disp / 10 if wrong_distances else disp
                                    if (vel < 150):
                                        if (smallest_dist_so_far > too_close_dist):
                                            if (not is_redundant(all_collisions, (time, wt_num, wxy), wrong_distances)):
                                                all_collisions.append(
                                                    (time,  # time corrected for when def shows up
                                                     disp,
                                                     vel,
                                                     False,
                                                     wt_num,
                                                     wxy,
                                                     def_num)
                                                )
                                    # coll_times.append(time_of_smallest_dist) # update
                                # print("UPDSTED")
                            # else:
                            # print("HELPP")
                            # print(mins(time_of_smallest_dist), vel, def_num)
                            # else:
                                # ones += 1

                    prox_start_time = wrow[0]

                    # DEAL WITH NEW EVENT
                    # proximity_times.write("NEW EVENT at " + mins(prox_start_time) + "\n")
                    drift_closed = False
                    already_in_proximity = True  # update
                    prox_duration = 1
                    num_collisions += 1
                    smallest_dist_so_far = distance
                    vel_of_smallest_dist = wrow[8]
                    time_of_smallest_dist = float(wrow[0])
                    dxy_of_smallest_dist = dxy
                    sum_movement = 0
                    sum_frdist = 0
                    if (drow[7] != '-'):  # set new active disp
                        active_disp = float(drow[7])
                    else:
                        active_disp = 0

                elif (already_in_proximity):  # existing event
                    # proximity_times.write(str(distance) + "\n")   #	writes distance during event
                    prox_duration += 1
                    # print(time_of_smallest_dist)
                    # print(distance)
                    if (float(drow[0]) < float(
                            time_of_smallest_dist) + 2):  # it's been less than 2s since we found smallest dist
                        # proximity_times.write("smallest at " + mins(time_of_smallest_dist) + "\n")
                        if (distance < smallest_dist_so_far):  # update if smaller dist found
                            # proximity_times.write("UPDATED AT " + mins(drow[0]) + "\n")
                            smallest_dist_so_far = distance
                            vel_of_smallest_dist = wrow[8]
                            time_of_smallest_dist = float(wrow[0])
                            dxy_of_smallest_dist = dxy
                            if (drow[7] != '-'):
                                active_disp = float(drow[7])  # displacement resets when new small dist does
                            else:
                                active_disp = 0
                        else:  # not a new smaller dist
                            if (drow[7] != '-'):
                                # print(drow[0])
                                active_disp += float(drow[7])  # update active displacement
                    # print(drow)
                    '''

                    '''
                    if (not drift_closed):  # still moving
                        # proximity_times.write(drow[0] + " " + str(dxy_of_smallest_dist[0]) + " " + str(dxy_of_smallest_dist[1]) + "\n")
                        # proximity_times.write(drow[0] + " " + str(dxy[0]) + " " + str(dxy[1]) + "\n")
                        frdist = (dist(dxy, last_dxy))
                        # proximity_times.write('\n')
                        # if (drow[7] != '-'):
                        # proximity_times.write("diff is " + str((float(drow[7]) - frdist)/10) + "\n")
                        if (drow[7] == '-'):  # no movement
                            sum_movement += 0
                        else:
                            sum_movement += float(drow[7])
                        sum_frdist += frdist
                    # proximity_times.write("frdist so far: " + str(sum_frdist) + "\n")


            # proximity_times.write(str(drow[0]) + '\n') # report time in proxiity

            else:  # not in proximity
                already_in_proximity = False  # will end proximity event

            # Calculate displacements after 2s
            # this is a problem because just because there's A smallest dist doesn't mean it'll be THE smallest dist?
            # is it likely that the real collision will happen more than 3s after the proximity begins
            # collision is smallest dist within first 3s?

            if (time_of_smallest_dist != None):  # if there is an existing collision on record
                if ((float(drow[0]) >= float(time_of_smallest_dist) + 5) and (not drift_closed)):
                    # if at least 5 seconds since collision passed and displacement not yet calculated (this code hasn't yet run for it)
                    # used to be 2
                    # problem is that displacement can get off maybe if it is hit by another WT in this time
                    #    -- drift does not close based on ANY other collision happening in that time :/ and can't really be done because these are not calcd in order
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

                    # exclude velocity nans
                    disp = float(dist(dxy, dxy_of_smallest_dist))
                    if (prox_duration != 1):
                        # if(time_of_smallest_dist not in coll_times):
                        if (vel_of_smallest_dist != "-"):
                            vel = float(vel_of_smallest_dist) if not wrong_distances else (
                                        float(vel_of_smallest_dist) / 10)
                            disp = disp / 10 if wrong_distances else disp
                            time = float(time_of_smallest_dist) - float(def_start) + 1.034  # FOR NOWWWW @@@@@@@@
                            if (vel < 150):
                                if (smallest_dist_so_far > too_close_dist):
                                    if (not is_redundant(all_collisions, (time, wt_num, wxy), wrong_distances)):
                                        all_collisions.append(
                                            (time,
                                             disp,
                                             vel,
                                             True,
                                             wt_num,
                                             wxy,
                                             def_num)
                                        )
                            # coll_times.append(time_of_smallest_dist) # update
                            # print("WOO")
                    # else:
                    # print("HELPP")
                    # print(mins(time_of_smallest_dist), vel, def_num)
                    # else:
                        # ones += 1
                    # NaN velocities show up as "-"
                    # True is because it's a clean collision (2s displacement after)

                    # proximity_times.write("ends at " + mins(drow[0]) + "\n")
                    # proximity_times.write("smallest dist was "+ str(smallest_dist_so_far) + "\n")
                    # print(dxy_of_smallest_dist) # not necessarily defined but hopefully if statement fixes
                    # print('\n')
                    # proximity_times.write("disp calc w times of: " + mins(time_of_smallest_dist) + " to " + mins(drow[0]) + "\n")
                    # proximity_times.write("sum mvmt: " + str(sum_movement) + "\n")
                    # proximity_times.write("sum fr: " + str(sum_frdist) + "\n")
                    # proximity_times.write("active disp: " + str(active_disp) + "\n")
                    # proximity_times.write("diff: " + (str(dist(dxy, dxy_of_smallest_dist) - active_disp)) + "\n")
                    # proximity_times.write("lost w:" + str(w_lost) + " lost d:" + str(d_lost) + "\n")

                    # proximity_times.write("speed: " + str(vel_of_smallest_dist) + "\n")
                    drift_closed = True
            last_dxy = dxy

    # proximity_times.write(str(num_collisions))
    # proximity_times.close()
    # print(len(coll_times))
    # print(len(set(coll_times)))
    return (all_collisions, time_with_def)