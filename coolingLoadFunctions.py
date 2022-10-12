from cmath import nan
from fileinput import close
from statistics import mean
from tkinter.tix import COLUMN
import pandas as pd
import numpy
import matplotlib.pyplot as plt

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
def daysInMonths(months):
    monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
    days = sum(monthDays[i] for i in months)
    return int(days)
def timeInterval(day, minuteInterval):
    multiplier = 24*60/minuteInterval
    startingInt = multiplier*day
    return int(startingInt)

def seasonTimes(Leap):
    #summer is June 1st to semptember 30
#Winter is december 1st to end of May
#Winter break is dec 15th - Jan 10
    monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
    if Leap == True:
        monthDays[1] = 29
    beforeSummer = [0,1,2,3,4]
    endSummer = [0,1,2,3,4,5,6,7,8]
    beforeWinter = [0,1,2,3,4,5,6,7,8,9,10]
    year = [0,1,2,3,4,5,6,7,8,9,10,11]
    winterMonths = [11,0,1,2]
    summerMonths = [5,6,7,8]
    beforeSpring = [0,1,2, 3]
    summerDay = daysInMonths(beforeSummer)
    summerStart = timeInterval(summerDay, 15)
    winterDay = daysInMonths(beforeWinter)
    winterStart = timeInterval(winterDay, 15)
    fallDay = daysInMonths(beforeSpring)
    winterEnd = timeInterval(fallDay-1, 15)
    summerSeason = daysInMonths(endSummer)
    summerEnd = timeInterval(summerSeason, 15)
    summerInt = [summerStart, summerEnd]
    winterInt = [winterStart, winterEnd]
    endYear = int(timeInterval(daysInMonths(year),15))
    breakStartDay = daysInMonths(beforeWinter) +15
    breakEndDay = 10
    breakStartInt = int(timeInterval(breakStartDay, 15))
    breakEndInt = int(timeInterval(breakEndDay, 15))
    winterBreak = [breakStartInt, breakEndInt]
    return summerInt, winterInt, endYear, winterBreak

def seasonAverages(seasonEnergy):
    averageRow = []
    for interval in range(0,len(seasonEnergy[1])-1):
        sumSeason =0
        for year in range(0,len(seasonEnergy)):
            sumSeason += seasonEnergy[year][interval]
        averageSeason = sumSeason/len(seasonEnergy)
        averageRow.append(averageSeason)
    seasonEnergy.append(averageRow)
    return seasonEnergy

def data_frame_to_excel_transpose(data, header, writer, sheetName):
    df = pd.DataFrame(data).transpose()
    df.columns = header
    df.to_excel(writer, sheet_name = sheetName)
    return df

def data_frame_to_excel(data, header, writer, sheetName):
    df = pd.DataFrame(data)
    df.columns = header
    df.to_excel(writer, sheet_name = sheetName)
    return df

def interval_average(seasonEnergy, intervalsPerDay, yearSelect):
    intervalAveragePerDay = []
    for k in range(0,intervalsPerDay-1):
        seasonDaySum = 0
        seasonDayAverage = 0
        for i in range(0,len(seasonEnergy[yearSelect])-intervalsPerDay,intervalsPerDay):
            seasonDaySum += seasonEnergy[yearSelect][k+i]
        seasonDayAverage = seasonDaySum/((len(seasonEnergy[yearSelect])-1)/intervalsPerDay)
        intervalAveragePerDay.append(seasonDayAverage)
    return intervalAveragePerDay

def get_input_year(energyData):
    print("Year Options:")
    validYear = False
    while(validYear == False):
        year = 2008
        for i in range(0,len(energyData)-1):
            print("[",i, "] : ", year)
            year += 1
        print("[",i+1, "] : Average")
        yearSelect = int(input("Select Year: "))
        if(yearSelect < len(energyData) and yearSelect > 0):
            validYear = True
        if(validYear == False):
            print("Invalid input")
    return yearSelect


def get_year_cooling(seasonOneEnergy, seasonTwoEnergy, yearSelect):
    coolingEnergy=[]
    if(len(seasonTwoEnergy[yearSelect]) > len(seasonOneEnergy[yearSelect])):
        print("Long Winter")
        for h in range(0,len(seasonOneEnergy[yearSelect])-1):
            coolingEnergy.append(seasonOneEnergy[yearSelect][h]-seasonTwoEnergy[yearSelect][h])
    else:
        print("Long Summer")
        for h in range(0,len(seasonTwoEnergy[yearSelect])-1):
            coolingEnergy.append(seasonOneEnergy[yearSelect][h]-seasonTwoEnergy[yearSelect][h])
    return coolingEnergy
def get_cooling_day(summerIntervalAverage, winterIntervalAverage):
    coolingIntervalAverage = []
    for i in range(0,len(summerIntervalAverage)):
        coolingIntervalAverage.append(summerIntervalAverage[i]-winterIntervalAverage[i])
    return coolingIntervalAverage

def min_max_average_column(yearData):
    lowest = min(yearData)
    highest = max(yearData)
    average = mean(yearData)
    return lowest, highest, average