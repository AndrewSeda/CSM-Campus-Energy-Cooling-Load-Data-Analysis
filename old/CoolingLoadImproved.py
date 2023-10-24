from cmath import nan
from fileinput import close
from statistics import mean
import pandas as pd
import numpy
import matplotlib.pyplot as plt
from scipy.integrate import trapz, simps
from coolingLoadFunctions import*
#File location: D:\Work\Research\Research Fall 2022\Modified\
FILE_PATH = "D:\Work\Research\Research Fall 2022\Modified\\"

df = pd.read_excel(FILE_PATH + "Electrical_Power_Demand_2008-2019.xlsx", sheet_name = "Avg Demand (kW) 15min Interval")

cols = df.columns
#print(cols)
winterRange = [11,2]
summerRange = [5,8]
monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]

# Initializes a nested array for each year + avg 
summerEnergy = []
winterEnergy = []
intervalsPerDay = time_interval(1,15)

for i in range(0,len(cols)):
    #Checks if its a leap year and, if so, adds 1 day to February
    monthDays = check_leap(i)
    #Stores a value for the last interval in the year
    endYear = intervals_to_start_month(11, monthDays) + time_interval(31, 15)
    #Stores the first and last interval of each season
    summerIntervalRange = season_range(summerRange, monthDays)
    winterIntervalRange = season_range(winterRange, monthDays)
    #Finds the Set used to label each interval range 
    #Finds the months for each season
    winterSet, winterMonthIntervals = season_set(winterRange, monthDays, monthNames)
    summerSet, summerMonthIntervals = season_set(summerRange, monthDays, monthNames)

    #Find the interval range for winter break
    winterBreak = break_range(days_to_month(11, monthDays)+15,10)
    winterRow = []
    summerRow = []
    for j in range(winterIntervalRange[0],endYear):
        #if(j > winterBreak[0]):#Ignores Winter Break
        #    continue
        #else:
            winterRow.append(df.at[j,cols[i]])
    for n in range(0,winterIntervalRange[1]):
       # if(n < winterBreak[1]):#Ignores Winter Break
       #     continue
       # else:
            winterRow.append(df.at[n,cols[i]])
    for k in range(summerIntervalRange[0],summerIntervalRange[-1]):
        summerRow.append(df.at[k, cols[i]])
    summerEnergy.append(summerRow)
    winterEnergy.append(winterRow)
#print(summerEnergy[1])
print(winterIntervalRange, "\n", summerIntervalRange, "\n", endYear) 


summerEnergy = seasonAverages(summerEnergy)
winterEnergy = seasonAverages(winterEnergy)


#   Arranging data for DataFrame and to print to excel
avg= pd.Index(['Average'])
seasonHeader = pd.Index(['Summer Load', 'Winter Load', 'Cooling Load'])
finalColumns = cols.append(avg)
#print(finalColumns)

yearSelect = get_input_year(summerEnergy)


#Gets daily averages over a given time period (Currently by year)
summerIntervalAverage = interval_average(summerEnergy, intervalsPerDay, yearSelect)
winterIntervalAverage = interval_average(winterEnergy, intervalsPerDay, yearSelect)
coolingIntervalAverage = get_cooling_day(summerIntervalAverage, winterIntervalAverage)

#Get cooling energy averages 
coolingEnergy = get_year_cooling(summerEnergy, winterEnergy, yearSelect)
compiledEnergy = [summerEnergy[yearSelect],winterEnergy[yearSelect],coolingEnergy]

coolingInfo = min_max_average_column(coolingIntervalAverage)

combinedSet = []
#print(len(summerSet), len(winterSet))
for i in range(0,len(summerSet)):
    combinedSet.append(summerSet[i] + " / " + winterSet[i])

#Intitializes excel file and allows for writing to multiple sheets
writer = pd.ExcelWriter('coolingLoad.xlsx')

#Write all data to excel file on sepearte sheets
intervalAverageData = data_frame_to_excel_transpose([summerIntervalAverage, winterIntervalAverage, coolingIntervalAverage], seasonHeader, writer, "Average Energy per Day")
compiledData = data_frame_to_excel_transpose(compiledEnergy, seasonHeader, writer, "Compiled Data")
winterData = data_frame_to_excel_transpose(winterEnergy, finalColumns, writer, "Winter Energy")
summerData = data_frame_to_excel_transpose(summerEnergy, finalColumns, writer, "Summer Energy")
coolingData = data_frame_to_excel(coolingEnergy, pd.Index(["Cooling Load Average"]), writer, "Cooling Load")
writer.save()
close()
#Excel file writing completed and file is closed
print('{:18.16f}'.format(trapz(intervalAverageData[2], i in range(0,len(intervalAverageData[2])))))
print('{:18.16f}'.format(simps(intervalAverageData[2], i in range(0,len(intervalAverageData[2])))))
#print(coolingInfo)
#Plot data
compiledData.plot()

plt.xticks(winterMonthIntervals, combinedSet, rotation=45)
intervalAverageData.plot()
plt.show()




