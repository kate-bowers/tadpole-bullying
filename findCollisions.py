# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# findCollisions.py -- compare paths of a wild-type and the deformed tadpole, identify collisions

import os
import csv
from utilities import dist, mins
from isRedundant import is_redundant

# branching this is probably best bet

# def add_collision():   #  TODO make function - maybe in class because i dont wanna pass all these vars
#     if (prox_duration > 1) and (vel_of_smallest_dist != "-"):
#         if ((float(curr_time) - latest_prox_time) >= 0.101):
#             # Calculate time, vel, disp
#             # TODO figure out what time should be? idk what was changed
#             time = (float(time_of_smallest_dist))  # - float( TODO i made it just tosd
#             # def_start) + 1.034)  # @@@@@ woooo change mee back when u need to compare
#             vel = float(vel_of_smallest_dist) if not wrong_distances \
#                 else float(vel_of_smallest_dist) / 10
#             disp = float(dist(dxy, dxy_of_smallest_dist)) if not wrong_distances \
#                 else float(dist(dxy, dxy_of_smallest_dist)) / 10
#
#             if (vel < 150):
#                 if (smallest_dist_so_far > too_close_dist) and \
#                         (not is_redundant(all_collisions, (time, wt_num, wxy), wrong_distances)):
#                     all_collisions.append(
#                         (time,  # time corrected for when def shows up
#                          disp,
#                          vel,
#                          False,
#                          wt_num,
#                          wxy,
#                          def_num,
#                          prox_duration,
#                          prox_start_time)
#                     )
#             # End work on old event
#         else:
#             all_collisions.append((curr_time, "better luck next time"))

def find_collisions(wt_num, def_num, csvs_path, wrong_distances, def_start, all_collisions):
    def_start = float(def_start)
    deformed_csv = os.path.join(csvs_path, f"track-arena_1-subject_{def_num}.csv")
    wt_csv = os.path.join(csvs_path, f"track-arena_1-subject_{wt_num}.csv")

    # READING IN DATA & ISOLATING XY COORDS
    with open(deformed_csv, newline='') as def_f, open(wt_csv, newline='') as wt_f:
        def_reader = csv.reader(def_f)
        wt_reader = csv.reader(wt_f)

        for _ in range(36):  # skips the 36 header lines
            next(wt_reader)
            next(def_reader)

        # Initialize variables for tracking proximity event details
        already_in_proximity = False
        prox_start_time = None
        prox_duration = 0
        latest_committed_prox = 0  # there is no collisions listed yet
        smallest_dist_so_far = None
        vel_of_smallest_dist = None
        time_of_smallest_dist = None
        dxy_of_smallest_dist = []
        timed_out = False

        # active_disp = None # I DONT THINK THIS DOES ANYTHING?
        num_lost = 0
        w_lost = 0  # i don't ever really use these trackers though?
        d_lost = 0

        # last_dxy = None # hmm what do i even use this for? "frdist" - not sure thats relevant anymore

        for drow, wrow in zip(def_reader, wt_reader):
            if float(drow[0]) < float(def_start): continue  # if the def tadpole isnt here yet, ignore

            dxy = drow[2:4]
            wxy = wrow[2:4]
            curr_time = float(wrow[0])
            #curr_vel = float(wrow[8])

            # Filter out timepoints where either tadpole is lost
            if wxy[0] == "-":
                w_lost += 1
                continue
            if (dxy[0] == "-"):
                # hopefully manual correction will ensure the def tadpole is only lost when no collisions happen
                d_lost += 1
                continue

            # Calculate distance between tadpoles
            dxy[0], dxy[1], wxy[0], wxy[1] = float(dxy[0]), float(dxy[1]), float(wxy[0]), float(wxy[1])
            distance = dist(dxy, wxy)

            # One of my experiment files was calibrated wrong and has all distances off by a factor of 10
            # This corrects for distance discrepancy
            if (wrong_distances):
                significant_distance = 40
                too_close_dist = 5
            else:
                significant_distance = 4
                too_close_dist = 0.5

            # Now we look for collisions
            if ((distance <= significant_distance)):  # within significant proximity to deformed
                if ((not already_in_proximity) and (distance > too_close_dist)):  # new proximity event to follow

                    # Close any ongoing proximity event, record collision if it is valid
                    if (prox_start_time is not None) and (not timed_out):
                        # If the collision is valid, record it
                        # (future) Do not count a "collision" that happens less than
                        # 3 time points since the last logged proximity
                        if (prox_duration > 1) and (vel_of_smallest_dist != "-"):
                            # Calculate time, vel, disp
                            # TODO figure out what time should be? idk what was changed
                            time = time_of_smallest_dist # - float( TODO i made it just tosd
                                # def_start) + 1.034)  # @@@@@ woooo change mee back when u need to compare
                            vel = float(vel_of_smallest_dist) if not wrong_distances \
                                else float(vel_of_smallest_dist) / 10
                            disp = dist(dxy, dxy_of_smallest_dist) if not wrong_distances \
                                else dist(dxy, dxy_of_smallest_dist) / 10

                            if (vel < 150):
                                if (smallest_dist_so_far > too_close_dist) and \
                                        (not is_redundant(all_collisions, (time, wt_num, wxy), wrong_distances)):
                                    if (curr_time - latest_committed_prox >= 0.101):
                                        all_collisions.append(
                                            (time,  # time corrected for when def shows up
                                             disp,
                                             vel,
                                             False,
                                             wt_num,
                                             wxy,
                                             def_num,
                                             prox_duration)  # ,
                                             # prox_start_time)
                                        )
                                        latest_committed_prox = latest_prox_time
                            # End work on old event
                                    else:
                                         print((mins(curr_time), wt_num, "better luck next time"))

                    # Initialize variables for new event
                    prox_start_time = curr_time
                    latest_prox_time = curr_time
                    timed_out = False
                    already_in_proximity = True  # for future timepoints
                    prox_duration = 1
                    smallest_dist_so_far = distance
                    vel_of_smallest_dist = wrow[8]
                    time_of_smallest_dist = curr_time
                    dxy_of_smallest_dist = dxy
                    # sum_movement = 0  # I don't think these are relevant but not deleting yet
                    # sum_frdist = 0
                    # if (drow[7] != '-'):  # set new active disp
                    #     active_disp = float(drow[7])
                    # else:
                    #     active_disp = 0

                # Not a new event, but the next timepoint in an ongoing event
                elif (already_in_proximity):
                    prox_duration += 1
                    latest_prox_time = curr_time
                    if (curr_time < time_of_smallest_dist + 2):  # it's been less than 2s since we found the smallest dist
                        if (distance < smallest_dist_so_far):  # Update if this is the smallest distance so far
                            # TODO should be more than min distance though
                            smallest_dist_so_far = distance
                            vel_of_smallest_dist = wrow[8]
                            time_of_smallest_dist = curr_time
                            dxy_of_smallest_dist = dxy
                            # if (drow[7] != '-'):
                            #     active_disp = float(drow[7])  # displacement resets when new small dist does
                            # else:
                            #    active_disp = 0    # IDK WHAT ALL THESE ACTIVE DISP THINGS ARE
                        # else:  # not a new smaller dist
                        #    if (drow[7] != '-'):
                        #        active_disp += float(drow[7])  # update active displacement

                    # if (not timed_out):  # TODO is any of this relevant?
                        # frdist = (dist(dxy, last_dxy))  # again, IDK what this is
                        # if (drow[7] == '-'):  # no movement
                        #     sum_movement += 0
                        # else:
                        #    sum_movement += float(drow[7])
                        # sum_frdist += frdist

            else:  # not in proximity
                already_in_proximity = False  # will end proximity event

            # Calculate displacements after 2s
            # this is a problem because just because there's A smallest dist doesn't mean it'll be THE smallest dist?
            # is it likely that the real collision will happen more than 3s after the proximity begins
            # collision is smallest dist within first 3s?

            if time_of_smallest_dist is not None:  # if there is an existing collision on record
                if (curr_time >= time_of_smallest_dist + 5) and (not timed_out):
                    # if at least 5 seconds since collision passed and displacement not yet calculated
                    #  TODO make global constants for time and other stuff lol
                    # problem is that displacement can get off maybe if it is hit by another WT in this time
                    #    -- drift does not close based on ANY other collision happening in that time :/
                    #    and can't really be done because these are not calcd in order

                    # Copying collision recording code from earlier
                    if (prox_duration > 1) and (vel_of_smallest_dist != "-"):
                        # Calculate time, vel, disp
                        time = time_of_smallest_dist  # - float( TODO i changed the time to just tosd
                            # def_start) + 1.034)  # @@@@@ woooo change mee back when u need to compare
                        # TODO figure out what time should be? idk what was changed
                        vel = float(vel_of_smallest_dist) if not wrong_distances \
                            else float(vel_of_smallest_dist) / 10
                        disp = dist(dxy, dxy_of_smallest_dist) if not wrong_distances \
                            else dist(dxy, dxy_of_smallest_dist) / 10
                        if (vel < 150):
                            if (smallest_dist_so_far > too_close_dist) and \
                                    (not is_redundant(all_collisions, (time, wt_num, wxy), wrong_distances)):
                                if ((curr_time - latest_committed_prox) >= 0.101):
                                    all_collisions.append(
                                        (time,  # time corrected for when def shows up
                                         disp,
                                         vel,
                                         True,
                                         wt_num,
                                         wxy,
                                         def_num,
                                         prox_duration) # ,
                                         # prox_start_time)
                                    )
                                    latest_committed_prox = latest_prox_time
                                else:
                                     print((mins(curr_time), wt_num, "better luck next time - timed out btw"))
                    # True is because it's a clean collision (2s displacement after)
                    # Though like .. could be not clean at all bc who knows if a diff WT hit the deformed and the
                    #   "displacement" we record for it is due to the other WT's collision
                    timed_out = True
            # last_dxy = dxy
        last_time = curr_time
    time_with_def = last_time - def_start  # i added this new - check if it works right?
    return (all_collisions, time_with_def)
