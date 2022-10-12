from cmath import nan
from fileinput import close
from statistics import mean
import pandas as pd
import numpy
import matplotlib.pyplot as plt
from coolingLoadFunctions import*
#File location: D:\Work\Research\Research Fall 2022\Modified\
FILE_PATH = "D:\Work\Research\Research Fall 2022\Modified\\"

df = pd.read_excel(FILE_PATH + "Electrical_Power_Demand_2008-2019.xlsx", sheet_name = "Avg Demand (kW) 15min Interval")

cols = df.columns
#print(cols)



# Initializes a nested array for each year + avg 
summerEnergy = []
winterEnergy = []
intervalsPerDay = timeInterval(1,15)
for i in range(0,len(cols)):
    if i%4 == 0:
        Leap = True
    else:
         Leap = False
    summerInt, winterInt, endYear, winterBreak = seasonTimes(Leap)
    winterRow = []
    summerRow = []
    for j in range(winterInt[0],endYear):
        if(j > winterBreak[0]):#Ignores Winter Break
            continue
        else:
            winterRow.append(df.at[j,cols[i]])
    for n in range(0,winterInt[1]-1):
        if(n < winterBreak[1]):#Ignores Winter Break
            continue
        else:
            winterRow.append(df.at[n,cols[i]])
    for k in range(summerInt[0],summerInt[-1]-1):
        summerRow.append(df.at[k, cols[i]])
    summerEnergy.append(summerRow)
    winterEnergy.append(winterRow)
#print(summerEnergy[1])


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

print(coolingInfo)
#Plot data
compiledData.plot()
intervalAverageData.plot()
plt.show()


