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

#File location: D:\Work\Research\Research Fall 2022\Modified\
#Change file location to access epw files
os.chdir("D:\Work\Research\Research Fall 2022\Weather\epw Files")
d = dict()
dfEpwFiles = {}
splitTab = False
# Used To initialize pandas to write the the same file
writer = pd.ExcelWriter('epwTesting.xlsx')
# Creates dataframes out of all of the weather files
# Writes dataframes to excel sheets
for i in range (13,20):
    print(i)
    fileName = "CO_BROOMFIELD-JEFFCO_724699_" + str(i) + ".epw"
    dfName = 'df20' + str(i) + 'EpwFile'
    if i == 14 or i== 18 or i==19:
        splitTab = False
    else:
        splitTab = False
    dfEpwFiles[dfName] = Create_df_weather(fileName, splitTab)
    dfEpwFiles[dfName].to_excel(writer, sheet_name= '20' + str(i))
writer.save()
close()    
# Finishes writing files to excel sheet

#Return to main directory
os.chdir("D:\Work\Research\Research Fall 2022")
# File path for the excel data files
FILE_PATH = "D:\Work\Research\Research Fall 2022\Modified\\"
#Read excel file
df = pd.read_excel(FILE_PATH + "Electrical_Power_Demand_2008-2019.xlsx", sheet_name = "Avg Demand (kW) 15min Interval")
# Initializes cols to store all of the column names in df as a list
cols = df.columns
#rint(type(cols))
# Ensures the user inputs valid responses
validInput = False
while validInput == False:
    inputWinterBreak = str(input("Exclude Winter Break from Data Set? [Y] or [N]: "))
    if inputWinterBreak.upper() == "Y" or inputWinterBreak.upper() == "N":
        validInput = True
        if inputWinterBreak.upper() == "Y":
            excludeWinterBreak = True
            #summerRange[-1] = 7
        else:
            excludeWinterBreak = False
    else:
        print("Invalid input.")
#Year to analyze data from
yearSelect = get_input_year()
#Generates data for each range of months
# 1 Month, 2 month, 3 month, and 4 month ranges
for i in range(1,5):
    if i == 1:
        winterRange = [11,0]
        summerRange = [5,6]
        combinedSet1, compiledData1, intervalAverageData1, winterData1, summerData1, coolingData1, winterMonthIntervals1, weekIntervalAverageData1 = create_data_sets(summerRange, winterRange, df, yearSelect)
        continue
    elif i == 2:
        winterRange = [11,1]
        summerRange = [5,7]
        combinedSet2, compiledData2, intervalAverageData2, winterData2, summerData2, coolingData2, winterMonthIntervals2, weekIntervalAverageData2  = create_data_sets(summerRange, winterRange, df, yearSelect)
        continue
    elif i ==3 :
        winterRange = [11,2]
        summerRange = [5,8]
        combinedSet3, compiledData3, intervalAverageData3, winterData3, summerData3, coolingData3, winterMonthIntervals3, weekIntervalAverageData3 = create_data_sets(summerRange, winterRange, df, yearSelect)
        continue
    elif i == 4:
        winterRange = [11,3]
        summerRange = [5,9]
        combinedSet4, compiledData4, intervalAverageData4, winterData4, summerData4, coolingData4, winterMonthIntervals4, weekIntervalAverageData4 = create_data_sets(summerRange, winterRange, df, yearSelect)
        continue
# Writes all data to a new excel file
writerNew = pd.ExcelWriter('coolingLoadNew.xlsx')
intervalAverageData4.to_excel(writerNew, sheet_name = "Interval Average Data")
compiledData4.to_excel(writerNew, sheet_name = "Compiled Data")
winterData4.to_excel(writerNew, sheet_name = "Winter Data")
summerData4.to_excel(writerNew, sheet_name = "Summer Data")
coolingData4.to_excel(writerNew, sheet_name = "Cooling Data")
writerNew.save()
close()


hourTickInterval = []
hourTick = []
b = 1
# Generates an hour count which corresponds to each time interval
for i in range(0,len(intervalAverageData4[2])):
    if(i%4 == 0):
        hourTickInterval.append(i)
        hourTick.append(b)
        b +=1

# Plots the daily average electricity load in 15 minute increments for each season
plt.figure(1)
plt.plot(intervalAverageData4)
plt.xticks(hourTickInterval, hourTick, rotation=45)
plt.xlabel("Time of Day (Hour)")
plt.legend(["Summer", "Winter" , "Average"])
plt.title("Average Electricity Load Over a Day by Season")

#Plot hourly average cooling over 1, 2, 3, and 4 month ranges
#Plots are overlayed
plt.figure(2)
plt.plot(intervalAverageData1[2], label = "1 Month Average")
plt.plot(intervalAverageData2[2], label = "2 Month Average")
plt.plot(intervalAverageData3[2], label = "3 Month Average")
plt.plot(intervalAverageData4[2], label = "4 Month Average")

plt.xticks(hourTickInterval, hourTick, rotation=45)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.title("Cooling Data Average at Different Ranges (Starting in December/June)")
plt.legend()

#Plot hourly average winter over 1, 2, 3, and 4 month ranges
#Plots are overlayed
plt.figure(3)
plt.plot(intervalAverageData1[1], label = "1 Month Average")
plt.plot(intervalAverageData2[1], label = "2 Month Average")
plt.plot(intervalAverageData3[1], label = "3 Month Average")
plt.plot(intervalAverageData4[1], label = "4 Month Average")

plt.xticks(hourTickInterval, hourTick, rotation=45)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.title("Winter Data Average at Different Ranges (Starting in December)")
plt.legend()

plt.figure(4)
plt.plot(weekIntervalAverageData4[0], label = "Summer weekend")
plt.plot(weekIntervalAverageData4[1], label = "Winter weekend")
plt.plot(weekIntervalAverageData4[2], label = "Summer weekday")
plt.plot(weekIntervalAverageData4[3], label = "Winter weekday")

plt.title("Average Energy Use Through the Day")
plt.xticks(hourTickInterval, hourTick, rotation=45)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()

plt.figure(5)
plt.plot(weekIntervalAverageData4[0], label = "Summer weekend")
plt.plot(weekIntervalAverageData4[1], label = "Winter weekend")

plt.title("Average Energy Use Through the Day on Weekends")
plt.xticks(hourTickInterval, hourTick, rotation=45)
plt.xlabel("Time of Day (Hour)")
plt.ylabel("kWh")
plt.legend()

plt.figure(6)
#print(intervalAverageData4)
intervalsPerDay = number_of_intervals_to_day(1,15)  

winterNames = ["December", "January", "February", "March", "April"]
monthLength = 30*24*60/15
winterIntervals = [monthLength*0,monthLength*1, monthLength*2, monthLength*3, monthLength*4 ]

plt.plot(winterData4[yearSelect])
plt.title("Winter Data over 4 month span")
plt.xticks(winterIntervals, winterNames, rotation=45)

plt.figure(7)
#Plot Summer, winter, wooling, and radiation data over 4 month span
radiationSummerSeason = create_radiation_data(dfEpwFiles[dfName], summerRange)
radiationWinterSeason = create_radiation_data(dfEpwFiles[dfName], winterRange)
dfRadiationSummerSeason = pd.DataFrame(radiationSummerSeason)
dfRadiationWinterSeason = pd.DataFrame(radiationWinterSeason)
#print(type(compiledData4), " and ", type(dfRadiationSeason))
#newData = pd.concat([compiledData4[0], dfRadiationSummerSeason])
#plt.plot(dfRadiationSummerSeason, label = "Radiation")
#plt.plot(compiledData4[0], label = "Summer Electrical Load")
#plt.legend = ["Summer", "Winter" , "Average"]
#axNew = axTest.twinx()
#axNew.plot(radiationSeason, color = 'r')
figure7, ax7 = plt.subplots()
color = 'tab:blue'
ax7.set_xlabel('Month')
ax7.set_ylabel('kWh', color = color)
ax7.plot(dfRadiationSummerSeason, label = "Radiation", color = color)
ax7twin = ax7.twinx()
color = 'tab:red'

ax7twin.set_ylabel('W/m^2', color = color)
ax7twin.plot(compiledData4[0], label = "Summer Electrical Load", color=color)
plt.xticks(winterMonthIntervals4, combinedSet4, rotation=45)
plt.legend()
plt.title("Summer Electrical Load Relative to Solar Radiation")

#plt.figure(8)
figure8, ax8 = plt.subplots()
color = 'tab:blue'
ax8.set_xlabel('Month')
ax8.set_ylabel('kWh', color = color)
ax8.plot(dfRadiationWinterSeason, label = "Radiation", color = color)
ax8twin = ax8.twinx()
color = 'tab:red'

ax8twin.set_ylabel('W/m^2', color = color)
ax8twin.plot(compiledData4[1], label = "Winter Electrical Load", color=color)
#plt.plot(dfRadiationWinterSeason, label = "Radiation")
#plt.plot(compiledData4[1], label = "Winter Electrical Load")
plt.legend()
plt.title("Winter Electrical Load Relative to Solar Radiation")
plt.xticks(winterMonthIntervals4, combinedSet4, rotation=45)


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
holdArray = [intervalAverageData4[2],dfEpwFiles[dfName]['average_temperature'] , dfEpwFiles[dfName]['average_radiation']]
nameArray = ["Average Cooling Load", "Average Temperature", "Average Solar Radiation"]
yArray = ["kWh" , "Degrees Celcius" ,"W/m^2"]
yArrayTemp = ["Average Cooling Load (kWh)" , "Average Temperature (Celcius)" ,"Average Solar Radiation (W/m^2)"]
b = 0
for ax, color in zip(axes, colors):
    ax.plot(holdArray[b],  color=color, label = nameArray[b])
    ax.set_ylabel(yArrayTemp[b], color=color)
    ax.tick_params(axis='y', colors=color)
    b +=1

ax.set_xticks(hourTickInterval, hourTick, rotation = 45)
#fig.xticks(hourTickInterval, hourTick, rotation=45)
axes[0].set_xlabel('Time of Day (Hour)')

ax.set_title("2017 Average Cooling Load Compared to Temperaturand Solar Radiation")





plt.show()





#for i in range(1,4):
#    range = number_of_intervals_to_day(7*i, 15)
#    winterIntervalAverage = interval_average(winterData4, intervalsPerDay, yearSelect)
#    plt.plot(winterIntervalAverage)
#    winterData1.iloc[0:range].plot(y = yearSelect)
#plt.show()


#ax.legend(nameArray)
#plt.show()
#plt.plot(intervalAverageData4[0], label = "4 Month Average")
#ax2 = ax1.twinx()
#plt.plot(df2017['dew_point_temperature'], label = "Temperature", color = 'purple')
#ax3 = ax2.twinx()
#plt.plot(df2017['direct_normal_radiation'], label= "Solar Radiation", color = 'black')

#Intitializes excel file and allows for writing to multiple sheets

#Write all data to excel file on sepearte sheets
#intervalAverageData = data_frame_to_excel_transpose([summerIntervalAverage, winterIntervalAverage, coolingIntervalAverage], seasonHeader, writer, "Average Energy per Day")
#compiledData = data_frame_to_excel_transpose(compiledEnergy, seasonHeader, writer, "Compiled Data")
#winterData = data_frame_to_excel_transpose(winterEnergy, finalColumns, writer, "Winter Energy")
#summerData = data_frame_to_excel_transpose(summerEnergy, finalColumns, writer, "Summer Energy")
#coolingData = data_frame_to_excel(coolingEnergy, pd.Index(["Cooling Load Average"]), writer, "Cooling Load")
#writerNew.save()
#close()
#Excel file writing completed and file is closed
#print('{:18.16f}'.format(trapz(coolingIntervalAverage, i in range(0,len(coolingIntervalAverage)))))
#print('{:18.16f}'.format(simps(coolingIntervalAverage, i in range(0,len(coolingIntervalAverage)))))

#print(coolingInfo)
#Plot data










