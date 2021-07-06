# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# event.py -- class declaration for Event class

from utilities import mins, dist, PROXIMITY_DISTANCE, NECESSARY_DISTANCE, TOO_CLOSE
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
        self.collision_window_open = False
        self.collision_found = False

    # collisionValid returns True if the event at its current state is a valid collision to record, False if not
    # helper function to tryAddCollision
    def collisionValid(self):
        if (self.duration > 1) and (self.collision_vel != "-"):
            if (self.collision_vel < 150) and \
                    (TOO_CLOSE < (self.collision_dist) < NECESSARY_DISTANCE):
                return True
        return False

    # updateSelf always updates the event duration, and the collision details if needed
    def updateSelf(self, distance, curr_time, curr_vel, curr_dxy, curr_wxy):
        self.duration += 1
        # self.collision_window_open and
        if self.collision_window_open and \
                not self.collision_found and \
                curr_time < self.collision_time + 2:  # less than 2s since last updated coll time
            if TOO_CLOSE < distance < self.collision_dist:
                self.collision_dist = distance
                self.collision_vel = curr_vel
                self.collision_time = curr_time
                self.collision_dxy = curr_dxy
                self.collision_wxy = curr_wxy
                print("updated distance to ", self.collision_dist, " at ", curr_time)

    # determine if this event's collision is all set to record
    def tryAddCollision(self, wrong_distances, all_collisions, dxy, clean):
        if self.collision_vel != "-":
            self.collision_vel = float(self.collision_vel) / 10 if wrong_distances \
                else float(self.collision_vel)  # this is a very local change
            if self.collisionValid():  # vel, distance, etc check
                if not (is_redundant(all_collisions, (self.collision_time, self.wt_num,
                                                      self.collision_wxy), wrong_distances)):
                    # Create and record new collision

                    disp = dist(dxy, self.collision_dxy) if not wrong_distances \
                        else dist(dxy, self.collision_dxy) / 10
                    collisionNew = Collision(self.collision_time, disp,
                                             self.collision_vel,
                                             clean, self.wt_num, self.collision_wxy,
                                             self.def_num, self.duration,
                                             self.collision_dist)
                    return collisionNew


# self.collision_vel = float(self.collision_vel) if not self.wrong_dists \
#     else float(self.collision_vel) / 10
# self.collision_disp = dist(dxy, dxy_of_smallest_dist) if not wrong_distances \
#     else dist(dxy, dxy_of_smallest_dist) / 10
class Collision:
    def __init__(self, time, disp, vel, clean, wt_num, wxy, def_num, duration, distance):
        self.time = time
        self.vel = vel
        self.disp = disp
        self.clean = clean
        self.wt_num = wt_num
        self.wxy = wxy
        self.def_num = def_num
        self.duration = duration
        self.distance = distance

    def printSelf(self):
        print(mins(self.time), tuple((self.time, self.disp, self.vel, self.clean, self.wt_num,
              self.wxy, self.def_num, self.duration, self.distance)))
        '''
        print("just added, ",
            mins(self.time),
            self.vel,
            self.disp,
            self.clean,
            self.wt_num,
            self.duration,
            self.distance
        )
        '''

