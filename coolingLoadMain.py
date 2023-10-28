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

energy_summer.write_data_to_excel()





#compareMonthRanges.main(df, year_selected, hour_tick, hour_tick_interval)
figure_number = 0




figure_number += 1
energy_summer.plot_energy_use_standard_winter(figure_number)

figure_number += 1
energy_Aug_to_Sept.plot_energy_use_standard_winter(figure_number)

figure_number += 1
energy_Aug_to_Sept.plot_energy_use(figure_number)

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










