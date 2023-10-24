from cmath import nan
from fileinput import close
import pandas as pd
import numpy
import matplotlib.pyplot as plt
#File location: D:\Work\Research\Research Fall 2022\Modified\
FILE_PATH = "D:\Work\Research\Research Fall 2022\Modified\\"

df = pd.read_excel(FILE_PATH + "Electrical_Power_Demand_2008-2019.xlsx", sheet_name = "Avg Demand (kW) 15min Interval")
#summer is June 1st to August 31
#Winter is december 1st to end of Feb
cols = df.columns
#print(cols)

#Days in each month:
    # Jan - 31
    # Feb - 28/29
    # March - 31
    # April - 30
    # May - 31
    # June - 30
    # July - 31
    # August - 31
    # September - 30
    # October - 31
    # November 30
    # December 31
#Returns the interval for the first day of summer assuming 15 min intervals
def seasonTimes(Leap):
    monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
    if Leap == True:
        monthDays[1] = 29
    beforeSummer = [0,1,2,3,4]
    summerMonths = [5,6,7]
    beforeWinter = {0,1,2,3,4,5,6,7,8,9,10,11}
    winterMonths = [12,0,1]
    beforeFall = {0,1,2}
    summerDay = sum(monthDays[i] for i in beforeSummer)
    summerStart = summerDay * 24 * 4
    winterDay = sum(monthDays[i] for i in beforeWinter)
    winterStart = winterDay * 24 * 4
    fallDay = sum(monthDays[i] for i in beforeFall)
    winterEnd = (fallDay - 1) * 24 *4
    summer = sum(monthDays[i] for i in summerMonths) * 24 * 4
    summerInt = [summerStart, summer+summerStart]
    winterInt = [winterStart, winterEnd]
    endYear = sum(monthDays[:]) * 4 * 24
    return summerInt, winterInt, endYear


    
# Initializes a nested array for each year + avg 
summerEnergy = []
winterEnergy = []
for i in range(0,len(cols)):
    if i%4 == 0:
        Leap = True
    else:
         Leap = False
    summerInt, winterInt, endYear = seasonTimes(Leap)
    winterRow = []
    summerRow = []
    for j in range(winterInt[0],endYear):
        winterRow.append(df.at[j,cols[i]])
    for n in range(0,winterInt[1]-1):
        winterRow.append(df.at[n,cols[i]])
    for k in range(summerInt[0],summerInt[-1]-1):
        summerRow.append(df.at[k, cols[i]])
    summerEnergy.append(summerRow)
    winterEnergy.append(winterRow)
#print(summerEnergy[1])
summerAverageRow = []
winterAverageRow = []

print(len(cols))
for interval in range(0, len(summerEnergy[0])-1):
    sumSummer = 0
    for col in range(0,len(cols)):
        sumSummer += summerEnergy[col][interval]
    averageSummer = sumSummer/len(cols)
    summerAverageRow.append(averageSummer)
summerEnergy.append(summerAverageRow)


for interval in range(0,len(winterEnergy[1])-1):
    sumWinter = 0
    for col in range(0,len(cols)):
        sumWinter += winterEnergy[col][interval]
    averageWinter = sumWinter/len(cols)
    winterAverageRow.append(averageWinter)
winterEnergy.append(winterAverageRow)


#   Arranging data for DataFrame and to print to excel
avg= pd.Index(['Average'])
compiledHeader = pd.Index(['Summer Load', 'Winter Load', 'Cooling Load'])
finalColumns = cols.append(avg)
#print(finalColumns)
coolingEnergy=[]
if(len(winterEnergy[0]) > len(summerEnergy[0])):
    print("Long Winter")
    for h in range(0,len(summerEnergy[0])):
        coolingEnergy.append(summerEnergy[-1][h]-winterEnergy[-1][h])
else:
    print("Long Summer")
    for h in range(0,len(winterEnergy[1])-1):
        coolingEnergy.append(summerEnergy[-1][h]-winterEnergy[-1][h])

compiledEnergy = [summerEnergy[-1],winterEnergy[-1],coolingEnergy]
compiledData = pd.DataFrame(compiledEnergy).transpose()
coolingData = pd.DataFrame(coolingEnergy)
winterData = pd.DataFrame(winterEnergy).transpose()
summerData = pd.DataFrame(summerEnergy).transpose()
compiledData.columns = compiledHeader
#coolingData.columns = finalColumns
summerData.columns = finalColumns
winterData.columns = finalColumns
#print(summerData)
writer = pd.ExcelWriter('coolingLoad.xlsx')
compiledData.to_excel(writer, sheet_name = "Compiled Data")
coolingData.to_excel(writer, sheet_name = "Cooling Load")
summerData.to_excel(writer, sheet_name = "Summer")
winterData.to_excel(writer, sheet_name = "Winter")
writer.save()
close()
compiledData.plot()
plt.show()

