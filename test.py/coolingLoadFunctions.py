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
#Parameters:
#Month

class Year:
    monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    monthDays = []
    endOfYear = 0
    def __init__(self) -> None:
        pass
    def __init__(self, year):
        if (year%4 == 0):
            self.monthDays = [31,29,31,30,31,30,31,31,30,31,30,31]
        else:
            self.monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
        #Stores a value for the last interval in the year
        self.endOfYear = number_of_intervals_to_start_of_month(11, self.monthDays) + number_of_intervals_to_day(31, 15)
        return
        
        
    
def number_of_days_to_month(months: list, monthDays: list):
    """Returns the number of days before the specified month

    Args:
        months (int): The number of months before the target month (Ex: 3 for April)
        monthDays (int list): A list containing the number of days in each month

    Returns:
        int: Total number of days before specified month
    """
    
    
    days = sum(monthDays[i] for i in range(0,months))
    return int(days)

def number_of_intervals_to_day(day: int, minuteInterval: list):
    """Calculates the interval index corresponding to the desired day

    Args:
        day (int): The day to  convert to an interval
        minuteInterval (int): The number of minutes per interval

    Returns:
        int: The interval index for the input day
    """
    multiplier = 24*60/minuteInterval
    startingInt = multiplier*day
    return int(startingInt)

def number_of_intervals_to_start_of_month(month: int, monthDays: list):
    """Finds the number of days to the start of a month

    Args:
        month (int): The month to find the number of intervals before
        monthDays (int list): The number of days in each month

    Returns:
       Int: The interval index corresponding to the first day in the month
    """
    monthStartDay = number_of_days_to_month(month, monthDays)
    monthStartInterval = number_of_intervals_to_day(monthStartDay,15)
    return monthStartInterval

def check_leap(year: int):
    """Checks whether the current year is a leap year and adjusts the days per month accordingly

    Args:
        year (int): The year to check leap for

    Returns:
        int list: The number of days in each month
    """    
    monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
    if year%4 == 0:
        Leap = True
    else:
         Leap = False
    if Leap == TRUE:
        monthDays[1] = 29
    return monthDays



def season_interval_range(seasonRange: list, monthDays: list):
    """Generates a list containing the first and last interval index for a range of months

    Args:
        seasonRange (int list): Contains the first and last month to find an interval range for
        monthDays (int list): the number of days in a month

    Returns:
        int list: The first and last interval index for a range of months
    """    
    seasonStartInterval = number_of_intervals_to_start_of_month(seasonRange[0], monthDays)
    seasonEndInterval = number_of_intervals_to_start_of_month(seasonRange[1], monthDays)
    seasonIntervalRange = [seasonStartInterval, seasonEndInterval]
    return seasonIntervalRange

def break_range(breakStartDay: int, breakEndDay: int):
    """Generates an interval range for the days to exclude from the data

    Args:
        breakStartDay (int): The first day to be excluded
        breakEndDay (int): The last day to be exluded

    Returns:
        int list: Contains the first and last interval index for the specified break
    """    
    breakStartInt = int(number_of_intervals_to_day(breakStartDay, 15))
    breakEndInt = int(number_of_intervals_to_day(breakEndDay, 15))
    breakRange = [breakStartInt, breakEndInt]
    return breakRange

def season_set( seasonRange: list, monthDays: list,monthNames: list):
    """_summary_

    Args:
        seasonRange (int list): _description_
        monthDays (int list): _description_
        monthNames (int list): _description_

    Returns:
        _type_: _description_
    """    
    seasonSet = []
    monthIntervals = [0]
    j = 0
    if seasonRange[0] > seasonRange[1]:
        for i in range(seasonRange[0],12):
            seasonSet.append(monthNames[i])
            if j > 0:
                monthIntervals.append(int( number_of_intervals_to_day(monthDays[i],15))+monthIntervals[j-1])
            j +=1
        for i in range(0,seasonRange[1]+1):
            seasonSet.append(monthNames[i])
            if j > 0:
                monthIntervals.append(int( number_of_intervals_to_day(monthDays[i],15))+monthIntervals[j-1])
            j +=1
    else:
        for i in range(seasonRange[0],seasonRange[1]+1):
            seasonSet.append(monthNames[i])
            if j > 0:
                monthIntervals.append(int( number_of_intervals_to_day(monthDays[i],15))+monthIntervals[j-1])
            j +=1
    return seasonSet, monthIntervals

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

# Generates daily averages across the length of seasonEnergy
def seasonWeekdayAverages(seasonEnergy, boolSummer):
    averageWeekdayRow = []
    averageWeekendRow = []
    seasonWeekdayEnergy = []
    seasonWeekendEnergy = []

    weekdayIntervalTracker = 0
    # This  loops through each interval in a day
    # The nested loop causes each interval in a day to be averaged for every 
    # occurance of that interval before continuing to the next interval
    for interval in range(0,len(seasonEnergy[1])-1):
        sumWeekdaySeason =0
        sumWeekendSeason = 0
        weekdayCount = 0
        weekendCount = 0
        
        for year in range(0,len(seasonEnergy)):
            if year == 0:
                if boolSummer == True:
                    weekdayIntervalTracker = 0
                else:
                    weekdayIntervalTracker = 96
            elif year == 1:
                if boolSummer == True:
                    weekdayIntervalTracker = 96
                else:
                    weekdayIntervalTracker = 96*2
            elif year == 2:
                if boolSummer == True:
                    weekdayIntervalTracker = 96*2
                else:
                    weekdayIntervalTracker = 96*3
            elif year == 3:
                if boolSummer == True:
                    weekdayIntervalTracker = 96*3
                else:
                    weekdayIntervalTracker = 96*4
            elif year == 4:
                if boolSummer == True:
                    weekdayIntervalTracker = 96*5
                else:
                    weekdayIntervalTracker = 96*6
            elif year == 5:
                if boolSummer == True:
                    weekdayIntervalTracker = 96*6
                else:
                    weekdayIntervalTracker = 0
            elif year == 6:
                if boolSummer == True:
                    weekdayIntervalTracker = 0
                else:
                    weekdayIntervalTracker = 96
            elif year == 7:
                if boolSummer == True:
                    weekdayIntervalTracker = 96
                else:
                    weekdayIntervalTracker = 96*2
            elif year == 8:
                if boolSummer == True:
                    weekdayIntervalTracker = 96*3
                else:
                    weekdayIntervalTracker = 96*4
            elif year == 9:
                if boolSummer == True:
                    weekdayIntervalTracker = 96*4
                else:
                    weekdayIntervalTracker = 96*5
            elif year == 10:
                if boolSummer == True:
                    weekdayIntervalTracker = 96*5
                else:
                    weekdayIntervalTracker = 96*6
            elif year == 11:
                if boolSummer == True:
                    weekdayIntervalTracker = 96*6
                else:
                    weekdayIntervalTracker = 0      
            weekdayIntervalTracker += interval
            weekdayIntervalTracker = weekdayIntervalTracker % (96*7)
            if weekdayIntervalTracker < 96 or weekdayIntervalTracker >= (96*6):
                sumWeekendSeason += seasonEnergy[year][interval]
                weekendCount +=1
            else:
                sumWeekdaySeason += seasonEnergy[year][interval]
                weekdayCount +=1
        averageWeekendSeason = 0
        averageWeekdaySeason = 0
        #if weekdayIntervalTracker < 96 or weekdayIntervalTracker > (96*6):
        averageWeekendSeason = sumWeekendSeason/weekendCount
        #else:
        averageWeekdaySeason = sumWeekdaySeason/weekdayCount
        #averageSeason = sumSeason/len(seasonEnergy)
        averageWeekdayRow.append(averageWeekdaySeason)
        averageWeekendRow.append(averageWeekendSeason)
    seasonEnergy.append(averageWeekdayRow)
    seasonEnergy.append(averageWeekendRow)

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

def get_input_year():
    print("Year Options:")
    validYear = False
    while(validYear == False):
        year = 2008
        for i in range(0,12):
            print("[",i, "] : ", year)
            year += 1
        print("[",i+1, "] : Average")
        yearSelect = int(input("Select Year: "))
        if(yearSelect < 13 and yearSelect > 0):
            validYear = True
        else:
            print("Invalid input")
    return yearSelect


def get_year_cooling(seasonOneEnergy, seasonTwoEnergy, yearSelect):
    coolingEnergy=[]
    if(len(seasonTwoEnergy[yearSelect]) > len(seasonOneEnergy[yearSelect])):
        #print("Long Winter")
        for h in range(0,len(seasonOneEnergy[yearSelect])-1):
            coolingEnergy.append(seasonOneEnergy[yearSelect][h]-seasonTwoEnergy[yearSelect][h])
    else:
        #print("Long Summer")
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


def create_season_energy(seasonMonthRange: list,  df, boolSummer):
        
    # Initializes a nested array for each year + avg 
    
    #monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    #monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
    seasonEnergy = []
    yearNum = 2008
    cols = df.columns
    for i in range(0,len(cols)):
        #Checks if its a leap year and, if so, adds 1 day to February
        year = Year(yearNum)
        yearNum +=1
        #monthDays = check_leap(i)
        
        #Stores the first and last interval of each season
        seasonIntervalRange = season_interval_range(seasonMonthRange, year.monthDays)
        
        #Find the interval range for winter break (Dec 15 to Jan 10)
        breakRange = break_range(number_of_days_to_month(11, year.monthDays)+15,10)

        seasonRow = season_energy(seasonIntervalRange, year.endOfYear,breakRange, df, i)

        seasonEnergy.append(seasonRow)


    seasonEnergy = seasonAverages(seasonEnergy)
    seasonEnergy = seasonWeekdayAverages(seasonEnergy, boolSummer)
    return seasonEnergy

def create_data_sets(summerMonthRange, winterMonthRange, df, yearSelect):
    cols = df.columns
    summerEnergy = create_season_energy(summerMonthRange, df, True)
    winterEnergy = create_season_energy(winterMonthRange, df, False)

    #Finds the Set used to label each interval range 
    #Finds the months for each season
    year = Year(2018)
    summerSet, summerMonthIntervals = season_set(summerMonthRange, year.monthDays, year.monthNames)
    winterSet, winterMonthIntervals = season_set(winterMonthRange, year.monthDays, year.monthNames)


    #   Arranging data for DataFrame and to print to excel
    avg= pd.Index(['Average'])
    seasonHeader = pd.Index(['Summer Load', 'Winter Load', 'Cooling Load'])
    finalColumns = cols.append(avg)

    
    #Gets daily averages over a given time period (Currently by year)
    intervalsPerDay = number_of_intervals_to_day(1,15)  
    summerIntervalAverage = interval_average(summerEnergy, intervalsPerDay, yearSelect)
    winterIntervalAverage = interval_average(winterEnergy, intervalsPerDay, yearSelect)
    coolingIntervalAverage = get_cooling_day(summerIntervalAverage, winterIntervalAverage)
    summerWeekdayIntervalAverage = interval_average(summerEnergy, intervalsPerDay, 13)
    summerWeekendIntervalAverage = interval_average(summerEnergy, intervalsPerDay, 14)
    winterWeekdayIntervalAverage = interval_average(winterEnergy, intervalsPerDay, 13)
    winterWeekendIntervalAverage = interval_average(winterEnergy, intervalsPerDay, 14)

    #Get cooling energy averages 
    coolingEnergy = get_year_cooling(summerEnergy, winterEnergy, yearSelect)
    compiledEnergy = [summerEnergy[yearSelect],winterEnergy[yearSelect],coolingEnergy]

    coolingInfo = min_max_average_column(coolingIntervalAverage)

    combinedSet = []
    for i in range(0,len(summerSet)):
        combinedSet.append(summerSet[i] + " / " + winterSet[i]) 
    chosenYear = 2008 +yearSelect
    if(chosenYear == 2020):
        chosenYear = "Average"
    print(chosenYear, " Energy Data: ")
    print("Area Under Energy use curve: ", simpson(coolingIntervalAverage))
    print(trapezoid(coolingIntervalAverage))
    print("Peak Cooling Load: ", max(coolingIntervalAverage), "kWh")
    print("Average Cooling Load: ", mean(coolingIntervalAverage), "kWh \n")
    intervalAverageData = pd.DataFrame([summerIntervalAverage, winterIntervalAverage, coolingIntervalAverage]).transpose()
    weekIntervalAverageData = pd.DataFrame([summerWeekendIntervalAverage, winterWeekendIntervalAverage, summerWeekdayIntervalAverage, winterWeekdayIntervalAverage]).transpose()

    compiledData = pd.DataFrame(compiledEnergy).transpose()
    winterData = pd.DataFrame(winterEnergy).transpose()
    summerData = pd.DataFrame(summerEnergy).transpose()
    coolingData = pd.DataFrame(coolingEnergy)


    return combinedSet, compiledData, intervalAverageData, winterData, summerData, coolingData, winterMonthIntervals, weekIntervalAverageData

def season_energy(seasonRange, endYear, timeToExclude, df,  i):
    cols = df.columns
    excludeTime = False
    seasonRow = []
    if(excludeTime != 0):
        excludeTime = True
    if(seasonRange[0] > seasonRange[1]):
        for j in range(seasonRange[0], endYear):
            if( excludeTime == True and j >timeToExclude[0]):
                seasonRow.append(seasonRow[j-1])
                continue
            else:
                seasonRow.append(df.at[j,cols[i]])
        for j in range(0, seasonRange[1]):
            if( excludeTime == True and j > timeToExclude[0]):
                seasonRow.append(seasonRow[j-1])
                continue
            else:
                seasonRow.append(df.at[j,cols[i]])
    else:
        for k in range(seasonRange[0],seasonRange[1]):
            seasonRow.append(df.at[k, cols[i]])
    return seasonRow

def create_radiation_data(data_weather, seasonMonthRange):
    year = Year(2017)
    seasonIntervalRange = season_interval_range(seasonMonthRange, year.monthDays)
    radiationSeason = []
    cols = data_weather.columns
    if(seasonIntervalRange[0] < seasonIntervalRange[1]):
        for i in range(int(seasonIntervalRange[0]/4),int(seasonIntervalRange[1]/4)+1):
            for b in range(0,5):
                radiationSeason.append(data_weather.at[i,cols[10]])
    else:
        for i in range(int(seasonIntervalRange[0]/4),int(year.endOfYear/4)):
            for b in range(0,5):
                radiationSeason.append(data_weather.at[i,cols[10]])
        for i in range(0,int(seasonIntervalRange[1]/4)):
            for b in range(0,5):
                radiationSeason.append(data_weather.at[i,cols[10]])

    return radiationSeason
