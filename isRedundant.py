# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# isRedundant.py -- identifies if a given collision is redundant/multiple-ID #TODO this is a bad desc

from utilities import dist, mins


def is_redundant(collisions_so_far, curr_coll, wrong_distances):  # tells whether this is a redundant/multipleID WT collision
    # curr_coll -- time, wt_num, wxy,
    time = curr_coll[0]
    identity = curr_coll[1]
    xy = curr_coll[2]

    '''all_collisions.append(
        (float(time_of_smallest_dist) - float(def_start), #time corrected for when def shows up
            disp, 
            vel, 
            False,
            wt_num, 
            wxy,
            def_num)
        )'''

    for coll in collisions_so_far: # TODO i got rid of the print statements here dont forget
        if (abs(time - coll[0]) <= 0.5):  # within half a second
            if wrong_distances:
                distance = dist(coll[5], xy) / 10
            else:
                distance = dist(coll[5], xy)
            print("maybeing, ", distance)

            if (distance <= 3):  # within one mm idk lol
                print("redundant too close, ", distance, mins(time), mins(coll[0]), identity, coll[4])
                return True

            if (identity == coll[4]):
                print("redundant with self", mins(time), mins(coll[0]), identity, coll[4])
                return True

            else:
                print("naurrrr \n but yeet dist was ", distance, mins(time), mins(coll[0]), identity, coll[4])

    return False
