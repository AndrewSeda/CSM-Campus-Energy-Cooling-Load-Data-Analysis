from cmath import nan
from fileinput import close
from pickle import TRUE
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
def days_to_month(months, monthDays):
    days = sum(monthDays[i] for i in range(0,months))
    return int(days)

def time_interval(day, minuteInterval):
    multiplier = 24*60/minuteInterval
    startingInt = multiplier*day
    return int(startingInt)

def intervals_to_start_month(month, monthDays):
    monthStartDay = days_to_month(month, monthDays)
    monthStartInterval = time_interval(monthStartDay,15)
    return monthStartInterval
#def interval_to_month():
#   monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
#    monthName = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "August", "September", "October", "November", "December"]
#    intervalMonth = []
###    daysToMonth = 0
#    for i in range(0, len(monthDays)):
#        monthToInterval = timeInterval(monthDays[i], 15)
#        intervalMonth.append(monthToInterval)
#        daysToMonth += monthDays[i]
#    return intervalMonth, monthName
def check_leap(i):
    monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
    if i%4 == 0:
        Leap = True
    else:
         Leap = False
    if Leap == TRUE:
        monthDays[1] = 29
    return monthDays



def season_range(seasonRange, monthDays):
    seasonStartInterval = intervals_to_start_month(seasonRange[0], monthDays)
    seasonEndInterval = intervals_to_start_month(seasonRange[1], monthDays)
    seasonIntervalRange = [seasonStartInterval, seasonEndInterval]
    return seasonIntervalRange

def break_range(breakStartDay, breakEndDay):
    breakStartInt = int(time_interval(breakStartDay, 15))
    breakEndInt = int(time_interval(breakEndDay, 15))
    breakRange = [breakStartInt, breakEndInt]
    return breakRange

def season_set( seasonRange, monthDays,monthNames):
    seasonSet = []
    monthIntervals = [0]
    j = 0
    if seasonRange[0] > seasonRange[1]:
        for i in range(seasonRange[0],12):
            seasonSet.append(monthNames[i])
            if j > 0:
                monthIntervals.append(int( time_interval(monthDays[i],15))+monthIntervals[j-1])
            j +=1
        for i in range(0,seasonRange[1]+1):
            seasonSet.append(monthNames[i])
            if j > 0:
                monthIntervals.append(int( time_interval(monthDays[i],15))+monthIntervals[j-1])
            j +=1
    else:
        for i in range(seasonRange[0],seasonRange[1]+1):
            seasonSet.append(monthNames[i])
            if j > 0:
                monthIntervals.append(int( time_interval(monthDays[i],15))+monthIntervals[j-1])
            j +=1
    return seasonSet, monthIntervals

#def seasonTimes(Leap):
    #summer is June 1st to semptember 30
#Winter is december 1st to end of May
#Winter break is dec 15th - Jan 10
 #   monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
 #   monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
 #   if Leap == True:
 #       monthDays[1] = 29
 #  endSummer = [0,1,2,3,4,5,6,7,8]
 #   beforeWinter = [0,1,2,3,4,5,6,7,8,9,10]
 #   year = [0,1,2,3,4,5,6,7,8,9,10,11]
 #   winterMonths = [11,0,1,2]
 #   summerMonths = [5,6,7,8]
 #   beforeSpring = [0,1,2, 3]
    #summerDay = daysInMonths(beforeSummer)
    #summerStart = timeInterval(summerDay, 15)
    #winterDay = daysInMonths(beforeWinter)
    #winterStart = timeInterval(winterDay, 15)
    #fallDay = daysInMonths(beforeSpring)
    #winterEnd = timeInterval(fallDay-1, 15)
    #summerSeason = daysInMonths(endSummer)
    #summerEnd = timeInterval(summerSeason, 15)
    #summerInt = [summerStart, summerEnd]
    #winterInt = [winterStart, winterEnd]
    #endYear = int(timeInterval(daysInMonths(year),15))
    #breakStartDay = daysInMonths(beforeWinter) +15
    #breakEndDay = 10
    #breakStartInt = int(timeInterval(breakStartDay, 15))
    #breakEndInt = int(timeInterval(breakEndDay, 15))
    #winterBreak = [breakStartInt, breakEndInt]
    #summerSet = []
    #winterSet = []
    #monthInterval = [0]
    #for i in range(0,len(summerMonths)):
    #    summerSet.append(monthName[summerMonths[i]])
    #    if(i > 0):
    #        monthInterval.append(int(timeInterval(30,15))+monthInterval[i-1])
    #for i in winterMonths:
    #    winterSet.append(monthName[i])
    #return summerInt, winterInt, endYear, winterBreak, winterSet, summerSet, monthInterval

# Generates daily averages across the length of seasonEnergy
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
    
    #Loops through all intervals for a 24hour period
    for k in range(0,intervalsPerDay-1):
        seasonDaySum = 0
        seasonDayAverage = 0
        nanCount = 0
        for i in range(0,len(seasonEnergy[yearSelect])-intervalsPerDay,intervalsPerDay):
            #if seasonEnergy[yearSelect][k+1] == nan:
            #    nanCount +=1
            #    continue
           # else:
            #    seasonDaySum += seasonEnergy[yearSelect][k+i]
            seasonDaySum += seasonEnergy[yearSelect][k+i]
        #seasonDayAverage = seasonDaySum/((len(seasonEnergy[yearSelect])-1-nanCount)/intervalsPerDay)
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