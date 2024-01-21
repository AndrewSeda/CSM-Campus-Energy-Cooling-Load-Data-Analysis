from tkinter import Y
import pandas as pd
import matplotlib.pyplot as plt
from coolingLoadFunctions import*
from epwFiles import*
from graph import*
import EnergyProfile


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
    year_selected = 11 #Years since 2008
    date_range = [5,9,1,4]


'''
Analyze Data for the Desired Summer Season and a Standard Winter Season

'''

# Initialize 3 sets of intervals at locations of bad data
# Interval_8_11 is the interval corresponding to the first interval of August 11
y1 = Year(year_selected+2008)
interval_8_11 = number_of_intervals_to_day(number_of_days_to_month(7,y1.month_days)+10,15)
interval_8_31 = number_of_intervals_to_day(number_of_days_to_month(7,y1.month_days)+30,15)
interval_7_14 = number_of_intervals_to_day(number_of_days_to_month(6,y1.month_days)+15,15)
interval_8_3 = number_of_intervals_to_day(number_of_days_to_month(7,y1.month_days)+2,15)
interval_7_31 = number_of_intervals_to_day(number_of_days_to_month(6,y1.month_days)+30,15)
interval_9_18 = number_of_intervals_to_day(number_of_days_to_month(8,y1.month_days)+17,15)
interval_3_3 = number_of_intervals_to_day(number_of_days_to_month(2,y1.month_days)+2,15)
interval_3_13 = number_of_intervals_to_day(number_of_days_to_month(2,y1.month_days)+12,15)
interval_2_18 = number_of_intervals_to_day(number_of_days_to_month(1,y1.month_days)+17,15)

#print("Intervals to 8/11: " + str(interval_8_11)) # Monday
#print("Intervals to 8/30: " + str(interval_8_31)) # Tuesday

#print("Intervals to 7/14: " + str(interval_7_14)) # Monday
#print("Intervals to 7/22: " + str(interval_8_3)) # Tuesday

#print(str(df.at[ 0, '               ' + str(year_selected+2008)]))

# Fix data at given locations by setting data equal to the data from a week prior
for i in range(0,INTERVALS_PER_DAY):
    index1 = i + interval_7_31
    index2 = i + interval_7_31 - INTERVALS_PER_DAY*7
    df.at[index1, year_selected+2008] = df.at[index2, year_selected+2008]

for i in range(0,INTERVALS_PER_DAY):
    index1 = i + interval_9_18
    index2 = i + interval_9_18 - INTERVALS_PER_DAY*7
    df.at[index1, year_selected+2008] = df.at[index2, year_selected+2008]

for i in range(0,interval_8_31-interval_8_11):
    index1 = i + interval_8_11
    index2 = i + interval_7_14
    df.at[index1, year_selected+2008] = df.at[index2, year_selected+2008]

for i in range(0,interval_3_13-interval_3_3):
    index1 = i + interval_3_3
    index2 = i + interval_2_18
    df.at[index1, year_selected+2008] = df.at[index2, year_selected+2008]

season_winter_standard = Season([0,2,0,0],False, Year(year_selected + 2008)) # Creates a standard for winter using Jan 1 - Mar 1
season_summer = Season(date_range, bool_exclude_winter_break, Year(year_selected + 2008)) # Creates a Summer Season based on preset or custom inputs
energy_summer = EnergyProfile.EnergyProfile(season_summer, season_winter_standard, df)

season_whole_year = Season([0,11,0,30],True, Year(year_selected + 2008))
energy_whole_year = EnergyProfile.EnergyProfile(season_whole_year, season_winter_standard, df)


# Initialize Seasons to extract data over specific periods
season_Jun_to_July = Season([6,7,15,15], True, Year(year_selected + 2008))
season_Aug_to_Sept = Season([8,9,19,20], True, Year(year_selected + 2008))
season_Dec_to_Jan = Season([11,0,0,0], False, Year(year_selected + 2008))
energy_Jun_to_July = EnergyProfile.EnergyProfile(season_Jun_to_July, season_Dec_to_Jan, df)
energy_Aug_to_Sept = EnergyProfile.EnergyProfile(season_Aug_to_Sept, season_Dec_to_Jan, df)

energy_summer.write_data_to_excel()


figure_number = 0

'''Plots'''
figure_number += 1
energy_summer.plot_energy_use_standard_winter(figure_number)

figure_number += 1
energy_Aug_to_Sept.plot_energy_use_standard_winter(figure_number)

figure_number += 1
energy_Aug_to_Sept.plot_energy_use(figure_number)

figure_number += 1
energy_summer.plot_winter_day_of_the_week_seperated_data(figure_number)

figure_number += 1
energy_summer.plot_average_energy_use_through_day(figure_number)

figure_number += 1
energy_summer.plot_std_dev_through_day_weekend(figure_number)

figure_number += 1
energy_summer.plot_std_dev_through_day_weekday(figure_number)

figure_number += 1
energy_whole_year.plot_energy_use_standard_winter(figure_number)


#Need to run the first time
df_epw_files=process_epw_files()
df_name = 'df20' + str(year_selected+2) + 'EpwFile'

list_temperature_season = []
list_wet_temperature_season = []
start = energy_summer.summer_season.list_interval_range[0]
end = energy_summer.summer_season.list_interval_range[1]

for i in range(int(start/4),int(end/4)):
    for b in range(0,4):
        list_temperature_season.append(df_epw_files[df_name].at[i,'dry_bulb_temperature'])
    
#Plot cooling load, temperature, and radiation hourly data
fig, ax = plt.subplots()
# Twin the x-axis twice to make independent y-axes.
axes = [ax, ax.twinx()]
# Make some space on the right side for the extra y-axis.
fig.subplots_adjust(right=0.75)
# Move the last y-axis spine over to the right by 20% of the width of the axes
#axes[-1].spines['right'].set_position(('axes', 1.2))
# To make the border of the right-most axis visible, we need to turn the frame
# on. This hides the other plots, however, so we need to turn its fill off.
axes[-1].set_frame_on(True)
axes[-1].patch.set_visible(False)
# And finally we get to plot things...
colors = ('Green', 'Red')
holdArray = [energy_summer.summer_energy_usage[year_selected],list_temperature_season]
nameArray = ["Average Cooling Load", "Dry Temperature"]
yArray = ["kWh" , "Degrees Celcius"]
yArrayTemp = ["Average Cooling Load (kWh)" , "Dry Bulb Temperature (Celcius)"]
b = 0
for ax, color in zip(axes, colors):
    ax.plot(holdArray[b],  color=color, label = nameArray[b])
    ax.set_ylabel(yArrayTemp[b], color=color)
    ax.tick_params(axis='y', colors=color)
        
    b +=1

ax.set_xticks(energy_summer.summer_season.list_offset_day_intervals, energy_summer.summer_season.list_day_names, rotation = 45)
axes[0].set_xlabel('Time of Day (Hour)')

ax.set_title("2019 Average Cooling Load Compared to Dry Bulb Temperature")

plt.show()










