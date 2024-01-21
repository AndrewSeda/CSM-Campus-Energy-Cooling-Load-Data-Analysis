# Campus Energy Cooling Load Data Analysis
## Overview: 
The Colorado School of Mines campus energy data is minimally informative. By performing data analysis, we hope to extract useful information
that can inform decisions regarding the state of campus energy use. 
## Methodology:
The current objective  is to obtain an accurate measure of the campus cooling load.
This was accomplished using a standard winter week created by averaging the data between January and the end of February. As there is little to no cooling during
this period, we can subtract the standard winter Monday from a Monday in the Summer to determine the cooling used on that day.

## Installation Details:
The project was developed in Python 3.9.13 with the conda package manager
### Libraries used:
1. pandas
2. matplotlib
3. tkinter
4. numpy
5. scipy

## How to Use:
1. Copy the repository onto your system
2. Update the file paths in coolingLoadFunctions.py, EnergyProfile.py, and coolingLoadMain.py
3. Run coolingLoadMain.py
4. Input 2 at the first prompt and hit enter
5. At this point, the code may take a couple of minutes to complete. You should see a count from 13 to 19 in the terminal as it processes the data files.
6. The graphs should appear in separate windows
7. Enter ctrl + c in the terminal to exit

## Contact Information
If you need a walkthrough of the project or have any issues/questions, please get in touch with me at abalmaseda@mines.edu or balmaseda.andrew@gmail.com if I do not respond.
