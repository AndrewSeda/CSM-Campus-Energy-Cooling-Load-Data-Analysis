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

#File location: D:\Work\Research\Research Fall 2022\Modified\
#Change file location to access epw files
os.chdir("D:\Work\Research\Research Fall 2022\Weather\epw Files")
df_epw_files = {}
bool_split_tab = False
# Used To initialize pandas to write the the same file
writer = pd.ExcelWriter('epwTesting.xlsx')
# Creates dataframes out of all of the weather files
# Writes dataframes to excel sheets
for i in range (13,20):
    print(i)
    file_name = "CO_BROOMFIELD-JEFFCO_724699_" + str(i) + ".epw"
    df_name = 'df20' + str(i) + 'EpwFile'
    if i == 14 or i== 18 or i==19:
        bool_split_tab = False
    else:
        bool_split_tab = False
    df_epw_files[df_name] = Create_df_weather(file_name, bool_split_tab)
    df_epw_files[df_name].to_excel(writer, sheet_name= '20' + str(i))
writer.save()
close()    
# Finishes writing files to excel sheet
# All of the weather files are viewable in an excel workbook named epwTesting.xlsx

#Return to main directory
os.chdir("D:\Work\Research\Research Fall 2022")
# File path for the excel data files
FILE_PATH = "D:\Work\Research\Research Fall 2022\Modified\\"
OUTPUT_PATH = "D:\Work\Research\Research Fall 2022\Output_Data\\"
#Read excel file
df = pd.read_excel(FILE_PATH + "Electrical_Power_Demand_2008-2019.xlsx", sheet_name = "Avg Demand (kW) 15min Interval")
# Initializes cols to store all of the column names in df as a list
cols = df.columns

# Ensures the user inputs valid responses
bool_exclude_winter_break = get_winter_break()

#Year to analyze data from
year_selected = get_input_year()

# Need to convert. Year() does not work when average is selected for get_input_year
summer_1 = Season(6,7,15,15, True, Year(year_selected + 2008))
winter = Season(11,0,0,0, False, Year(year_selected + 2008)) # Creates a winter season from December 1st to January 1st
winter_standard = Season(0,2,0,0,False, Year(year_selected + 2008)) # Creates a standard for winter using Jan 1 - Mar 1
summer_2 = Season(8,9,19,20, True, Year(year_selected + 2008))

summer_comparison = Season(5,9,0,0, True, Year(year_selected + 2008))

list_summer_range = [6,7] # From July to August
## Change to [[Month,Day],[Month,Day]]
summer_range_2 = [8,9] # From August to September
winter_range = [11,0] # From December to January


list_summer_energy = create_season_energy(summer_1, df) # July 15 - June 15 from 2008 to 2019
list_summer_energy_2 = create_season_energy(summer_2, df) #Aug 19 - Sept 20 from 2008 to 2019
list_summer_comparison = create_season_energy(summer_comparison, df)

list_winter_energy = create_season_energy(winter, df) # December 1 - Jan 1 from 2008 to 2019
list_winter_standard_energy = create_season_energy(winter_standard, df) # Jan 1 - Mar 1 from 2008 to 2019

list_summer_weekend_dataset = interval_average_dataset(list_summer_energy, 14)

# Simple and innaccurate method of generating a cooling load
list_cooling_energy = get_all_cooling(list_summer_energy, list_winter_energy)
list_cooling_energy_2 = get_all_cooling(list_summer_energy_2, list_winter_energy)

winter_weekend_dataset = interval_average_dataset(list_winter_energy, 14)
winter_weekday_dataset = interval_average_dataset(list_winter_energy, 13)
list_summer_weekend_dataset_2 = interval_average_dataset(list_summer_energy_2, 14)
list_summer_weekday_dataset_2 = interval_average_dataset(list_summer_energy_2, 13)
list_cooling_weekend_dataset = interval_average_dataset(list_cooling_energy, 14)
list_cooling_weekday_dataset = interval_average_dataset(list_cooling_energy, 13)
list_cooling_weekend_dataset_2 = interval_average_dataset(list_cooling_energy_2, 14)
list_cooling_weekday_dataset_2 = interval_average_dataset(list_cooling_energy_2, 13)

#list_summer_weekend_dataset.append(stdev(list_summer_weekend_dataset))
df_summer_weekend = pd.DataFrame(list_summer_weekend_dataset)
df_winter_weekend = pd.DataFrame(winter_weekend_dataset)

#summerStdDf = df_summer_weekend.groupby(self).agg([np.mean, np.std])
#winterStdDf = df_winter_weekend.groupby().agg([np.mean, np.std])

list_summer_interval_average, list_summer_weekday_average,list_summer_weekend_average = season_daily_averages(list_summer_energy, year_selected)
list_summer_interval_average_2, list_summer_weekday_average_2,list_summer_weekend_average_2 = season_daily_averages(list_summer_energy_2, year_selected)

list_winter_interval_average, list_winter_weekday_average,list_winter_weekend_average = season_daily_averages(list_winter_energy, year_selected)
#df_prices = df.groupby("type").agg([np.mean, np.std])


list_compiled_energy = [list_summer_energy[year_selected],list_winter_energy[year_selected],list_cooling_energy[year_selected]]

list_cooling_interval_average = get_cooling_day(list_summer_interval_average, list_winter_interval_average)

list_weekend_cooling_data = get_cooling_day(list_summer_weekend_average, list_winter_weekend_average)
list_weekday_cooling_data = get_cooling_day(list_summer_weekday_average, list_winter_weekday_average)
##list_weekend_cooling_dataset = interval_average_dataset(list_weekday_cooling_data, 14)
list_weekend_cooling_data_2 = get_cooling_day(list_summer_weekend_average_2, list_winter_weekend_average)
list_weekday_cooling_data_2 = get_cooling_day(list_summer_weekday_average_2, list_winter_weekday_average)


list_winter_day_of_the_week_average_data = season_day_of_the_week_averages(list_winter_energy[11], False, year_selected)
list_winter_standard_day_of_the_week_average_data = season_day_of_the_week_averages(list_winter_standard_energy[year_selected], False, year_selected)


# Generate a list containing the average energy use at each time of day (in 15 min intervals) for each day of the week
list_winter_day_of_week_seperated_interval_average_data = create_day_of_the_week_seperated_interval_average_data(list_winter_day_of_the_week_average_data)
list_winter_standard_day_of_the_week_seperated_interval_average_data = create_day_of_the_week_seperated_interval_average_data(list_winter_standard_day_of_the_week_average_data)


list_cooling_day_of_the_week_data, list_winter_standard_day_of_the_week_data, list_summer_day_of_the_week_data = create_cooling_energy(summer_comparison, df, list_winter_standard_day_of_the_week_seperated_interval_average_data)
list_cooling_day_of_the_week_data2, list_winter_day_of_the_week_data2, list_summer_day_of_the_week_data2 = create_cooling_energy(summer_2, df, list_winter_day_of_week_seperated_interval_average_data)

list_cooling_season_energy_typical_winter_intervals = create_cooling_data_by_interval(list_summer_energy_2, 1, list_winter_day_of_week_seperated_interval_average_data)

list_cooling_season_energy_average_winter_day = []
for interval in range(0,len(list_summer_energy_2[11])-1):    
        daily_interval= interval % len(list_winter_interval_average)
        list_cooling_season_energy_average_winter_day.append(list_summer_energy_2[11][interval] - list_winter_interval_average[daily_interval])

#print((list_cooling_season_energy_typical_winter_intervals))
#print(len(list_winter_day_of_the_week_data))
#print(len(list_winter_day_of_week_seperated_interval_average_data))

df_winter_day_seperated_data = pd.DataFrame(list_winter_day_of_week_seperated_interval_average_data).transpose()
df_winter_day_seperated_data.columns = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]



df_interval_average_data = pd.DataFrame([list_summer_interval_average, list_winter_interval_average, list_cooling_interval_average]).transpose()
df_week_interval_average_data = pd.DataFrame([list_summer_weekend_average, list_winter_weekend_average, list_summer_weekday_average, list_winter_weekday_average, list_weekend_cooling_data, list_weekday_cooling_data]).transpose()
df_week_interval_average_data_2 = pd.DataFrame([list_summer_weekend_average_2, list_winter_weekend_average, list_summer_weekday_average_2, list_winter_weekday_average, list_weekend_cooling_data_2, list_weekday_cooling_data_2]).transpose()

column_names = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "Average", "Weekday", "Weekend"]

df_compiled_data = pd.DataFrame(list_compiled_energy).transpose()
df_compiled_data.columns = ["Summer", "Winter", "Cooling"]
df_winter_data = pd.DataFrame(list_winter_energy).transpose()
df_winter_data.columns = column_names
df_summer_data = pd.DataFrame(list_summer_energy).transpose()
df_summer_data.columns = column_names
df_cooling_data = pd.DataFrame(list_cooling_energy).transpose()
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
for i in range(0,len(summer_1.list_day_names)):
    combined_day_names_1.append(summer_1.list_day_names[i] + ' | ' + winter.list_day_names[i])

combined_day_names_2 = []
for i in range(0,len(summer_1.list_day_names)):
    combined_day_names_2.append(summer_2.list_day_names[i] + ' | ' + winter.list_day_names[i])


plt.figure(figure_number)
plt.plot(list_summer_day_of_the_week_data[year_selected], color = "r")
plt.plot(list_winter_standard_day_of_the_week_data[year_selected], color = "b")
plt.plot(list_cooling_day_of_the_week_data[year_selected], color = "g")
plt.ylim(-1000,7000)
plt.ylabel("Energy Use (kWh)")
plt.xticks(summer_comparison.list_offset_day_intervals, summer_comparison.list_day_names, rotation=45)
plt.xlabel("Month")
plt.title("Summer, Winter, and Cooling Data (July-Aug) Using Average Winter Days - " + str(year_selected+2008))
plt.legend(["Summer", "Winter" , "Cooling"])

writer_senior_design_data = pd.ExcelWriter(OUTPUT_PATH + '2019_Summer_Cooling_Load.xlsx')
list_combined_day_of_the_week_data = [list_summer_day_of_the_week_data[year_selected],list_winter_standard_day_of_the_week_data[year_selected],list_cooling_day_of_the_week_data[year_selected]]
df_combined_day_of_the_week_data = pd.DataFrame(list_combined_day_of_the_week_data).transpose()
df_combined_day_of_the_week_data.columns = ["Summer", "Winter", "Cooling"]
df_combined_day_of_the_week_data.to_excel(writer_senior_design_data, sheet_name= "2019 Summer Cooling Load")

writer_senior_design_data.save()
close()


figure_number+=1

plt.figure(figure_number)
plt.plot(list_summer_energy[year_selected], color = 'r')
plt.plot(list_winter_energy[year_selected], color = "b")
plt.plot(list_cooling_energy[year_selected], color = "g")
plt.ylim(-1000,7000)
plt.ylabel("Energy Use (kWh)")
plt.xticks(summer_1.list_offset_day_intervals, combined_day_names_1, rotation=45)
plt.xlabel("Month")
plt.title("Summer, Winter, and Cooling Data (July-Aug)")
plt.legend(["Summer", "Winter" , "Cooling"])

figure_number+=1

plt.figure(figure_number)
plt.plot(list_summer_energy_2[year_selected], color = 'r')
plt.plot(list_winter_energy[year_selected], color = "b")
plt.plot(list_cooling_energy_2[year_selected], color = "g")
plt.ylim(-1000,7000)
plt.ylabel("Energy Use (kWh)")
plt.xticks(summer_2.list_offset_day_intervals, combined_day_names_2, rotation=45)
plt.xlabel("Date (Summer / Winter)")
plt.title("Summer, Winter, and Cooling Data (Aug-Sept)")
plt.legend(["Summer", "Winter" , "Cooling"])

figure_number+=1

plt.figure(figure_number)
test = []
for i in range(5,6):
    for b in range(0,len(list_winter_day_of_week_seperated_interval_average_data[i])):
        test.append(list_winter_day_of_week_seperated_interval_average_data[i][b])
for i in range(0,5):
    for b in range(0,len(list_winter_day_of_week_seperated_interval_average_data[i])):
        test.append(list_winter_day_of_week_seperated_interval_average_data[i][b])
for i in range(0,len(test)):
    test.append(test[i])
plt.plot(list_summer_energy_2[year_selected], color = 'r')
#plt.plot(list_winter_energy[year_selected], color = "b")
plt.plot(test, color = "b")
plt.plot(list_cooling_season_energy_typical_winter_intervals, color = "g")
plt.ylabel("Energy Use (kWh)")
plt.ylim(-1000,7000)
plt.xticks(summer_2.list_offset_day_intervals, combined_day_names_2, rotation=45)
plt.xlabel("Date (Summer)")
plt.title("Cooling Data Using Day of the Week Winter Interval Data")
plt.legend(["Summer" ,"Winter", "Cooling"])

figure_number+=1

plt.figure(figure_number)

plt.plot(list_summer_energy_2[year_selected], color = 'r')
#plt.plot(list_winter_energy[year_selected], color = "b")
plt.plot(list_winter_energy[year_selected], color = "b")
plt.plot(list_cooling_season_energy_average_winter_day, color = "g")
plt.ylabel("Energy Use (kWh)")
plt.ylim(-1000,7000)
plt.xticks(summer_2.list_offset_day_intervals, combined_day_names_2, rotation=45)
plt.xlabel("Date (Summer)")
plt.title("Cooling Data Using Average Winter Interval Data")
plt.legend(["Summer" ,"Winter", "Cooling"])

figure_number+=1

plt.figure(figure_number)

plt.plot(list_winter_day_of_week_seperated_interval_average_data[0], label = "Mon")
plt.plot(list_winter_day_of_week_seperated_interval_average_data[1], label = "Tues")
plt.plot(list_winter_day_of_week_seperated_interval_average_data[2], label = "Wed")
plt.plot(list_winter_day_of_week_seperated_interval_average_data[3], label = "Thur")
plt.plot(list_winter_day_of_week_seperated_interval_average_data[4], label = "Fri")
plt.plot(list_winter_day_of_week_seperated_interval_average_data[5], label = "Sat")
plt.plot(list_winter_day_of_week_seperated_interval_average_data[6], label = "Sun")
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
#plt.plot(list_summer_weekend_dataset[-1])
#plt.xticks(hour_tick_interval, hour_tick, rotation=45)
#plt.xlabel("Time of Day (Hour)")
#plt.title("Summer Standard Deviation")

#figureNumber+=1

average_winter_day_for_season = []
for i in range(0,30):
    for k in range(0,len(list_winter_interval_average)):
        average_winter_day_for_season.append(list_winter_interval_average[k])
    average_winter_day_for_season.append(list_winter_interval_average[-1])
plt.figure(figure_number)
plt.plot(average_winter_day_for_season, color = 'b')
plt.plot(list_cooling_season_energy_typical_winter_intervals, color = "g")
plt.plot(list_summer_energy_2[year_selected], color = 'r')
plt.xticks(summer_2.list_offset_day_intervals, combined_day_names_2, rotation=45)
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
print(len(list_summer_weekend_dataset[-1]))
print(len(winter_weekend_dataset[-1]))

plt.figure(figure_number)
plt.plot(df_week_interval_average_data["Summer Weekend"], label = "Summer weekend", color = 'r')
plt.plot(df_week_interval_average_data["Winter Weekend"], label = "Winter weekend", color = 'b')
plt.plot(df_week_interval_average_data["Cooling Weekend"], label = "Cooling Weekend", color = 'g')
plt.fill_between(xCoords, df_week_interval_average_data["Summer Weekend"]-list_summer_weekend_dataset[-1],  df_week_interval_average_data["Summer Weekend"]+list_summer_weekend_dataset[-1], color='r', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data["Winter Weekend"]-winter_weekend_dataset[-1],  df_week_interval_average_data["Winter Weekend"]+winter_weekend_dataset[-1], color='b', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data["Cooling Weekend"]-list_cooling_weekend_dataset[-1],  df_week_interval_average_data["Cooling Weekend"]+list_cooling_weekend_dataset[-1], color='g', alpha=0.4)


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
plt.fill_between(xCoords, df_week_interval_average_data_2["Summer Weekend"]-list_summer_weekend_dataset_2[-1],  df_week_interval_average_data_2["Summer Weekend"]+list_summer_weekend_dataset_2[-1], color='r', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data["Winter Weekend"]-winter_weekend_dataset[-1],  df_week_interval_average_data["Winter Weekend"]+winter_weekend_dataset[-1], color='b', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data_2["Cooling Weekend"]-list_cooling_weekend_dataset_2[-1],  df_week_interval_average_data_2["Cooling Weekend"]+list_cooling_weekend_dataset_2[-1], color='g', alpha=0.4)

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
plt.fill_between(xCoords, df_week_interval_average_data_2["Summer Weekday"]-list_summer_weekday_dataset_2[-1],  df_week_interval_average_data_2["Summer Weekday"]+list_summer_weekday_dataset_2[-1], color='r', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data["Winter Weekday"]-winter_weekday_dataset[-1],  df_week_interval_average_data["Winter Weekday"]+winter_weekday_dataset[-1], color='b', alpha=0.4)
plt.fill_between(xCoords, df_week_interval_average_data_2["Cooling Weekday"]-list_cooling_weekday_dataset_2[-1],  df_week_interval_average_data_2["Cooling Weekday"]+list_cooling_weekday_dataset_2[-1], color='g', alpha=0.4)

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







plt.show()










