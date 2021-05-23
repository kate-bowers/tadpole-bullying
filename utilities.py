# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# utilities.py -- straightforward utility functions for larger collision script

import math
import os
import csv


def dist(p1, p2):
    """Calculates Euclidean distance between two XY coordinate sets"""
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return dist


def mins(time):
    """Reports seconds as minutes:seconds format"""
    t = float(time)
    m = math.floor(t / 60)  # num of minutes
    s = t % 60
    return (str(m) + ":" + str(s)[:6])


def find_def_start_time(def_num, csvs_path):
    """"Scans through CSV of deformed tadpole to find timestamp it appears first"""
    deformed_csv = os.path.join(csvs_path, f"track-arena_1-subject_{def_num}.csv")

    with open(deformed_csv, newline='') as def_f:
        def_reader = csv.reader(def_f)

        for _ in range(36):  # skips the 36 header lines
            next(def_reader)

        for drow in def_reader:
            not_started = (drow[2] == "-")  # is location of deformed tadpole undefined
            if not not_started:  # location is known!
                print(mins(drow[0]))
                return drow[0]
