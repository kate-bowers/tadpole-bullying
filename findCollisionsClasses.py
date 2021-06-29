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

        counter = 0  # temporary
        for drow, wrow in zip(def_reader, wt_reader):
            counter += 1
            if counter > 28500:  # look at first 15:45 ish (end of my annotated collision list)
                # in orig results contains 1 ongoing and one graze
                break
            if float(drow[0]) < float(def_start):
                continue  # if the def tadpole isnt here yet, ignore

            dxy = drow[2:4]
            wxy = wrow[2:4]
            curr_time = float(wrow[0])
            # curr_vel = float(wrow[8])

            # Filter out timepoints where either tadpole is lost
            if wxy[0] == "-":
                w_lost += 1
                continue
            if dxy[0] == "-":
                # hopefully manual correction will ensure the def tadpole is only lost when no collisions happen
                d_lost += 1
                continue

            # Calculate distance between tadpoles
            dxy[0], dxy[1], wxy[0], wxy[1] = float(dxy[0]), float(dxy[1]), float(wxy[0]), float(wxy[1])
            distance = dist(dxy, wxy)
            if wrong_distances:
                distance = distance / 10
            # One of my experiment files was calibrated wrong and has all distances off by a factor of 10
            # This corrects for distance discrepancy

            # Now we look for collisions
            if distance <= PROXIMITY_DISTANCE:  # within significant proximity to deformed
                if (not already_in_proximity) and (distance > TOO_CLOSE):  # new proximity event to follow
                    print(mins(curr_time), distance, "new event")
                    # ddeal with existing event
                    # then make new one
                    # Close any ongoing proximity event, record collision if it is valid
                    if len(WTevents) != 0:
                        # currEvent is the last event in WTevents
                        if not currEvent.timed_out:
                            if currEvent.collision_vel != "-":
                                currEvent.collision_vel = float(currEvent.collision_vel) / 10 if wrong_distances \
                                    else float(currEvent.collision_vel)
                                if currEvent.collisionValid():  # vel, distance, etc check
                                    if not (is_redundant(all_collisions, (currEvent.collision_time, wt_num,
                                                                          wxy), wrong_distances)):  # TODO FIX WXY THING
                                        # Create and record new collision
                                        disp = dist(dxy, currEvent.collision_dxy) if not wrong_distances \
                                            else dist(dxy, currEvent.collision_dxy) / 10
                                        collisionNew = Collision(currEvent.collision_time, disp,
                                                                 currEvent.collision_vel,
                                                                 False, currEvent.wt_num, currEvent.collision_wxy,
                                                                 currEvent.def_num, currEvent.duration,
                                                                 currEvent.collision_dist)
                                        all_collisions.append(collisionNew)
                                        collisionNew.printSelf()

                    # Create and add new event
                    currEvent = Event(curr_time, distance, wrow[8], dxy, wxy, def_num, wt_num)
                    WTevents.append(currEvent)
                    already_in_proximity = True  # for future timepoints

                # Not a new event, but the next timepoint in an ongoing event
                elif already_in_proximity:
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

            if len(WTevents) != 0:  # if there is an existing collision on record # TODO is this a good feature
                if (curr_time >= currEvent.collision_time + 5) and (not currEvent.timed_out):
                    print(mins(curr_time), "doing the timeout thing")
                    # if at least 5 seconds since collision passed and displacement not yet calculated
                    #  TODO make global constants for time and other stuff lol
                    # problem is that displacement can get off maybe if it is hit by another WT in this time
                    #    -- drift does not close based on ANY other collision happening in that time :/
                    #    and can't really be done because these are not calcd in order
                    if currEvent.collision_vel != "-":
                        currEvent.collision_vel = float(currEvent.collision_vel) / 10 if wrong_distances \
                            else float(currEvent.collision_vel)
                        if currEvent.collisionValid():  # vel, distance, etc check
                            if not (is_redundant(all_collisions, (currEvent.collision_time, wt_num,
                                                                  wxy), wrong_distances)):  # TODO FIX WXY
                                # Create and record new collision
                                disp = dist(dxy, currEvent.collision_dxy) if not wrong_distances \
                                    else dist(dxy, currEvent.collision_dxy) / 10
                                collisionNew = Collision(currEvent.collision_time, disp,
                                                         currEvent.collision_vel,
                                                         True, currEvent.wt_num, currEvent.collision_wxy,
                                                         currEvent.def_num, currEvent.duration,
                                                         currEvent.collision_dist)
                                all_collisions.append(collisionNew)
                                collisionNew.printSelf()

                    # True is because it's a clean collision (2s displacement after)
                    # Though like .. could be not clean at all bc who knows if a diff WT hit the deformed and the
                    #   "displacement" we record for it is due to the other WT's collision
                    currEvent.timed_out = True
            last_dxy = dxy
        last_time = curr_time
    time_with_def = last_time - def_start  # i added this new - check if it works right?
    print("END OF WT ", wt_num, " :: ", len(all_collisions))
    return all_collisions, time_with_def
