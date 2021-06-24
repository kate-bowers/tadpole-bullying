# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# findCollisions.py -- compare paths of a wild-type and the deformed tadpole, identify collisions

from utilities import dist, mins
from isRedundant import is_redundant

def add_collision():   #  TODO make function - maybe in class because i dont wanna pass all these vars
    if (prox_duration > 1) and (vel_of_smallest_dist != "-"):
        if ((float(curr_time) - latest_prox_time) >= 0.101):
            # Calculate time, vel, disp
            # TODO figure out what time should be? idk what was changed
            time = (float(time_of_smallest_dist))  # - float( TODO i made it just tosd
            # def_start) + 1.034)  # @@@@@ woooo change mee back when u need to compare
            vel = float(vel_of_smallest_dist) if not wrong_distances \
                else float(vel_of_smallest_dist) / 10
            disp = float(dist(dxy, dxy_of_smallest_dist)) if not wrong_distances \
                else float(dist(dxy, dxy_of_smallest_dist)) / 10

            if (vel < 150):
                if (smallest_dist_so_far > too_close_dist) and \
                        (not is_redundant(all_collisions, (time, wt_num, wxy), wrong_distances)):
                    all_collisions.append(
                        (time,  # time corrected for when def shows up
                         disp,
                         vel,
                         False,
                         wt_num,
                         wxy,
                         def_num,
                         prox_duration,
                         prox_start_time)
                    )
            # End work on old event
        else:
            all_collisions.append((curr_time, "better luck next time"))