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

list_summer_energy_usage = create_season_energy(season_summer, df)
list_season_winter_standard_energy = create_season_energy(season_winter_standard, df) # Jan 1 - Mar 1 from 2008 to 2019
list_season_winter_standard_day_of_the_week_average_data = season_day_of_the_week_averages(list_season_winter_standard_energy[year_selected], False, year_selected)
list_season_winter_standard_day_of_the_week_seperated_interval_average_data = create_day_of_the_week_seperated_interval_average_data(list_season_winter_standard_day_of_the_week_average_data)
list_cooling_day_of_the_week_data, list_season_winter_standard_day_of_the_week_data, list_summer_day_of_the_week_data = create_cooling_energy(season_summer, df, list_season_winter_standard_day_of_the_week_seperated_interval_average_data)

season_Jun_to_July = Season([6,7,15,15], True, Year(year_selected + 2008))
season_Aug_to_Sept = Season([8,9,19,20], True, Year(year_selected + 2008))
season_Dec_to_Jan = Season([11,0,0,0], False, Year(year_selected + 2008))
energy_Jun_to_July = EnergyProfile.EnergyProfile(season_Jun_to_July, season_Dec_to_Jan, df)
energy_Aug_to_Sept = EnergyProfile.EnergyProfile(season_Aug_to_Sept, season_Dec_to_Jan, df)

'''
Compare Two Summer Seasons Energy Usage

Can be refactored into a method or deleted

# Need to convert. Year() does not work when average is selected for get_input_year

season_summer_Jun_to_July = Season([6,7,15,15], True, Year(year_selected + 2008))
season_summer_Aug_to_Sept = Season([8,9,19,20], True, Year(year_selected + 2008))
season_winter_Dec_to_Jan = Season([11,0,0,0], False, Year(year_selected + 2008)) # Creates a winter season from December 1st to January 1st

list_summer_energy_usage_Jun_to_July = create_season_energy(season_summer_Jun_to_July, df) # June 15 - July 15 from 2008 to 2019
list_summer_energy_usage_Aug_to_Sept = create_season_energy(season_summer_Aug_to_Sept, df) #Aug 19 - Sept 20 from 2008 to 2019
list_winter_energy_usage_Dec_to_Jan = create_season_energy(season_winter_Dec_to_Jan, df) # December 1 - Jan 1 from 2008 to 2019

# Simple and innaccurate method of generating a cooling load
list_cooling_energy_Jun_to_July = get_all_cooling(list_summer_energy_usage_Jun_to_July, list_winter_energy_usage_Dec_to_Jan)
list_cooling_energy_Aug_to_Sept = get_all_cooling(list_summer_energy_usage_Aug_to_Sept, list_winter_energy_usage_Dec_to_Jan)

winter_weekend_dataset_Dec_to_Jan = interval_average_dataset(list_winter_energy_usage_Dec_to_Jan, 14)
winter_weekday_dataset_Dec_to_Jan = interval_average_dataset(list_winter_energy_usage_Dec_to_Jan, 13)
list_summer_weekend_dataset_Jun_to_July_Aug_to_Sept = interval_average_dataset(list_summer_energy_usage_Aug_to_Sept, 14)
list_summer_weekday_dataset_Aug_to_Sept = interval_average_dataset(list_summer_energy_usage_Aug_to_Sept, 13)
list_cooling_weekend_dataset_Jun_to_July = interval_average_dataset(list_cooling_energy_Jun_to_July, 14)
list_cooling_weekday_dataset_Jun_to_July = interval_average_dataset(list_cooling_energy_Jun_to_July, 13)
list_cooling_weekend_dataset_Aug_to_Sept = interval_average_dataset(list_cooling_energy_Aug_to_Sept, 14)
list_cooling_weekday_dataset_Aug_to_Sept = interval_average_dataset(list_cooling_energy_Aug_to_Sept, 13)

list_summer_weekend_dataset_Jun_to_July = interval_average_dataset(list_summer_energy_usage_Jun_to_July, 14)

list_summer_interval_average_Jun_to_July, list_summer_weekday_average_Jun_to_July,list_summer_weekend_average_Jun_to_July = season_daily_averages(list_summer_energy_usage_Jun_to_July, year_selected)
list_summer_interval_average_Aug_to_Sept, list_summer_weekday_average_Aug_to_Sept,list_summer_weekend_average_Aug_to_Sept = season_daily_averages(list_summer_energy_usage_Aug_to_Sept, year_selected)

df_summer_weekend = pd.DataFrame(list_summer_weekend_dataset_Jun_to_July)
df_winter_weekend = pd.DataFrame(winter_weekend_dataset_Dec_to_Jan)

list_winter_interval_average_Dec_to_Jan, list_winter_weekday_average_Dec_to_Jan,list_winter_weekend_average_Dec_to_Jan = season_daily_averages(list_winter_energy_usage_Dec_to_Jan, year_selected)

list_compiled_energy__Jun_to_July = [list_summer_energy_usage_Jun_to_July[year_selected],list_winter_energy_usage_Dec_to_Jan[year_selected],list_cooling_energy_Jun_to_July[year_selected]]

list_cooling_interval_average_Jun_to_July = get_cooling_day(list_summer_interval_average_Jun_to_July, list_winter_interval_average_Dec_to_Jan)

list_weekend_cooling_data_Jun_to_July = get_cooling_day(list_summer_weekend_average_Jun_to_July, list_winter_weekend_average_Dec_to_Jan)
list_weekday_cooling_data_Jun_to_July = get_cooling_day(list_summer_weekday_average_Jun_to_July, list_winter_weekday_average_Dec_to_Jan)
##list_weekend_cooling_data_Jun_to_Julyset = interval_average_dataset(list_weekday_cooling_data_Jun_to_July, 14)
list_weekend_cooling_data_Aug_to_Sept = get_cooling_day(list_summer_weekend_average_Aug_to_Sept, list_winter_weekend_average_Dec_to_Jan)
list_weekday_cooling_data_Aug_to_Sept = get_cooling_day(list_summer_weekday_average_Aug_to_Sept, list_winter_weekday_average_Dec_to_Jan)


list_winter_day_of_the_week_average_data_Dec_to_Jan = season_day_of_the_week_averages(list_winter_energy_usage_Dec_to_Jan[11], False, year_selected)

# Generate a list containing the average energy use at each time of day (in 15 min intervals) for each day of the week
list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan = create_day_of_the_week_seperated_interval_average_data(list_winter_day_of_the_week_average_data_Dec_to_Jan)

list_cooling_day_of_the_week_data_Aug_to_Sept, list_winter_day_of_the_week_data_Aug_to_Sept, list_summer_day_of_the_week_data_Aug_to_Sept = create_cooling_energy(season_summer_Aug_to_Sept, df, list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan)
list_cooling_season_energy_typical_winter_intervals_Aug_to_Sept = create_cooling_data_by_interval(list_summer_energy_usage_Aug_to_Sept, 1, list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan)


list_cooling_season_energy_average_winter_day = []
for interval in range(0,len(list_summer_energy_usage_Aug_to_Sept[11])-1):    
        daily_interval= interval % len(list_winter_interval_average_Dec_to_Jan)
        list_cooling_season_energy_average_winter_day.append(list_summer_energy_usage_Aug_to_Sept[11][interval] - list_winter_interval_average_Dec_to_Jan[daily_interval])
'''

df_winter_day_seperated_data = pd.DataFrame(energy_Aug_to_Sept.winter_day_of_week_seperated_interval_average_data).transpose()
df_winter_day_seperated_data.columns = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]



df_interval_average_data = pd.DataFrame([energy_Jun_to_July.summer_interval_average_energy_usage, energy_Jun_to_July.winter_interval_average_energy_usage, energy_Jun_to_July.cooling_interval_average]).transpose()
df_week_interval_average_data = pd.DataFrame([energy_Jun_to_July.summer_weekend_average_energy_usage, energy_Jun_to_July.winter_weekend_average_energy_usage, energy_Jun_to_July.summer_weekday_average_energy_usage, energy_Jun_to_July.winter_weekday_average_energy_usage, energy_Jun_to_July.cooling_weekend_energy_usage, energy_Jun_to_July.cooling_weekday_energy_usage]).transpose()
df_week_interval_average_data_2 = pd.DataFrame([energy_Aug_to_Sept.summer_weekend_average_energy_usage, energy_Aug_to_Sept.winter_weekend_average_energy_usage, energy_Aug_to_Sept.summer_weekday_average_energy_usage, energy_Aug_to_Sept.winter_weekday_average_energy_usage, energy_Aug_to_Sept.cooling_weekend_energy_usage, energy_Aug_to_Sept.cooling_weekday_energy_usage]).transpose()

column_names = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "Average", "Weekday", "Weekend"]

df_compiled_data = pd.DataFrame(energy_Jun_to_July.compiled_energy).transpose()
df_compiled_data.columns = ["Summer", "Winter", "Cooling"]
df_winter_data = pd.DataFrame(energy_Jun_to_July.winter_energy_usage).transpose()
df_winter_data.columns = column_names
df_summer_data = pd.DataFrame(energy_Jun_to_July.summer_energy_usage).transpose()
df_summer_data.columns = column_names
df_cooling_data = pd.DataFrame(energy_Jun_to_July.cooling_energy_simple).transpose()
df_cooling_data.columns = column_names
df_week_interval_average_data.columns = ["Summer Weekend", "Winter Weekend", "Summer Weekday", "Winter Weekday", "Cooling Weekend", "Cooling Weekday"]
df_week_interval_average_data_2.columns = ["Summer Weekend", "Winter Weekend", "Summer Weekday", "Winter Weekday", "Cooling Weekend", "Cooling Weekday"]





# Writes all data to a new excel file
writer_new = pd.ExcelWriter(OUTPUT_PATH + 'coolingLoadNew.xlsx')
df.to_excel(writer_new, sheet_name= "All Data")
df_interval_average_data.to_excel(writer_new, sheet_name = "Interval Average Data")
df_week_interval_average_data.to_excel(writer_new, sheet_name = "Interval Average Week Data")
df_compiled_data.to_excel(writer_new, sheet_name = "Compiled Data")
df_winter_data.to_excel(writer_new, sheet_name = "Winter Data")
df_summer_data.to_excel(writer_new, sheet_name = "Summer Data")
df_cooling_data.to_excel(writer_new, sheet_name = "Cooling Data")
df_winter_day_seperated_data.to_excel(writer_new, sheet_name = "Winter Day Seperated Data")
writer_new.save()
close()





hour_tick_interval = []
hour_tick = []
b = 1
# Generates an hour count which corresponds to each time interval
for i in range(0,len(df_interval_average_data[2])):
    if(i%4 == 0):
        hour_tick_interval.append(i)
        hour_tick.append(b)
        b +=1

#compareMonthRanges.main(df, year_selected, hour_tick, hour_tick_interval)
figure_number = 0

plot_continuous_average_electricity_load(figure_number, df_interval_average_data)



figure_number+=3

combined_day_names_1 = []
for i in range(0,len(energy_Jun_to_July.summer_season.list_day_names)):
    combined_day_names_1.append(energy_Jun_to_July.summer_season.list_day_names[i] + ' | ' + energy_Jun_to_July.winter_season.list_day_names[i])

combined_day_names_2 = []
for i in range(0,len(energy_Aug_to_Sept.summer_season.list_day_names)):
    combined_day_names_2.append(energy_Aug_to_Sept.summer_season.list_day_names[i] + ' | ' + energy_Aug_to_Sept.winter_season.list_day_names[i])


plt.figure(figure_number)
plt.plot(list_summer_day_of_the_week_data[year_selected], color = "r")
plt.plot(list_season_winter_standard_day_of_the_week_data[year_selected], color = "b")
plt.plot(list_cooling_day_of_the_week_data[year_selected], color = "g")
plt.ylim(-1000,7000)
plt.ylabel("Energy Use (kWh)")
plt.xticks(season_summer.list_offset_day_intervals, season_summer.list_day_names, rotation=45)
plt.xlabel("Month")
plt.title("Summer, Winter, and Cooling Data (July-Aug) Using Average Winter Days - " + str(year_selected+2008))
plt.legend(["Summer", "Winter" , "Cooling"])

figure_number += 1
energy_Aug_to_Sept.plot_energy_use_standard_winter(figure_number)

figure_number += 1
energy_Aug_to_Sept.plot_energy_use(figure_number)

figure_number += 1
energy_Aug_to_Sept.plot_test(figure_number)

figure_number += 1
energy_Aug_to_Sept.plot_test_2(figure_number)

writer_senior_design_data = pd.ExcelWriter(OUTPUT_PATH + '2019_Summer_Cooling_Load.xlsx')
list_combined_day_of_the_week_data = [list_summer_day_of_the_week_data[year_selected],list_season_winter_standard_day_of_the_week_data[year_selected],list_cooling_day_of_the_week_data[year_selected]]
df_combined_day_of_the_week_data = pd.DataFrame(list_combined_day_of_the_week_data).transpose()
df_combined_day_of_the_week_data.columns = ["Summer", "Winter", "Cooling"]
df_combined_day_of_the_week_data.to_excel(writer_senior_design_data, sheet_name= "2019 Summer Cooling Load")

writer_senior_design_data.save()
close()

'''
figure_number+=1

plt.figure(figure_number)
plt.plot(list_summer_energy_usage_Jun_to_July[year_selected], color = 'r')
plt.plot(list_winter_energy_usage_Dec_to_Jan[year_selected], color = "b")
plt.plot(list_cooling_energy_Jun_to_July[year_selected], color = "g")
plt.ylim(-1000,7000)
plt.ylabel("Energy Use (kWh)")
plt.xticks(season_summer_Jun_to_July.list_offset_day_intervals, combined_day_names_1, rotation=45)
plt.xlabel("Month")
plt.title("Summer, Winter, and Cooling Data (July-Aug)")
plt.legend(["Summer", "Winter" , "Cooling"])

figure_number+=1

plt.figure(figure_number)
plt.plot(list_summer_energy_usage_Aug_to_Sept[year_selected], color = 'r')
plt.plot(list_winter_energy_usage_Dec_to_Jan[year_selected], color = "b")
plt.plot(list_cooling_energy_Aug_to_Sept[year_selected], color = "g")
plt.ylim(-1000,7000)
plt.ylabel("Energy Use (kWh)")
plt.xticks(season_summer_Aug_to_Sept.list_offset_day_intervals, combined_day_names_2, rotation=45)
plt.xlabel("Date (Summer / Winter)")
plt.title("Summer, Winter, and Cooling Data (Aug-Sept)")
plt.legend(["Summer", "Winter" , "Cooling"])

figure_number+=1

plt.figure(figure_number)
test = []
for i in range(5,6):
    for b in range(0,len(list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan[i])):
        test.append(list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan[i][b])
for i in range(0,5):
    for b in range(0,len(list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan[i])):
        test.append(list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan[i][b])
for i in range(0,len(test)):
    test.append(test[i])
plt.plot(list_summer_energy_usage_Aug_to_Sept[year_selected], color = 'r')
#plt.plot(list_winter_energy_usage_Dec_to_Jan[year_selected], color = "b")
plt.plot(test, color = "b")
plt.plot(list_cooling_season_energy_typical_winter_intervals_Aug_to_Sept, color = "g")
plt.ylabel("Energy Use (kWh)")
plt.ylim(-1000,7000)
plt.xticks(season_summer_Aug_to_Sept.list_offset_day_intervals, combined_day_names_2, rotation=45)
plt.xlabel("Date (Summer)")
plt.title("Cooling Data Using Day of the Week Winter Interval Data")
plt.legend(["Summer" ,"Winter", "Cooling"])

figure_number+=1

plt.figure(figure_number)

plt.plot(list_summer_energy_usage_Aug_to_Sept[year_selected], color = 'r')
#plt.plot(list_winter_energy_usage_Dec_to_Jan[year_selected], color = "b")
plt.plot(list_winter_energy_usage_Dec_to_Jan[year_selected], color = "b")
plt.plot(list_cooling_season_energy_average_winter_day, color = "g")
plt.ylabel("Energy Use (kWh)")
plt.ylim(-1000,7000)
plt.xticks(season_summer_Aug_to_Sept.list_offset_day_intervals, combined_day_names_2, rotation=45)
plt.xlabel("Date (Summer)")
plt.title("Cooling Data Using Average Winter Interval Data")
plt.legend(["Summer" ,"Winter", "Cooling"])

figure_number+=1

plt.figure(figure_number)

plt.plot(list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan[0], label = "Mon")
plt.plot(list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan[1], label = "Tues")
plt.plot(list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan[2], label = "Wed")
plt.plot(list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan[3], label = "Thur")
plt.plot(list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan[4], label = "Fri")
plt.plot(list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan[5], label = "Sat")
plt.plot(list_winter_day_of_week_seperated_interval_average_data_Dec_to_Jan[6], label = "Sun")
#plt.ylim(-3000,7000)
plt.ylabel("Energy Use (kWh)")
plt.xticks(hour_tick_interval, hour_tick, rotation=45)
plt.xlabel("Time of Day (Hour)")
plt.title("Winter Data Seperated by Day")
plt.legend()




figure_number+=1

#"""Violin Plots"""
#plt.figure(figure_number)
#plt.violinplot(df[0:12], showmeans=False, showextrema=True, showmedians=True, points = 10000000)
#plt.title('Entire Year Violin Plots')
#plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12],column_names[0:12])
#plt.ylabel("kWh")
#figure_number+=1

#plt.figure(figure_number)
#plt.violinplot( df, showmeans=True, showextrema=True, showmedians=True, points= 10)
#plt.title('Entire Year Violin Test Plot')
#plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12],column_names[0:12])
#plt.ylabel("kWh")
#figure_number+=1
#plt.figure(figure_number)
#plt.plot(list_summer_weekend_dataset_Jun_to_July[-1])
#plt.xticks(hour_tick_interval, hour_tick, rotation=45)
#plt.xlabel("Time of Day (Hour)")
#plt.title("Summer Standard Deviation")

#figureNumber+=1

average_winter_day_for_season = []
for i in range(0,30):
    for k in range(0,len(list_winter_interval_average_Dec_to_Jan)):
        average_winter_day_for_season.append(list_winter_interval_average_Dec_to_Jan[k])
    average_winter_day_for_season.append(list_winter_interval_average_Dec_to_Jan[-1])
plt.figure(figure_number)
plt.plot(average_winter_day_for_season, color = 'b')
plt.plot(list_cooling_season_energy_typical_winter_intervals_Aug_to_Sept, color = "g")
plt.plot(list_summer_energy_usage_Aug_to_Sept[year_selected], color = 'r')
plt.xticks(season_summer_Aug_to_Sept.list_offset_day_intervals, combined_day_names_2, rotation=45)
plt.xlabel("Time of Day (Hour)")
plt.legend(["Average Winter Day","Cooling","Summer"])
plt.title("Overlayed Graphs")


figure_number+=1

xCoords = []
for i in range(0,len(df_week_interval_average_data["Summer Weekend"])):
    xCoords.append(i)


plt.figure(figure_number)
plt.plot(df_week_interval_average_data["Summer Weekend"], label = "Summer weekend")
plt.plot(df_week_interval_average_data["Winter Weekend"], label = "Winter weekend")
plt.plot(df_week_interval_average_data["Summer Weekday"], label = "Summer weekday")
plt.plot(df_week_interval_average_data["Winter Weekday"], label = "Winter weekday")

plt.title("Average Energy Use Through the Day ")
plt.xticks(hour_tick_interval, hour_tick, rotation=45)
plt.ylim(2500,5500)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()

figure_number+=1

print(len(df_week_interval_average_data["Summer Weekend"]))
print(len(list_summer_weekend_dataset_Jun_to_July[-1]))
print(len(winter_weekend_dataset_Dec_to_Jan[-1]))

plt.figure(figure_number)
plt.plot(df_week_interval_average_data["Summer Weekend"], label = "Summer weekend", color = 'r')
plt.plot(df_week_interval_average_data["Winter Weekend"], label = "Winter weekend", color = 'b')
plt.plot(df_week_interval_average_data["Cooling Weekend"], label = "Cooling Weekend", color = 'g')
plt.fill_between(xCoords, df_week_interval_average_data["Summer Weekend"]-list_summer_weekend_dataset_Jun_to_July[-1],  df_week_interval_average_data["Summer Weekend"]+list_summer_weekend_dataset_Jun_to_July[-1], color='r', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data["Winter Weekend"]-winter_weekend_dataset_Dec_to_Jan[-1],  df_week_interval_average_data["Winter Weekend"]+winter_weekend_dataset_Dec_to_Jan[-1], color='b', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data["Cooling Weekend"]-list_cooling_weekend_dataset_Jun_to_July[-1],  df_week_interval_average_data["Cooling Weekend"]+list_cooling_weekend_dataset_Jun_to_July[-1], color='g', alpha=0.4)


plt.title("June 14th to Aug 14th Average Energy Use Through the Day on Weekends with Std Deviation")
plt.xticks(hour_tick_interval, hour_tick, rotation=45)
plt.ylim(-500,5500)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()

figure_number+=1



plt.figure(figure_number)
plt.plot(df_week_interval_average_data_2["Summer Weekend"], label = "Summer weekend", color = 'r')
plt.plot(df_week_interval_average_data_2["Winter Weekend"], label = "Winter weekend", color = 'b')
plt.plot(df_week_interval_average_data_2["Cooling Weekend"], label = "Cooling Weekend", color = 'g')
plt.fill_between(xCoords, df_week_interval_average_data_2["Summer Weekend"]-list_summer_weekend_dataset_Jun_to_July_Aug_to_Sept[-1],  df_week_interval_average_data_2["Summer Weekend"]+list_summer_weekend_dataset_Jun_to_July_Aug_to_Sept[-1], color='r', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data["Winter Weekend"]-winter_weekend_dataset_Dec_to_Jan[-1],  df_week_interval_average_data["Winter Weekend"]+winter_weekend_dataset_Dec_to_Jan[-1], color='b', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data_2["Cooling Weekend"]-list_cooling_weekend_dataset_Aug_to_Sept[-1],  df_week_interval_average_data_2["Cooling Weekend"]+list_cooling_weekend_dataset_Aug_to_Sept[-1], color='g', alpha=0.4)

plt.title("Aug 15th to Sept 15th Average Energy Use Through the Day on Weekends with Std Deviation")
plt.xticks(hour_tick_interval, hour_tick, rotation=45)
plt.ylim(-500,5500)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()

figure_number+=1

plt.figure(figure_number)
plt.plot(df_week_interval_average_data_2["Summer Weekday"], label = "Summer weekday", color = 'r')
plt.plot(df_week_interval_average_data["Winter Weekday"], label = "Winter weekday", color = 'b')
plt.plot(df_week_interval_average_data_2["Cooling Weekday"], label = "Cooling Weekday", color = 'g')
plt.fill_between(xCoords, df_week_interval_average_data_2["Summer Weekday"]-list_summer_weekday_dataset_Aug_to_Sept[-1],  df_week_interval_average_data_2["Summer Weekday"]+list_summer_weekday_dataset_Aug_to_Sept[-1], color='r', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data["Winter Weekday"]-winter_weekday_dataset_Dec_to_Jan[-1],  df_week_interval_average_data["Winter Weekday"]+winter_weekday_dataset_Dec_to_Jan[-1], color='b', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data_2["Cooling Weekday"]-list_cooling_weekday_dataset_Aug_to_Sept[-1],  df_week_interval_average_data_2["Cooling Weekday"]+list_cooling_weekday_dataset_Aug_to_Sept[-1], color='g', alpha=0.4)

plt.title("Aug to Oct Average Energy Use Through the Day on Weekdays with Std Deviation")
plt.xticks(hour_tick_interval, hour_tick, rotation=45)
plt.ylim(-500,5500)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()



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










