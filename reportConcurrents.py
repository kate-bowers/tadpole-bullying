# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# reportConcurrents.py -- in a list of collisions, report all of the concurrent collisions

import os
import math
from utilities import mins


def report_concurrents(collisions, wt_num, csvs_path, deftime, num_tads):
    # within each video collision list
    print("WOOOOOOOOO")
    concurrents = open(os.path.join(csvs_path, str(wt_num) + "_new_output.txt"), "w")
    concurrents.write(str(deftime) + '\n')
    total_concurrents = 0
    total_diff_subj_concurrent = 0
    wot = 0
    unique_concurrents = [] * num_tads
    for x in collisions:  # at this collision time.....
        # num_concurrent = 0
        # diff_subj_concurrent = 0
        all_colliders = []
        self_collisions = 0
        for y in collisions:  # comparing with every other collision time....
            if (x != y):  # not comparing with self
                if (math.sqrt((y[0] - x[0]) ** 2) <= 0.5):  # who is within a half second of me....

                    # num_concurrent += 1
                    total_concurrents += 1
                    theirs = unique_concurrents[y[4] - 1]
                    if (y[0], x[0], y[4], x[4]) not in theirs:
                        if (x[4] != y[4]):  # if it's someone else....
                            # print("YOOOOOOO")
                            # diff_subj_concurrent += 1
                            wot += 1
                            print("writing for ", wt_num)
                            concurrents.write(str(mins(x[0])) + " " + str(mins(y[0])) +
                                              " " + str(x[4]) + " " + str(y[4]) + '\n')
                            all_colliders.append((x[0], y[0], x[4], y[4]))  # .....put them and their time on the list
                            unique_concurrents[x[4] - 1].append((x[0], y[0], x[4], y[4]))
            else:
                self_collisions += 1
        # print(all_colliders)
        # print(len(all_colliders))
        total_diff_subj_concurrent += len(all_colliders)

    # print(num_concurrent)
    # total_diff_subj_concurrent += diff_subj_concurrent
    concurrents.write(str(total_concurrents) + '\n')
    concurrents.write(str(total_diff_subj_concurrent) + '\n')
    concurrents.write(str(wot) + '\n')
    concurrents.close()
