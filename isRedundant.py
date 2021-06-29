# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# isRedundant.py -- identifies if a given collision is redundant/multiple-ID #TODO this is a bad desc

from utilities import dist, mins


def is_redundant(collisions_so_far, curr_coll, wrong_distances):
    # tells whether this is a redundant/multipleID WT collision # TODO better description

    # curr_coll -- time, wt_num, wxy,
    time = curr_coll[0]
    identity = curr_coll[1]
    xy = curr_coll[2]

    for coll in collisions_so_far:
        other_time = coll.time
        other_id = coll.wt_num
        other_wxy = coll.wxy
        if abs(time - other_time) <= 0.5: # within half a second
            distance = dist(other_wxy, xy) / 10 if wrong_distances else dist(other_wxy, xy)
            print("maybeing, ", identity, " and ", other_id, " ", distance)

            if distance <= 3:  # within 3mm idk lol
                print("redundant too close, ", distance, mins(time), mins(other_time), identity, other_id)
                return True

            if identity == other_id:
                print("redundant with self", mins(time), mins(other_time), identity, other_id)
                return True

            else:
                print("naurrrr \n but yeet dist was ", distance, mins(time), mins(other_time), identity, other_id)

    return False
