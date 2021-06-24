# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# findCollisions.py -- compare paths of a wild-type and the deformed tadpole, identify collisions

import os
import csv
from utilities import dist, mins, TOO_CLOSE, NECESSARY_DISTANCE, PROXIMITY_DISTANCE
from isRedundant import is_redundant
from event import Event, Collision

# branching this is probably best bet


def find_collisions(wt_num, def_num, csvs_path, wrong_distances, def_start, all_collisions):
    print("starting ", wt_num)
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

        # Initialize variables for tracking events in this WT csv
        already_in_proximity = False
        WTevents = []
        currEvent = None

        first_prox_window = True  # this is the window where the collision timestamp happens

        num_lost = 0
        w_lost = 0  # i don't ever really use these trackers though?
        d_lost = 0

        counter = 0 # temporary
        for drow, wrow in zip(def_reader, wt_reader):
            counter += 1
            if counter > 28500:  # look at first 15:45 ish (end of my annotated collision list)
                # in orig results contains 1 ongoing and one graze
                 break

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
            if (wrong_distances):
                distance = distance / 10
            # One of my experiment files was calibrated wrong and has all distances off by a factor of 10
            # This corrects for distance discrepancy
            # if (wrong_distances):
            #     significant_distance = 50
            #     necessary_distance = 40
            #     too_close_dist = 5
            # else:
            #     significant_distance = 5
            #     necessary_distance = 4
            #     too_close_dist = 0.5

            # Now we look for collisions

            if ((distance <= PROXIMITY_DISTANCE)):  # within significant proximity to deformed
                if ((not already_in_proximity) and (distance > TOO_CLOSE)):  # new proximity event to follow

                    print(mins(curr_time), distance, "new event")
                    # ddeal with existing event
                    # then make new one
                    # Close any ongoing proximity event, record collision if it is valid
                    if (len(WTevents) != 0):
                        if (WTevents[-1] != currEvent):   # CHECK
                            print("AHHHHHHH")
                            return
                        if not currEvent.timed_out:
                            if (currEvent.collisionValid()):
                                # maybe a probelm here is passing the wxy and not the collision wxy
                                # for right now i should just pass the current wxy to try to replicate results
                                if not(is_redundant(all_collisions, (currEvent.collision_time, wt_num,
                                                                    wxy), wrong_distances)):
                                    # add colliison
                                    return # TODO ADD COLLISION LOL and modify velocity if wrong distances
                                    # if (wrong_distances):
                                    #     vel = currEvent. / 10
                        # if (prox_duration > 1) and (vel_of_smallest_dist != "-"):
                        #     # Calculate time, vel, disp
                        #     # TODO figure out what time should be? idk what was changed
                        #     time = time_of_smallest_dist # - float( TODO i made it just tosd
                        #         # def_start) + 1.034)  # @@@@@ woooo change mee back when u need to compare
                        #     vel = float(vel_of_smallest_dist) if not wrong_distances \
                        #         else float(vel_of_smallest_dist) / 10
                        #     disp = dist(dxy, dxy_of_smallest_dist) if not wrong_distances \
                        #         else dist(dxy, dxy_of_smallest_dist) / 10
                    # Create and add new event
                    currEvent = Event(curr_time, distance, wrow[8], dxy, wxy, def_num, wt_num, )
                    WTevents.append(currEvent)
                    already_in_proximity = True  # for future timepoints

                # Not a new event, but the next timepoint in an ongoing event
                elif (already_in_proximity):
                    print(mins(curr_time), distance, "continuing")
                    currEvent.updateSelf(distance, curr_time, wrow[8], dxy, wxy)
                    WTevents[-1] = currEvent  # update complete list
            else:  # not in proximity
                # print("not in proximity")
                already_in_proximity = False  # will end proximity event


            # Calculate displacements after 2s
            # this is a problem because just because there's A smallest dist doesn't mean it'll be THE smallest dist?
            # is it likely that the real collision will happen more than 3s after the proximity begins
            # collision is smallest dist within first 3s?

            # if time_of_smallest_dist is not None:  # if there is an existing collision on record
            #     if (curr_time >= time_of_smallest_dist + 5) and (not timed_out):
            #         print(mins(curr_time), "doing the timeout thing")
            #         # if at least 5 seconds since collision passed and displacement not yet calculated
            #         #  TODO make global constants for time and other stuff lol
            #         # problem is that displacement can get off maybe if it is hit by another WT in this time
            #         #    -- drift does not close based on ANY other collision happening in that time :/
            #         #    and can't really be done because these are not calcd in order
            #
            #         # Copying collision recording code from earlier
            #         if (prox_duration > 1) and (vel_of_smallest_dist != "-"):
            #             # Calculate time, vel, disp
            #             time = time_of_smallest_dist  # - float( TODO i changed the time to just tosd
            #                 # def_start) + 1.034)  # @@@@@ woooo change mee back when u need to compare
            #             # TODO figure out what time should be? idk what was changed
            #             vel = float(vel_of_smallest_dist) if not wrong_distances \
            #                 else float(vel_of_smallest_dist) / 10
            #             disp = dist(dxy, dxy_of_smallest_dist) if not wrong_distances \
            #                 else dist(dxy, dxy_of_smallest_dist) / 10
            #             if (vel < 150):
            #                 if (smallest_dist_so_far > too_close_dist) and \
            #                         (smallest_dist_so_far <= necessary_distance) and \
            #                         (not is_redundant(all_collisions, (time, wt_num, wxy), wrong_distances)):
            #                     #    (smallest_dist_so_far <= necessary_distance) and \
            #                     if ((curr_time - latest_committed_prox) >= 0.101):
            #                         all_collisions.append(
            #                             (time,  # time corrected for when def shows up
            #                              disp,
            #                              vel,
            #                              True,
            #                              wt_num,
            #                              wxy,
            #                              def_num,
            #                              prox_duration,
            #                              smallest_dist_so_far) # ,
            #                              # mins(prox_start_time),
            #                              # mins(latest_prox_time))
            #                         )
            #                         print("just added ", (time,
            #                                               disp,
            #                                               vel,
            #                                               True,
            #                                               wt_num,
            #                                               wxy,
            #                                               def_num,
            #                                               prox_duration,
            #                                               smallest_dist_so_far))
            #                         latest_committed_prox = latest_prox_time
            #                     else:
            #                          print((mins(curr_time), wt_num, "better luck next time - timed out btw"))
            #         # True is because it's a clean collision (2s displacement after)
            #         # Though like .. could be not clean at all bc who knows if a diff WT hit the deformed and the
            #         #   "displacement" we record for it is due to the other WT's collision
            #         timed_out = True
            # last_dxy = dxy
        last_time = curr_time
    time_with_def = last_time - def_start  # i added this new - check if it works right?
    print("END OF WT ", wt_num, " :: ", len(all_collisions))
    return (all_collisions, time_with_def)