
#import excel sheets

#Buildings_Electricity_Usage.xlxs
    #Includes:
    #Data from 2016-2021 seperated by year measured in mega watts
    #Electricity usage of each building 
    #Electric cost of each building 
    #Total cost of each building 

#Electrical_Power_Demand_2008-2019.xlsx
    #Includes:
    #Data from 2008-2019 measured in mega watts
    #Average electrical demand in 15 min intervals
    #Peak electrical demand in 15 min intervals
    #Annual peak demand and increase

#Electricity_and_PV_2019.xlsx
    #Includes:
    #Electricity data in 15min intervals measured in mega watts
    #PV data in 1 hour intervals seperated by wattage
    #PV data in 1 hour intervals for August with average and peak data

#EnergyDataLoop_Buildings.xlsx
    #Includes:
    #Electrical data in 15 min intervals measured in joules for:
        #Brown Hall
        #Elm Hall
        #Weaver Towers
        #Starzer Welcome Center
        #Maple Hall
        #Berthoud Hall
        #CoorsTek
    #Electical data in 15 min intervals measured in mega watts for 
    # all the buildings. Includes HVAC electrical use

from tabnanny import check
import pandas as pd

#File location: D:\Work\Research\Research Fall 2022\Modified\
FILE_PATH = "D:\Work\Research\Research Fall 2022\Modified\\"
#Read 1st sheet of excell file

df = pd.read_excel(FILE_PATH + "Buildings_Electricity_Usage.xlsx", sheet_name= 0)

##Divide data into months

#loc to index (Locate row/column)
#print(df["Annual Peak Demand (kW)"].mean())

#print(type(dataFrame1))
#print(dataFrame1)
