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
    list_month_names = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    list_month_days = []
    end_of_year_int = 0
    def __init__(self) -> None:
        pass
    def __init__(self, year):
        if (year%4 == 0):
            self.list_month_days = [31,29,31,30,31,30,31,31,30,31,30,31]
        else:
            self.list_month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
        #Stores a value for the last interval in the year
        self.end_of_year_int = number_of_intervals_to_start_of_month(11, self.list_month_days) + number_of_intervals_to_day(31, 15)
        return
        
        
    
def number_of_days_to_month(months: list, list_month_days: list):
    """Returns the number of days before the specified month

    Args:
        months (int): The number of months before the target month (Ex: 3 for April)
        list_month_days (int list): A list containing the number of days in each month

    Returns:
        int: Total number of days before specified month
    """
    
    
    days = sum(list_month_days[i] for i in range(0,months))
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
    starting_int = multiplier*day
    return int(starting_int)

INTERVALS_PER_DAY = number_of_intervals_to_day(1,15) 

def number_of_intervals_to_start_of_month(month: int, list_month_days: list):
    """Finds the number of days to the start of a month

    Args:
        month (int): The month to find the number of intervals before
        list_month_days (int list): The number of days in each month

    Returns:
       Int: The interval index corresponding to the first day in the month
    """
    month_starting_day = number_of_days_to_month(month, list_month_days)
    month_starting_int = number_of_intervals_to_day(month_starting_day,15)
    return month_starting_int

def check_leap(year: int):
    """Checks whether the current year is a leap year and adjusts the days per month accordingly

    Args:
        year (int): The year to check leap for

    Returns:
        int list: The number of days in each month
    """    
    list_month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    if year%4 == 0:
        leap = True
    else:
         leap = False
    if leap == True:
        list_month_days[1] = 29
    return list_month_days



def season_interval_range(season_range: list, list_month_days: list):
    """Generates a list containing the first and last interval index for a range of months

    Args:
        season_range (int list): Contains the first and last month to find an interval range for
        list_month_days (int list): the number of days in a month

    Returns:
        int list: The first and last interval index for a range of months
    """    
    season_starting_int = number_of_intervals_to_start_of_month(season_range[0], list_month_days)
    season_ending_int = number_of_intervals_to_start_of_month(season_range[1], list_month_days)
    list_season_int_range = [season_starting_int, season_ending_int]
    return list_season_int_range

def break_range(break_starting_day: int, break_ending_day: int):
    """Generates an interval range for the days to exclude from the data

    Args:
        break_starting_day (int): The first day to be excluded
        break_ending_day (int): The last day to be exluded

    Returns:
        int list: Contains the first and last interval index for the specified break
    """    
    break_starting_int = int(number_of_intervals_to_day(break_starting_day, 15))
    break_ending_int = int(number_of_intervals_to_day(break_ending_day, 15))
    list_break_int_range = [break_starting_int, break_ending_int]
    return list_break_int_range

def month_name_and_interval_set( season_range: list, list_month_days: list,list_month_names: list):
    """_summary_

    Args:
        season_range (int list): _description_
        list_month_days (int list): _description_
        list_month_names (int list): _description_

    Returns:
        _type_: _description_
    """    
    list_month_names_and_int_positions = []
    list_month_names_for_season = [] # Change to a 2D tuple ie. month_nane_set[[names],[intervals]]
    list_month_int_positions = [0]
    j = 0
    if season_range[0] > season_range[1]:
        for i in range(season_range[0],12):
            list_month_names_for_season.append(list_month_names[i])
            if j > 0:
                list_month_int_positions.append(int( number_of_intervals_to_day(list_month_days[i],15))+list_month_int_positions[j-1])
            j +=1
        for i in range(0,season_range[1]+1):
            list_month_names_for_season.append(list_month_names[i])
            if j > 0:
                list_month_int_positions.append(int( number_of_intervals_to_day(list_month_days[i],15))+list_month_int_positions[j-1])
            j +=1
    else:
        for i in range(season_range[0],season_range[1]+1):
            list_month_names_for_season.append(list_month_names[i])
            if j > 0:
                list_month_int_positions.append(int( number_of_intervals_to_day(list_month_days[i],15))+list_month_int_positions[j-1])
            j +=1
    list_month_names_and_int_positions.append(list_month_names_for_season)
    list_month_names_and_int_positions.append(list_month_int_positions)
    return list_month_names_and_int_positions

# Generates daily averages across the length of list_seasonal_energy_use_data
def season_averages(list_seasonal_energy_use_data):
    list_average_row = []
    for interval in range(0,len(list_seasonal_energy_use_data[1])-1):
        sum_per_year =0
        for year in range(0,len(list_seasonal_energy_use_data)):
            sum_per_year += list_seasonal_energy_use_data[year][interval]
        average_season_energy_use = sum_per_year/len(list_seasonal_energy_use_data)
        list_average_row.append(average_season_energy_use)
    list_seasonal_energy_use_data.append(list_average_row)
    return list_seasonal_energy_use_data

# Generates daily averages across the length of list_seasonal_energy_use_data
def get_weekday_averages(list_seasonal_energy_use_data, bool_is_summer):
    list_average_weekday_row = []
    list_average_weekday_row = []
    interval_tracker = 0
    day_count = 0

    weekday_int_tracker = 0
    # This  loops through each interval in a day
    # The nested loop causes each interval in a day to be averaged for every 
    # occurance of that interval before continuing to the next interval
    for interval in range(0,len(list_seasonal_energy_use_data[1])-1):
        sum_weekday =0
        sum_weekend = 0
        weekday_count = 0
        weekend_count = 0
        
        for year in range(0,len(list_seasonal_energy_use_data)):
            if year == 0:
                if bool_is_summer == True:
                    weekday_int_tracker = 0
                else:
                    weekday_int_tracker = 96
            elif year == 1:
                if bool_is_summer == True:
                    weekday_int_tracker = 96
                else:
                    weekday_int_tracker = 96*2
            elif year == 2:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*2
                else:
                    weekday_int_tracker = 96*3
            elif year == 3:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*3
                else:
                    weekday_int_tracker = 96*4
            elif year == 4:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*5
                else:
                    weekday_int_tracker = 96*6
            elif year == 5:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*6
                else:
                    weekday_int_tracker = 0
            elif year == 6:
                if bool_is_summer == True:
                    weekday_int_tracker = 0
                else:
                    weekday_int_tracker = 96
            elif year == 7:
                if bool_is_summer == True:
                    weekday_int_tracker = 96
                else:
                    weekday_int_tracker = 96*2
            elif year == 8:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*3
                else:
                    weekday_int_tracker = 96*4
            elif year == 9:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*4
                else:
                    weekday_int_tracker = 96*5
            elif year == 10:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*5
                else:
                    weekday_int_tracker = 96*6
            elif year == 11:
                if bool_is_summer == True:
                    weekday_int_tracker = 96*6
                else:
                    weekday_int_tracker = 0      
            weekday_int_tracker += interval
            weekday_int_tracker = weekday_int_tracker % (96*7)
            if weekday_int_tracker < 96 or weekday_int_tracker >= (96*6):
                sum_weekend += list_seasonal_energy_use_data[year][interval]
                weekend_count +=1
            else:
                sum_weekday += list_seasonal_energy_use_data[year][interval]
                weekday_count +=1
            if interval_tracker == 76:
                interval_tracker = 0
                day_count +=1
            #dataSortedByInterval[day_count]
        average_weekend = 0
        average_weekday = 0
        #if weekday_int_tracker < 96 or weekday_int_tracker > (96*6):
        average_weekend = sum_weekend/weekend_count
        #else:
        average_weekday = sum_weekday/weekday_count
        #average_season_energy_use = sum_per_year/len(list_seasonal_energy_use_data)
        list_average_weekday_row.append(average_weekday)
        list_average_weekday_row.append(average_weekend)
    list_seasonal_energy_use_data.append(list_average_weekday_row)
    list_seasonal_energy_use_data.append(list_average_weekday_row)

    return list_seasonal_energy_use_data

def data_frame_to_excel_transpose(data, header, writer, sheet_name):
    df = pd.DataFrame(data).transpose()
    df.columns = header
    df.to_excel(writer, sheet_name = sheet_name)
    return df

def data_frame_to_excel(data, header, writer, sheet_name):
    df = pd.DataFrame(data)
    df.columns = header
    df.to_excel(writer, sheet_name = sheet_name)
    return df

def interval_average(list_seasonal_energy_use_data, year):
    list_int_average_over_a_day = []
    
    #Loops through all intervals for a 24hour period to construct a list
    # which contains the data seperated by the day
    #First loop goes through the first interval of each day
    # Inner loop goes through all the intervals for the day provied by the first interval
    for k in range(0,INTERVALS_PER_DAY-1):
        int_sum = 0
        int_average = 0
        for i in range(0,len(list_seasonal_energy_use_data[year])-INTERVALS_PER_DAY,INTERVALS_PER_DAY):
            int_sum += list_seasonal_energy_use_data[year][k+i]
        int_average = int_sum/((len(list_seasonal_energy_use_data[year])-1)/INTERVALS_PER_DAY)
        list_int_average_over_a_day.append(int_average)
    return list_int_average_over_a_day

def interval_average_dataset(list_seasonal_energy_use_data, year_selected):
    list_interval_seperated = []
    
    #Loops through all intervals for a 24hour period to construct a list
    # which contains the data seperated by interval
    #First loop goes through the first interval of each day
    # Inner loop goes through all the intervals for the day provied by the first interval
    for k in range(0,INTERVALS_PER_DAY-1):
        list_intervals = []
        for i in range(0,len(list_seasonal_energy_use_data[year_selected])-INTERVALS_PER_DAY,INTERVALS_PER_DAY):
            list_intervals.append(list_seasonal_energy_use_data[year_selected][k+i])
        list_interval_seperated.append(list_intervals)
    list_intervals = []
    #print(list_interval_seperated)
    #print(len(list_interval_seperated))
    # Constructs an array containing the 
    for b in range(0,INTERVALS_PER_DAY-1):
        #print(np.std(list_interval_seperated[b]))
        list_intervals.append(np.std(list_interval_seperated[b]))
        #print(b, "\n")
    list_interval_seperated.append(list_intervals)
 
    return list_interval_seperated

def get_input_year():
    print("Year Options:")
    bool_valid_year = False
    while(bool_valid_year == False):
        year = 2008
        for i in range(0,12):
            print("[",i, "] : ", year)
            year += 1
        print("[",i+1, "] : Average")
        year = int(input("Select Year: "))
        if(year < 13 and year > 0):
            bool_valid_year = True
        else:
            print("Invalid input")
    return year


def get_year_cooling(list_summer_energy_data, list_winter_energy_data, year):
    list_cooling_energy_data=[]
    if(len(list_winter_energy_data[year]) > len(list_summer_energy_data[year])):
        #print("Long Winter")
        for h in range(0,len(list_summer_energy_data[year])-1):
            list_cooling_energy_data.append(list_summer_energy_data[year][h]-list_winter_energy_data[year][h])
    else:
        #print("Long Summer")
        for h in range(0,len(list_winter_energy_data[year])-1):
            list_cooling_energy_data.append(list_summer_energy_data[year][h]-list_winter_energy_data[year][h])
    return list_cooling_energy_data

def get_cooling_day(list_summer_int_average, list_winter_int_average):
    list_cooling_int_average = []
    for i in range(0,len(list_summer_int_average)):
        list_cooling_int_average.append(list_summer_int_average[i]-list_winter_int_average[i])
    return list_cooling_int_average

def min_max_average_column(list_int_average):
    lowest = min(list_int_average)
    highest = max(list_int_average)
    average = mean(list_int_average)
    return lowest, highest, average


def create_season_energy(month_range: list,  df, bool_is_summer):
        
    # Initializes a nested array for each year + avg 
    #list_month_names = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    #list_month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    list_seasonal_energy_use_data = []
    year_num = 2008
    cols = df.columns
    for i in range(0,len(cols)):
        #Checks if its a leap year and, if so, adds 1 day to February
        obj_year = Year(year_num)
        year_num +=1
        #list_month_days = check_leap(i)
        
        #Stores the first and last interval of each season
        list_season_int_range = season_interval_range(month_range, obj_year.list_month_days)
        
        #Find the interval range for winter break (Dec 15 to Jan 10)
        list_break_int_range = break_range(number_of_days_to_month(11, obj_year.list_month_days)+15,10)

        list_single_season_data = season_energy(list_season_int_range, obj_year.end_of_year_int,list_break_int_range, df, i)

        list_seasonal_energy_use_data.append(list_single_season_data)


    list_seasonal_energy_use_data = season_averages(list_seasonal_energy_use_data)
    list_seasonal_energy_use_data = get_weekday_averages(list_seasonal_energy_use_data, bool_is_summer)
    return list_seasonal_energy_use_data

def create_data_sets(summer_month_range, winter_month_range, df, year):
    cols = df.columns
    list_summer_energy = create_season_energy(summer_month_range, df, True)
    list_winter_energy = create_season_energy(winter_month_range, df, False)

    #Finds the Set used to label each interval range 
    #Finds the months for each season
    obj_year = Year(2018)
    summer_month_and_int_set = month_name_and_interval_set(summer_month_range, obj_year.list_month_days, obj_year.list_month_names)
    winter_month_and_int_set = month_name_and_interval_set(winter_month_range, obj_year.list_month_days, obj_year.list_month_names)


    #   Arranging data for DataFrame and to print to excel
    avg= pd.Index(['Average'])
    seasonHeader = pd.Index(['Summer Load', 'Winter Load', 'Cooling Load'])
    finalColumns = cols.append(avg)

    
    #Gets daily averages over a given time period (Currently by year)
    list_summer_int_average = interval_average(list_summer_energy, year)
    list_winter_int_average = interval_average(list_winter_energy,  year)
    list_cooling_int_average = get_cooling_day(list_summer_int_average, list_winter_int_average)
    summer_weekday_int_average = interval_average(list_summer_energy, 13)
    summer_weekend_int_average = interval_average(list_summer_energy, 14)
    winter_weekday_int_average = interval_average(list_winter_energy, 13)
    winter_weekend_int_average = interval_average(list_winter_energy, 14)

    #Get cooling energy averages 
    list_cooling_energy_data = get_year_cooling(list_summer_energy, list_winter_energy, year)
    list_compiled_energy_data = [list_summer_energy[year],list_winter_energy[year],list_cooling_energy_data]

    #coolingInfo = min_max_average_column(list_cooling_int_average)

    combined_month_and_int_set = [[],[]]
    for i in range(0,len(summer_month_and_int_set)):
        combined_month_and_int_set[0].append(summer_month_and_int_set[0][i] + " / " + winter_month_and_int_set[0][i]) 
    combined_month_and_int_set[1] = summer_month_and_int_set[1]

    df_int_average_data = pd.DataFrame([list_summer_int_average, list_winter_int_average, list_cooling_int_average]).transpose()
    df_weekday_int_average_data = pd.DataFrame([summer_weekend_int_average, winter_weekend_int_average, summer_weekday_int_average, winter_weekday_int_average]).transpose()

    df_compiled_energy_data = pd.DataFrame(list_compiled_energy_data).transpose()
    df_winter_data = pd.DataFrame(list_winter_energy).transpose()
    df_summer_data = pd.DataFrame(list_summer_energy).transpose()
    df_cooling_data = pd.DataFrame(list_cooling_energy_data)


    return combined_month_and_int_set, df_compiled_energy_data, df_int_average_data, df_winter_data, df_summer_data, df_cooling_data, winter_month_and_int_set, df_weekday_int_average_data

def season_energy(season_range, end_of_year, time_to_exclude, df,  i):
    cols = df.columns
    bool_exclude_time = False
    list_single_season_data = []
    if(bool_exclude_time != 0):
        bool_exclude_time = True
    if(season_range[0] > season_range[1]):
        for j in range(season_range[0], end_of_year):
            if( bool_exclude_time == True and j >time_to_exclude[0]):
                list_single_season_data.append(list_single_season_data[j-1])
                continue
            else:
                list_single_season_data.append(df.at[j,cols[i]])
        for j in range(0, season_range[1]):
            if( bool_exclude_time == True and j > time_to_exclude[0]):
                list_single_season_data.append(list_single_season_data[j-1])
                continue
            else:
                list_single_season_data.append(df.at[j,cols[i]])
    else:
        for k in range(season_range[0],season_range[1]):
            list_single_season_data.append(df.at[k, cols[i]])
    return list_single_season_data

def create_radiation_data(df_weather_data, month_range):
    year = Year(2017)
    list_season_int_range = season_interval_range(month_range, year.list_month_days)
    list_radiation_season = []
    cols = df_weather_data.columns
    if(list_season_int_range[0] < list_season_int_range[1]):
        for i in range(int(list_season_int_range[0]/4),int(list_season_int_range[1]/4)+1):
            for b in range(0,5):
                list_radiation_season.append(df_weather_data.at[i,cols[10]])
    else:
        for i in range(int(list_season_int_range[0]/4),int(year.end_of_year_int/4)):
            for b in range(0,5):
                list_radiation_season.append(df_weather_data.at[i,cols[10]])
        for i in range(0,int(list_season_int_range[1]/4)):
            for b in range(0,5):
                list_radiation_season.append(df_weather_data.at[i,cols[10]])

    return list_radiation_season

def season_int_averages(list_seasonal_energy_use_data, year_selected):
    list_int_average = interval_average(list_seasonal_energy_use_data, year_selected)
    list_weekday_int_average = interval_average(list_seasonal_energy_use_data, 13)
    list_weekend_int_average = interval_average(list_seasonal_energy_use_data, 14)
    return list_int_average, list_weekday_int_average, list_weekend_int_average
    
def energy_use_data(year, list_cooling_int_average):
    chosen_year = 2008 +year
    if(chosen_year == 2020):
        chosen_year = "Average"
    print(chosen_year, " Energy Data: ")
    print("Area Under Energy use curve: ", simpson(list_cooling_int_average))
    print(trapezoid(list_cooling_int_average))
    print("Peak Cooling Load: ", max(list_cooling_int_average), "kWh")
    print("Average Cooling Load: ", mean(list_cooling_int_average), "kWh \n")