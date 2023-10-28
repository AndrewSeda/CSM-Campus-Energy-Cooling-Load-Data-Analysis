from cmath import nan, nanj
from fileinput import close
from statistics import mean
from tkinter import Y
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid, simpson
from coolingLoadFunctions import*
from epwFiles import*
from graph import*
import os
import compareMonthRanges
from statistics import stdev
import EnergyProfile

#Include the below function if comparing weather
#process_epw_files()

#Return to main directory (No longer necessary)
#os.chdir("D:\Work\Research\Research Fall 2022")

# File path for the excel data files
FILE_PATH = "D:\Work\Research\Research Fall 2022\Modified\\"
OUTPUT_PATH = "D:\Work\Research\Research Fall 2022\Output_Data\\"

#Read excel file
df = pd.read_excel(FILE_PATH + "Electrical_Power_Demand_2008-2019.xlsx", sheet_name = "Avg Demand (kW) 15min Interval")

# Initializes cols to store all of the column names in df as a list
cols = df.columns

use_presets = get_use_presets()

if use_presets == False:
    # Ensures the user inputs valid responses
    bool_exclude_winter_break = get_winter_break()

    # Year to analyze data from
    year_selected = get_input_year()

    # Month and day to start/end the season at
    date_range = get_date_range()
else:
    bool_exclude_winter_break = False
    year_selected = 11
    date_range = [5,9,0,0]


'''
Analyze Data for the Desired Summer Season and a Standard Winter Season

'''

season_winter_standard = Season([0,2,0,0],False, Year(year_selected + 2008)) # Creates a standard for winter using Jan 1 - Mar 1
season_summer = Season(date_range, bool_exclude_winter_break, Year(year_selected + 2008)) # Creates a Summer Season based on preset or custom inputs
energy_summer = EnergyProfile.EnergyProfile(season_summer, season_winter_standard, df)

season_Jun_to_July = Season([6,7,15,15], True, Year(year_selected + 2008))
season_Aug_to_Sept = Season([8,9,19,20], True, Year(year_selected + 2008))
season_Dec_to_Jan = Season([11,0,0,0], False, Year(year_selected + 2008))
energy_Jun_to_July = EnergyProfile.EnergyProfile(season_Jun_to_July, season_Dec_to_Jan, df)
energy_Aug_to_Sept = EnergyProfile.EnergyProfile(season_Aug_to_Sept, season_Dec_to_Jan, df)

energy_summer.write_data_to_excel()


figure_number = 0




figure_number += 1
energy_summer.plot_energy_use_standard_winter(figure_number)

figure_number += 1
energy_Aug_to_Sept.plot_energy_use_standard_winter(figure_number)

figure_number += 1
energy_Aug_to_Sept.plot_energy_use(figure_number)

figure_number += 1
energy_summer.plot_winter_day_of_the_week_seperated_data(figure_number)

figure_number += 1
energy_summer.plot_overlayed(figure_number)

figure_number += 1
energy_summer.plot_average_energy_use_through_day(figure_number)

figure_number += 1
energy_summer.plot_std_dev_through_day_weekend(figure_number)

figure_number += 1
energy_summer.plot_std_dev_through_day_weekday(figure_number)

'''
figure_number+=1


plt.figure(figure_number)
plt.plot(df_week_interval_average_data["Summer Weekend"], label = "June 14 to August 14 weekend")
plt.plot(df_week_interval_average_data_2["Summer Weekend"], label = "August 15 to October 15 weekend")

plt.title("Summer Weekend Energy Use Comparison")
plt.xticks(hour_tick_interval, hour_tick, rotation=45)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()

figure_number+=1

'''

plt.show()










