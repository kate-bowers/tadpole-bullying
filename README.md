# Overview
A program to identify collisions by wild-type tadpoles against deformed tadpoles in Ethovision XT15 track export files. Made by Kate Bowers for the Tufts University Levin Lab tadpole bullying project.

# Installation and Execution
This code is written in Python 3.7 with openpyxl, matplotlib, and numpy as dependencies. 

Download and unzip code in your preferred directory. The dependencies on this project are pretty minimal, but you can do it in a virtual environment if you want to control your package installations.

In terminal/command prompt, navigate to that directory and enter `make setup` to install the required packages with pip.

Then, enter `make run` and follow prompts.

# Notes for Input and Output
When prompted for a data folder, choose your folder of Ethovision track output Excel files. These files should all be of the same experiment type (ie all controls or all experimental) as the thresholds for identifying collisions and interactions (named the proximity distance and necessary distance) are different for control (pebble) videos and experimental videos since the pebbles are larger than the tadpoles.

I recommend 5.5 (mm) as a proximity distance for all experiments, 4.2 as a necessary distance for experimental videos, and 5 as a necessary distance for control videos.

# Plots
I have made many plots for this project with Python over the years. I included all of those files in the /plot/ directory, though they are not called by the program. Feel free to browse and reuse code. The data for those is typically hard coded in. Also, there are many commented-out parts of the sourcecode that encode more plots (ie zoomed-in versions of the output plots with different axes). Feel free to uncomment these on your local copy and play around with different visualization. For simplicity, I only left in the overall collision overview for each video, but zooming in would show more nuance to the plots including collision duration and overlap of ongoing collisions.

# Improvements
This program probably has some remaining flaws and bugs. I have moved on from Tufts, but feel free to submit pull requests for them if you fix anything.

# Contact
This project has moved on from me (Kate) to another Levin lab member, but feel free to contact me with any code related questions at kbowers405 (at) gmail (dot) com with any questions.
