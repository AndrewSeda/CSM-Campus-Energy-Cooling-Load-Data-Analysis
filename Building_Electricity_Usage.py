#Buildings_Electricity_Usage.xlxs
    #Includes:
    #Data from 2016-2021 seperated by year measured in mega watts
    #Electricity usage of each building 
    #Electric cost of each building 
    #Total cost of each building 

from cmath import nan
from fileinput import close
import pandas as pd
import numpy
#import pdb

#File location: D:\Work\Research\Research Fall 2022\Modified\
FILE_PATH = "D:\Work\Research\Research Fall 2022\Modified\\"
OUTPUT_PATH = "D:\Work\Research\Research Fall 2022\Output_Data\\"

dfElecCost = pd.read_excel(FILE_PATH + "Buildings_Electricity_Usage.xlsx", sheet_name= "Electricity cost ($)", na_values="---" )
dfElecUsage = pd.read_excel(FILE_PATH + "Buildings_Electricity_Usage.xlsx", sheet_name= "Electricity usage (kWh)", na_values="---" )

header = [2021,2019,2018,2017,2016, "Average"]
#print(header)
buildings = []
ElecCost= []
ElecUsage = []
costPerUsage = []

dorms = {"Elm Hall", "Maple Hall", "Weaver Tower", "Randall Hall", "Stratton Hall", "Thomas Hall*", "Morgan Hall*", "Bradford Hall", "1600 Jackson", "Mines Park", "Aspen Hall" }#No longer Dorm Building

#print(dfElecCost["Year 2021"][0])
##Fills three arrays with cost/usage and cost per usage for each building seperated by year
for year in range(2021,2015,-1):
    year = str(year)
    costHolder = []
    usageHolder = []
    costPerHolder = []
    if year == "2020":
        continue
    for i in range(0,52):
        if year == "2021":
            ##Fill building array with all building names
            buildings.append(dfElecCost["Building"][i])
        costHolder.append(dfElecCost["Year " + year][i]) ##unnecessary?
        usageHolder.append(dfElecUsage["Year " + year][i]) ##unnecessary?
        costPerHolder.append(float(usageHolder[i])/float(costHolder[i]))
    ##Each array index filled with data for all buildings
    ElecCost.append(costHolder)
    ElecUsage.append(usageHolder)
    costPerUsage.append(costPerHolder)


buildings.append("Average")
df = pd.DataFrame((costPerUsage)).transpose()
s = (df.mean(axis=0))
df = df.append(s, ignore_index=True)
df2 = df.transpose()
df2 = df2.append(df.mean(axis=1), ignore_index=True)
df2.columns = [buildings]
df3 = df2.transpose()
df3.columns = [header]

dfnew = 1/ df3
dormArray = []
total = float(0)
#dfDorms = dfDorms.append(dormArra)
d = df3.loc['Randall Hall', 'Average']
#print(d)
#print(type(d))
#c = d.iloc[0,0]
#print(c)
#intArray = []
#print(df3)
count = float(0)
nameHeader = []
for name in dorms:
    #total += float((df3.loc['Randall Hall','Average']))
    d = df3.loc[name,"Average"]
    #print(d)
    if len(d) > 1:
        #print(name)
        #print(len(d))
        #print(d)
        for i in range(0,len(d)-1):
            c = d.iloc[i,0]
            if c == nan:
                c = 0
            dormArray.append(c)
            count += 1
            total += c
            nameHeader.append(name)
    else:
        c = d.iloc[0,0]
        if c == nan:
            c = 0
        dormArray.append(c)
        nameHeader.append(name)
        count += 1
        print(total)
        total += c
print(count, total)
avgDorms = total/count
dormArray.append(avgDorms)
nameHeader.append("Average")
#print(intArray)
dfDorms = pd.DataFrame(dormArray).transpose()
dfDorms.columns = (nameHeader)
dfDorms = dfDorms.transpose()
#print(dfDorms)
#print(dormArray)
#print(type(dormArray))
#for i in range(0,len(dormArray)):
 #   dormArray = [s.replace("Average", "") for s in dormArray[i]]

writer = pd.ExcelWriter(OUTPUT_PATH + 'costPerUsage.xlsx')
#print(dormArray)
df3.to_excel(writer, sheet_name = "kWh per Dollar")
dfnew.to_excel(writer, sheet_name ="Dollar per kWh")
dfDorms.to_excel(writer, sheet_name = "Dorm Average")
writer.save()
close()



