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
import os
import compareMonthRanges
from statistics import stdev

#File location: D:\Work\Research\Research Fall 2022\Modified\
#Change file location to access epw files
os.chdir("D:\Work\Research\Research Fall 2022\Weather\epw Files")
d = dict()
df_epw_files = {}
bool_split_tab = False
# Used To initialize pandas to write the the same file
writer = pd.ExcelWriter('epwTesting.xlsx')
# Creates dataframes out of all of the weather files
# Writes dataframes to excel sheets
for i in range (13,20):
    print(i)
    file_name = "CO_BROOMFIELD-JEFFCO_724699_" + str(i) + ".epw"
    df_name = 'df_raw_electricity_data20' + str(i) + 'EpwFile'
    if i == 14 or i== 18 or i==19:
        bool_split_tab = False
    else:
        bool_split_tab = False
    df_epw_files[df_name] = Create_df_weather(file_name, bool_split_tab)
    df_epw_files[df_name].to_excel(writer, sheet_name= '20' + str(i))
writer.save()
close()    
# Finishes writing files to excel sheet

#Return to main directory
os.chdir("D:\Work\Research\Research Fall 2022")
# File path for the excel data files
FILE_PATH = "D:\Work\Research\Research Fall 2022\Modified\\"
#Read excel file
df_raw_electricity_data = pd.read_excel(FILE_PATH + "Electrical_Power_Demand_2008-2019.xlsx", sheet_name = "Avg Demand (kW) 15min Interval")
# Initializes cols to store all of the column names in df_raw_electricity_data as a list
cols = df_raw_electricity_data.columns
#rint(type(cols))
# Ensures the user inputs valid responses
bool_valid_input = False
while bool_valid_input == False:
    input_winter_break = str(input("Exclude Winter Break from Data Set? [Y] or [N]: "))
    if input_winter_break.upper() == "Y" or input_winter_break.upper() == "N":
        bool_valid_input = True
        if input_winter_break.upper() == "Y":
            bool_exclude_winter_break = True
        else:
            bool_exclude_winter_break = False
    else:
        print("Invalid input.")
#Year to analyze data from
year_selected = get_input_year()
summer_range = [5,7]
summer_range_2 = [7,9]
winter_range = [11,1]

list_summer_energy = create_season_energy(summer_range, df_raw_electricity_data, True)
list_summer_energy_2 = create_season_energy(summer_range_2, df_raw_electricity_data, True)

list_winter_energy = create_season_energy(winter_range, df_raw_electricity_data, False)

list_summer_weekend_dataset = interval_average_dataset(list_summer_energy, 14)

list_winter_weekend_dataset = interval_average_dataset(list_winter_energy, 14)
list_winter_weekday_dataset = interval_average_dataset(list_winter_energy, 13)
list_summer_weekend_dataset_2 = interval_average_dataset(list_summer_energy_2, 14)
summer_weekday_dataset_2 = interval_average_dataset(list_summer_energy_2, 13)

#list_summer_weekend_dataset.append(stdev(list_summer_weekend_dataset))
df_summer_weekend = pd.DataFrame(list_summer_weekend_dataset)
df_winter_weekend = pd.DataFrame(list_winter_weekend_dataset)

#summerStdDf_raw_electricity_data = df_summer_weekend.groupby(self).agg([np.mean, np.std])
#winterStdDf_raw_electricity_data = df_winter_weekend.groupby().agg([np.mean, np.std])

summer_int_average, summer_weekday_average,summer_weekend_average = season_int_averages(list_summer_energy, year_selected)
summer_int_average_2, summer_weekday_average_2,summer_weekend_average_2 = season_int_averages(list_summer_energy_2, year_selected)

winter_int_average, winter_weekday_average,winter_weekend_average = season_int_averages(list_winter_energy, year_selected)
#df_raw_electricity_data_prices = df_raw_electricity_data.groupby("type").agg([np.mean, np.std])

list_cooling_energy = get_year_cooling(list_summer_energy, list_winter_energy, year_selected)
list_compiled_energy = [list_summer_energy[year_selected],list_winter_energy[year_selected],list_cooling_energy]

list_cooling_int_average = get_cooling_day(summer_int_average, winter_int_average)

df_int_average_data = pd.DataFrame([summer_int_average, winter_int_average, list_cooling_int_average]).transpose()
df_int_average_week_data = pd.DataFrame([summer_weekend_average, winter_weekend_average, summer_weekday_average, winter_weekday_average]).transpose()
df_int_average_week_data_2 = pd.DataFrame([summer_weekend_average_2, winter_weekend_average, summer_weekday_average_2, winter_weekday_average]).transpose()



df_compiled_data = pd.DataFrame(list_compiled_energy).transpose()
df_winter_data = pd.DataFrame(list_winter_energy).transpose()
df_summer_data = pd.DataFrame(list_summer_energy).transpose()
df_cooling_data = pd.DataFrame(list_cooling_energy)




year = Year(2018)
summer_month_and_int_set = month_name_and_interval_set(summer_range, year.list_month_days, year.list_month_names)
winter_month_and_int_set = month_name_and_interval_set(winter_range, year.list_month_days, year.list_month_names)
#print(summer_month_and_int_set)

combined_month_and_int_set = [[],[]]
for i in range(0,len(summer_month_and_int_set)+1):
    combined_month_and_int_set[0].append(summer_month_and_int_set[0][i] + " / " + winter_month_and_int_set[0][i]) 
combined_month_and_int_set[1] = summer_month_and_int_set[1]

#print(combined_month_and_int_set)

# Writes all data to a new excel file
writer_new = pd.ExcelWriter('coolingLoadNew.xlsx')
df_int_average_data.to_excel(writer_new, sheet_name = "Interval Average Data")
df_int_average_week_data.to_excel(writer_new, sheet_name = "Interval Average Week Data")
df_compiled_data.to_excel(writer_new, sheet_name = "Compiled Data")
df_winter_data.to_excel(writer_new, sheet_name = "Winter Data")
df_summer_data.to_excel(writer_new, sheet_name = "Summer Data")
df_cooling_data.to_excel(writer_new, sheet_name = "Cooling Data")
writer_new.save()
close()


hour_tick_int = []
hour_tick_val = []
b = 1
# Generates an hour count which corresponds to each time interval
for i in range(0,len(df_int_average_data[2])):
    if(i%4 == 0):
        hour_tick_int.append(i)
        hour_tick_val.append(b)
        b +=1

compareMonthRanges.main(df_raw_electricity_data, year_selected, hour_tick_val, hour_tick_int)
figure_number = 0

# Plots the daily average electricity load in 15 minute increments for each season
plt.figure(figure_number)
plt.plot(df_int_average_data)
plt.xticks(hour_tick_int, hour_tick_val, rotation=45)
plt.xlabel("Time of Day (Hour)")
plt.legend(["Summer", "Winter" , "Average"])
plt.title("Average Electricity Load Over a Day by Season")

figure_number+=3

#plt.figure(figure_number)
#plt.plot(list_summer_weekend_dataset[-1])
#plt.xticks(hour_tick_int, hour_tick_val, rotation=45)
#plt.xlabel("Time of Day (Hour)")
#plt.title("Summer Standard Deviation")

#igureNumber+=1

xCoords = []
for i in range(0,len(df_int_average_week_data[0])):
    xCoords.append(i)

plt.figure(figure_number)
plt.plot(df_int_average_week_data[0], label = "Summer weekend")
plt.plot(df_int_average_week_data[1], label = "Winter weekend")
plt.plot(df_int_average_week_data[2], label = "Summer weekday")
plt.plot(df_int_average_week_data[3], label = "Winter weekday")

plt.title("Average Energy Use Through the Day ")
plt.xticks(hour_tick_int, hour_tick_val, rotation=45)
plt.ylim(2500,5500)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()

figure_number+=1

plt.figure(figure_number)
plt.plot(df_int_average_week_data[0], label = "Summer weekend", color = 'r')
plt.plot(df_int_average_week_data[1], label = "Winter weekend", color = 'b')
plt.fill_between(xCoords, df_int_average_week_data[0]-list_summer_weekend_dataset[-1],  df_int_average_week_data[0]+list_summer_weekend_dataset[-1], color='r', alpha=0.4)
plt.fill_between(xCoords, df_int_average_week_data[1]-list_winter_weekend_dataset[-1],  df_int_average_week_data[1]+list_winter_weekend_dataset[-1], color='b', alpha=0.4)


plt.title("June to Aug Average Energy Use Through the Day on Weekends with Std Deviation")
plt.xticks(hour_tick_int, hour_tick_val, rotation=45)
plt.ylim(2500,5500)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()

figure_number+=1


plt.figure(figure_number)
plt.plot(df_int_average_week_data_2[0], label = "Summer weekend", color = 'r')
plt.plot(df_int_average_week_data[1], label = "Winter weekend", color = 'b')
plt.fill_between(xCoords, df_int_average_week_data_2[0]-list_summer_weekend_dataset_2[-1],  df_int_average_week_data_2[0]+list_summer_weekend_dataset_2[-1], color='r', alpha=0.4)
plt.fill_between(xCoords, df_int_average_week_data[1]-list_winter_weekend_dataset[-1],  df_int_average_week_data[1]+list_winter_weekend_dataset[-1], color='b', alpha=0.4)

plt.title("Aug to Oct Average Energy Use Through the Day on Weekends with Std Deviation")
plt.xticks(hour_tick_int, hour_tick_val, rotation=45)
plt.ylim(2500,5500)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()

figure_number+=1

plt.figure(figure_number)
plt.plot(df_int_average_week_data_2[2], label = "Summer weekday", color = 'r')
plt.plot(df_int_average_week_data[3], label = "Winter weekday", color = 'b')
plt.fill_between(xCoords, df_int_average_week_data_2[2]-summer_weekday_dataset_2[-1],  df_int_average_week_data_2[2]+summer_weekday_dataset_2[-1], color='r', alpha=0.4)
plt.fill_between(xCoords, df_int_average_week_data[3]-list_winter_weekday_dataset[-1],  df_int_average_week_data[3]+list_winter_weekday_dataset[-1], color='b', alpha=0.4)

plt.title("Aug to Oct Average Energy Use Through the Day on Weekdays with Std Deviation")
plt.xticks(hour_tick_int, hour_tick_val, rotation=45)
plt.ylim(2500,5500)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()



figure_number+=1

plt.figure(figure_number)
plt.plot(df_int_average_week_data[0], label = "June to August weekend")
plt.plot(df_int_average_week_data_2[0], label = "August to October weekend")

plt.title("Summer Weekend Energy Use Comparison")
plt.xticks(hour_tick_int, hour_tick_val, rotation=45)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()

figure_number+=1

plt.figure(figure_number)
#print(df_int_average_data)
intervalsPerDay = number_of_intervals_to_day(1,15)  

winterNames = ["December", "January", "February", "March", "April"]
monthLength = 30*24*60/15
winterIntervals = [monthLength*0,monthLength*1, monthLength*2, monthLength*3, monthLength*4 ]

plt.plot(df_winter_data[year_selected])
plt.title("Winter Data over 4 month span")
plt.xticks(winterIntervals, winterNames, rotation=45)

figure_number+=1

plt.figure(figure_number)
#Plot Summer, winter, wooling, and radiation data over 4 month span
list_radiation_summer_season = create_radiation_data(df_epw_files[df_name], summer_range)
list_radiation_winter_season = create_radiation_data(df_epw_files[df_name], winter_range)
df_radiation_summer_season = pd.DataFrame(list_radiation_summer_season)
df_radiation_winter_season = pd.DataFrame(list_radiation_winter_season)
#print(type(df_compiled_data), " and ", type(df_raw_electricity_dataRadiationSeason))
#newData = pd.concat([df_compiled_data[0], df_radiation_summer_season])
#plt.plot(df_radiation_summer_season, label = "Radiation")
#plt.plot(df_compiled_data[0], label = "Summer Electrical Load")
#plt.legend = ["Summer", "Winter" , "Average"]
#axNew = axTest.twinx()
#axNew.plot(radiationSeason, color = 'r')
figure7, ax7 = plt.subplots()
color = 'tab:blue'
ax7.set_xlabel('Month')
ax7.set_ylabel('kWh', color = color)
ax7.plot(df_radiation_summer_season, label = "Radiation", color = color)
ax7twin = ax7.twinx()
color = 'tab:red'

ax7twin.set_ylabel('W/m^2', color = color)
ax7twin.plot(df_compiled_data[0], label = "Summer Electrical Load", color=color)
plt.xticks(combined_month_and_int_set[1], combined_month_and_int_set[0], rotation=45)
plt.legend()
plt.title("Summer Electrical Load Relative to Solar Radiation")

#plt.figure(8)
figure8, ax8 = plt.subplots()
color = 'tab:blue'
ax8.set_xlabel('Month')
ax8.set_ylabel('kWh', color = color)
ax8.plot(df_radiation_winter_season, label = "Radiation", color = color)
ax8twin = ax8.twinx()
color = 'tab:red'

ax8twin.set_ylabel('W/m^2', color = color)
ax8twin.plot(df_compiled_data[1], label = "Winter Electrical Load", color=color)
#plt.plot(df_radiation_winter_season, label = "Radiation")
#plt.plot(df_compiled_data[1], label = "Winter Electrical Load")
plt.legend()
plt.title("Winter Electrical Load Relative to Solar Radiation")
plt.xticks(combined_month_and_int_set[1], combined_month_and_int_set[0], rotation=45)


#Plot cooling load, temperature, and radiation hourly data
fig, ax = plt.subplots()
# Twin the x-axis twice to make independent y-axes.
axes = [ax, ax.twinx(), ax.twinx()]
# Make some space on the right side for the extra y-axis.
fig.subplots_adjust(right=0.75)
# Move the last y-axis spine over to the right by 20% of the width of the axes
axes[-1].spines['right'].set_position(('axes', 1.2))
# To make the border of the right-most axis visible, we need to turn the frame
# on. This hides the other plots, however, so we need to turn its fill off.
axes[-1].set_frame_on(True)
axes[-1].patch.set_visible(False)
# And finally we get to plot things...
colors = ('Green', 'Red', 'Blue')
holdArray = [df_int_average_data[2],df_epw_files[df_name]['average_temperature'] , df_epw_files[df_name]['average_radiation']]
nameArray = ["Average Cooling Load", "Average Temperature", "Average Solar Radiation"]
yArray = ["kWh" , "Degrees Celcius" ,"W/m^2"]
yArrayTemp = ["Average Cooling Load (kWh)" , "Average Temperature (Celcius)" ,"Average Solar Radiation (W/m^2)"]
b = 0
for ax, color in zip(axes, colors):
    ax.plot(holdArray[b],  color=color, label = nameArray[b])
    ax.set_ylabel(yArrayTemp[b], color=color)
    ax.tick_params(axis='y', colors=color)
    b +=1

ax.set_xticks(hour_tick_int, hour_tick_val, rotation = 45)
#fig.xticks(hour_tick_int, hour_tick_val, rotation=45)
axes[0].set_xlabel('Time of Day (Hour)')

ax.set_title("2017 Average Cooling Load Compared to Temperaturand Solar Radiation")

plt.show()










