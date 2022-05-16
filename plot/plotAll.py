# Kate Bowers
# Levin Lab Tufts University
# Program development started March 2021
# Beckman Scholars - Tadpole Bullying
# plotAll.py -- makes graphs for collision statistics for each video
import matplotlib.pyplot as plt


def makePlots(video_collisions, min_def_time):
        '''
        print(len(video))
        x = len(list(filter(lambda video: video[0] < min_def_time, 
        video)))
        print(x)
        num_under += x
        '''
        # Filter out the collisions after the minimum time with def (min def time)
        # TODO this means this code doesnt report every collision in the video - time filtered

        filtered_collision = list(filter(lambda collision: collision[0] < min_def_time,
                                         video_collisions))
        print(len(filtered_collision))

        filtered_flat_times = list(map(lambda x: x[0], filtered_collision))
        filtered_flat_disps = list(map(lambda x: x[1], filtered_collision))
        filtered_flat_velocities = list(map(lambda x: x[2], filtered_collision))
        filtered_flat_videoIDs = list(map(lambda x: x[6], filtered_collision))

        print(filtered_flat_videoIDs)

        plt.xlabel("Time (s)")
        plt.ylabel("Collision frequency")
        # plt.title("NewVideo1_9_28_18")
        plt.title("Collision frequency (bin = 5s)")
        res = plt.hist(filtered_flat_times, bins=list(x * 5 for x in range(19 * 12)),
                       density=False)  # bin for every 5 seconds ////minute
        # TODO the time interval here is hardcoded oops
        # plt.hist(all_collisions_flat_times, bins=list(range(1450)))
        plt.show()

        # VELOCITIES OVER TIME - NEW VERSION ALL ALREADY UNDER 150
        plt.scatter(filtered_flat_times, filtered_flat_velocities)
        plt.xlabel("Time (s)")
        plt.ylabel("Velocity (mm/s)")
        # plt.title("NewVideo1_9_28_18")
        plt.title("Collision velocities over time")
        plt.show()

        # DISPLACEMENTS OVER TIME
        plt.scatter(filtered_flat_times, filtered_flat_disps)
        plt.xlabel("Time (s)")
        plt.ylabel("Displacement (mm)")
        # plt.title("NewVideo1_9_28_18")
        plt.title("Displacement of deformed tadpole in collisions over time")
        plt.show()

        # VELOCITIES VS DISPLACEMENTS
        plt.scatter(filtered_flat_velocities, filtered_flat_disps)
        plt.xlabel("Collision Velocity (mm/s)")
        plt.ylabel("Displacement (mm)")
        # plt.title("NewVideo1_9_28_18")
        plt.title("Collision velocities vs deformed tadpole displacement over time")
        plt.show()