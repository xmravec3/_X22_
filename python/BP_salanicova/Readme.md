# Visualization of speed climbing performances 
This is an attachment to my bachelor thesis. It contains all programs and data necessary to visualize and measure similarities and discrepencies in speed climbing performances on split-screen.

Guideline for split-screen



## Minimal working example 
1. Setup the envinroment by installing the packages listed in "requirements.txt" file (recommended to use Python 3.8 on Windows machine) 
2. Run the following python scripts from command line with the directory of this file as a working directory

 Original video
 * main.py "8_2019-08-17_1" "25_2019-08-17_1"
 
 Aligned video by height
 * main.py "8_2019-08-17_1" "25_2019-08-17_1" -s



## Data files folders:
 * unpacked_data - data files containt skeleton poses for each frame per annotated video
 * videa - cut-out videos
 * cut_out - absolute transformation matrices

## Python files
 * main.py - runs the program
 * compute.py - computes metrics
 * edit_data.py - edits given data for our purposes
 * visualisation.py - visualizes the video frames and creates the split-screen
 * file_work.py - loading data and writes our outputs
 
### Optional
 * random_files.py - prints two random climbers' performances from unpacked_data folder; it is possible that videa does not contain some performances and otherwise

## Parameters

 * two identification numbers of the arbitrary climbers' performances
 
### Optional
 * -s - split-screen switches to variant 2 - alignes videos by height
 * -t - prints time and length of trajectory per climber


## Output folders
 * outputs: split-screen video 
 * out_data: computed data visualized on split-screen: delay points, advantage and speed difference, and aligned indices of frames by height
 
## Rest of folders
 * images - contains split-screen frames 
 * original_videa - original videos of both climbers that competed against each other
 * data_folder - containts original unrolled skeleton poses