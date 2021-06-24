# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# event.py -- class declaration for Event class

from utilities import mins, PROXIMITY_DISTANCE, NECESSARY_DISTANCE, TOO_CLOSE
from isRedundant import is_redundant


# TODO i want to get rid of timed_out as a concept but should just implement classes in general first
class Event:
    # initialize Event variables for the very first timepoint of the event
    def __init__(self, start, dist, vel, dxy, wxy, def_num, wt_num):
        self.duration = 1
        self.start_time = start
        self.collision_dist = dist # collision variables will be updated as the event continues
        self.collision_vel = vel
        self.collision_time = start
        self.collision_dxy = dxy
        self.collision_wxy = wxy
        self.timed_out = False
        self.def_num = def_num
        self.wt_num = wt_num

    # collisionValid returns True if the event at its current state is a valid collision to record, False if not
    def collisionValid(self):
        if (self.duration > 1) and (self.collision_vel != "-"):
            if (self.collision_vel < 150) and \
                    (TOO_CLOSE < (self.collision_dist) < NECESSARY_DISTANCE):
                # TODO Can't fit is_redundant into this scope: check beforehand - must add for good functionality
                return True
        return False

    # updateSelf always updates the event duration, and the collision details if needed
    def updateSelf(self, distance, curr_time, curr_vel, curr_dxy, curr_wxy):
        self.duration += 1
        if (curr_time < self.collision_time + 2): # less than 2s since last updated coll time
            if (TOO_CLOSE < distance < self.collision_dist):
                self.collision_dist = distance
                self.collision_vel = curr_vel
                self.collision_time = curr_time
                self.collision_dxy = curr_dxy
                self.collision_wxy = curr_wxy
                print("updated distance to ", self.collision_dist, " at ", curr_time)



# self.collision_vel = float(self.collision_vel) if not self.wrong_dists \
#     else float(self.collision_vel) / 10
# self.collision_disp = dist(dxy, dxy_of_smallest_dist) if not wrong_distances \
#     else dist(dxy, dxy_of_smallest_dist) / 10
class Collision:
    def __init__(self, time, disp, vel, clean, wt_num, wxy, def_num, duration, dist):
        self.time = time
        self.vel = vel
        self.disp = disp
        self.clean = clean
        self.wt_num = wt_num
        self.wxy = wxy
        self.def_num = def_num
        self.duration = duration
        self.dist = dist

    def printSelf(self):
        print(
            mins(self.time),
            self.vel,
            self.disp,
            self.clean,
            self.wt_num,
            self.duration,
            self.dist
        )
